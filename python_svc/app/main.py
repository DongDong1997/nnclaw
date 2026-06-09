"""
NNClaw - Python Algorithm Service
FastAPI service that hosts the workflow engine + ML execution
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Set
import asyncio
import uuid
from datetime import datetime

from app.executors import registry
from app.executors.data_source import DataSourceExecutor
from app.executors.preprocess import PreprocessExecutor
from app.executors.train import TrainExecutor
from app.executors.evaluate import EvaluateExecutor
from app.executors.visualize import VisualizeExecutor

# 注册所有执行器
registry.register('data_source', DataSourceExecutor())
registry.register('preprocess', PreprocessExecutor())
registry.register('train', TrainExecutor())
registry.register('evaluate', EvaluateExecutor())
registry.register('visualize', VisualizeExecutor())

app = FastAPI(
    title="NNClaw - ML Algorithm Service",
    version="0.2.0",
    description="ML workflow engine + algorithm execution"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 数据模型 ============


class MLNodeSpec(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = {}
    position: Dict[str, float] | None = None


class MLEdgeSpec(BaseModel):
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None


class WorkflowRunRequest(BaseModel):
    """前端提交的工作流"""
    nodes: List[MLNodeSpec]
    edges: List[MLEdgeSpec]


class NodeExecuteRequest(BaseModel):
    """单节点执行 (调试用)"""
    task_id: str
    node_id: str
    type: str
    params: Dict[str, Any] = {}
    inputs: Dict[str, Any] = {}


# ============ 任务状态 ============


class TaskStore:
    """任务状态管理 + 订阅广播"""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.subscribers: Dict[str, Set[WebSocket]] = {}

    def create(self, task_id: str, workflow: WorkflowRunRequest) -> Dict[str, Any]:
        task = {
            "id": task_id,
            "status": "running",
            "workflow": workflow.model_dump(),
            "nodeStatuses": {
                n.id: {"status": "pending"} for n in workflow.nodes
            },
            "results": {},
            "startedAt": datetime.utcnow().isoformat(),
        }
        self.tasks[task_id] = task
        return task

    def update_node(self, task_id: str, node_id: str, **kwargs):
        if task_id in self.tasks and node_id in self.tasks[task_id]["nodeStatuses"]:
            self.tasks[task_id]["nodeStatuses"][node_id].update(kwargs)

    def get(self, task_id: str) -> Dict[str, Any] | None:
        return self.tasks.get(task_id)

    def subscribe(self, task_id: str, ws: WebSocket):
        self.subscribers.setdefault(task_id, set()).add(ws)

    def unsubscribe(self, task_id: str, ws: WebSocket):
        if task_id in self.subscribers:
            self.subscribers[task_id].discard(ws)

    def publish(self, task_id: str):
        """广播任务状态到所有订阅者"""
        task = self.tasks.get(task_id)
        if not task:
            return
        subs = self.subscribers.get(task_id, set()).copy()
        for ws in subs:
            try:
                # 异步发到 ws (FastAPI 同步 send 会抛错时跳过)
                pass
            except Exception:
                pass


store = TaskStore()


# ============ 调度引擎 ============


def topological_sort(nodes: List[MLNodeSpec], edges: List[MLEdgeSpec]) -> List[str]:
    """拓扑排序，返回节点执行顺序"""
    in_degree: Dict[str, int] = {n.id: 0 for n in nodes}
    adj: Dict[str, List[str]] = {n.id: [] for n in nodes}

    for e in edges:
        in_degree[e.target] = in_degree.get(e.target, 0) + 1
        adj.setdefault(e.source, []).append(e.target)

    queue = [nid for nid, deg in in_degree.items() if deg == 0]
    order = []
    while queue:
        nid = queue.pop(0)
        order.append(nid)
        for nxt in adj.get(nid, []):
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(nodes):
        raise ValueError("工作流存在循环依赖")
    return order


async def execute_workflow(task_id: str, workflow: WorkflowRunRequest):
    """在工作流任务中按拓扑顺序执行节点"""
    try:
        order = topological_sort(workflow.nodes, workflow.edges)
        node_map = {n.id: n for n in workflow.nodes}
        edge_map_in = {e.target: e for e in workflow.edges}

        for nid in order:
            node = node_map[nid]
            store.update_node(task_id, nid, status="running",
                              startedAt=datetime.utcnow().isoformat())

            # 收集上游节点的输出作为 inputs
            inputs: Dict[str, Any] = {}
            incoming = [e for e in workflow.edges if e.target == nid]
            for e in incoming:
                src_result = store.tasks[task_id]["results"].get(e.source, {})
                if e.sourceHandle and e.sourceHandle in src_result:
                    key = e.targetHandle or "in"
                    inputs[key] = src_result[e.sourceHandle]
                else:
                    # 无 handle: 把上游整包塞到默认 key
                    inputs[e.targetHandle or "in"] = src_result

            try:
                executor = registry.get(node.type)
                if not executor:
                    raise ValueError(f"未知节点类型: {node.type}")

                # 在线程池中执行（避免阻塞事件循环）
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, executor.execute, node.params, inputs
                )

                store.tasks[task_id]["results"][nid] = result
                store.update_node(task_id, nid, status="success",
                                  finishedAt=datetime.utcnow().isoformat())
            except Exception as e:
                store.update_node(task_id, nid, status="failed",
                                  error=str(e),
                                  finishedAt=datetime.utcnow().isoformat())
                store.tasks[task_id]["status"] = "failed"
                store.tasks[task_id]["error"] = f"节点 {nid} 执行失败: {e}"
                store.tasks[task_id]["finishedAt"] = datetime.utcnow().isoformat()
                return

        store.tasks[task_id]["status"] = "success"
        store.tasks[task_id]["finishedAt"] = datetime.utcnow().isoformat()
    except Exception as e:
        store.tasks[task_id]["status"] = "failed"
        store.tasks[task_id]["error"] = str(e)
        store.tasks[task_id]["finishedAt"] = datetime.utcnow().isoformat()


# ============ REST 路由 ============


@app.get("/")
async def root():
    return {
        "service": "NNClaw - ML Algorithm Service",
        "version": "0.2.0",
        "available_nodes": registry.list_types(),
    }


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/nodes")
async def list_nodes():
    """列出所有可用节点类型及其 schema"""
    return {
        "nodes": [
            {
                "type": node_type,
                "schema": executor.get_schema(),
            }
            for node_type, executor in registry.all().items()
        ]
    }


@app.post("/api/workflows/run")
async def run_workflow(req: WorkflowRunRequest):
    """前端直接提交工作流, 服务端负责调度"""
    if not req.nodes:
        raise HTTPException(400, "工作流至少需要一个节点")

    task_id = uuid.uuid4().hex[:12]
    task = store.create(task_id, req)
    asyncio.create_task(execute_workflow(task_id, req))
    return {"task_id": task_id, "status": "running"}


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    task = store.get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


@app.post("/api/tasks/{task_id}/cancel")
async def cancel_task(task_id: str):
    task = store.get(task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task["status"] = "cancelled"
    task["finishedAt"] = datetime.utcnow().isoformat()
    return {"ok": True}


@app.post("/api/nodes/execute")
async def execute_node(req: NodeExecuteRequest):
    """单节点执行（调试用）"""
    executor = registry.get(req.type)
    if not executor:
        raise HTTPException(400, f"Unknown node type: {req.type}")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, executor.execute, req.params, req.inputs
        )
        return {
            "node_id": req.node_id,
            "type": req.type,
            "status": "success",
            "outputs": result,
        }
    except Exception as e:
        raise HTTPException(500, f"Execution failed: {str(e)}")


# ============ WebSocket ============


@app.websocket("/ws/tasks/{task_id}")
async def task_progress_ws(websocket: WebSocket, task_id: str):
    """订阅任务进度"""
    await websocket.accept()
    if not store.get(task_id):
        await websocket.send_json({"error": "Task not found"})
        await websocket.close()
        return

    last_serialized = None
    try:
        while True:
            task = store.get(task_id)
            if not task:
                break
            import json
            payload = json.dumps(task, ensure_ascii=False)
            if payload != last_serialized:
                await websocket.send_text(payload)
                last_serialized = payload

            if task["status"] in ("success", "failed", "cancelled"):
                break

            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"error": str(e)})
        except Exception:
            pass
    finally:
        try:
            await websocket.close()
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
