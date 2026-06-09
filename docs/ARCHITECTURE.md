# NNClaw · 可视化 ML 流水线架构设计

## 一、整体架构（简化版）

```
┌──────────────────────────────────────────────────────────────────┐
│                    Vue Frontend (Vue Flow)                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │ 节点面板   │  │ 画布编辑   │  │ 运行监控   │  │ 结果展示   │  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘  │
│         │              │              │              │             │
│         └──────────────┴──────┬───────┴──────────────┘             │
│                                │                                   │
│              HTTP REST (提交/查询) + WebSocket (进度推送)          │
└────────────────────────────────┼─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│              Python FastAPI Service (一体化)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │ REST API     │  │ 工作流引擎   │  │ 节点执行器              │  │
│  │ /api/...     │  │ 拓扑排序     │  │  ├ 数据源 (sklearn)     │  │
│  │ /ws/...      │  │ 异步调度     │  │  ├ 预处理 (split)       │  │
│  └──────────────┘  │ 任务状态     │  │  ├ 训练 (RF/SVM/...)    │  │
│                    └──────────────┘  │  ├ 评估 (accuracy/f1)   │  │
│                                     │  └ 可视化 (matplotlib)  │  │
│                                     └────────────────────────┘  │
│                                              │                    │
│                                              ▼                    │
│                                     ┌────────────────────┐        │
│                                     │  ML 库             │        │
│                                     │  scikit-learn      │        │
│                                     │  PyTorch (可选)    │        │
│                                     │  pandas/numpy      │        │
│                                     │  matplotlib        │        │
│                                     └────────────────────┘        │
└──────────────────────────────────────────────────────────────────┘
```

## 二、技术栈

| 层        | 技术                                                    |
| --------- | ------------------------------------------------------- |
| 前端      | Vue 3 + TypeScript + Vue Flow + Vue Router              |
| 实时通信  | 原生 WebSocket                                          |
| 后端      | Python 3.10+ + FastAPI + uvicorn + asyncio              |
| ML 库     | scikit-learn, PyTorch (可选), pandas, numpy, matplotlib |
| 状态/队列 | 内存 TaskStore（单机）/ 后期可加 Redis                  |

## 三、核心数据模型

### 3.1 工作流定义

```typescript
interface Workflow {
  nodes: MLNode[]
  edges: MLEdge[]
}

interface MLNode {
  id: string
  type: 'data_source' | 'preprocess' | 'train' | 'evaluate' | 'visualize'
  params: Record<string, any>
  position?: { x: number; y: number }
}

interface MLEdge {
  source: string
  target: string
  sourceHandle?: string
  targetHandle?: string
}
```

### 3.2 任务状态

```python
{
  "id": "task-abc123",
  "status": "running",  # pending | running | success | failed | cancelled
  "workflow": {...},
  "nodeStatuses": {
    "node-1": { "status": "success", "startedAt": "...", "finishedAt": "..." },
    "node-2": { "status": "running" }
  },
  "results": {
    "node-1": { ... 节点输出 ... }
  }
}
```

## 四、关键流程

### 4.1 工作流执行

```
1. 前端 POST /api/workflows/run 提交 { nodes, edges }
2. FastAPI 创建 task, 状态 = running
3. 拓扑排序, 按顺序遍历节点
4. 对每个节点:
   ├─> 从上游节点的 results 收集 inputs
   ├─> 在线程池中执行 executor.execute(params, inputs)
   ├─> 保存输出到 task.results
   └─> 更新 nodeStatuses
5. 通过 WebSocket (/ws/tasks/{id}) 实时推送 task 状态
6. 所有节点完成 → task.status = success
```

### 4.2 节点数据流

- 上游节点输出存在 `task.results[nodeId]`
- 当处理下游节点时，根据 edge 的 `sourceHandle` / `targetHandle` 映射成 inputs
- 小数据（参数、列表）通过 JSON 直接传
- 大数据（模型序列化用 base64 pickle）单次传递（生产环境应该用对象存储）

## 五、项目目录结构

```
nnclaw/
├── src/                        # Vue 前端
│   ├── api/pythonService.ts           # Python API 客户端
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── WorkflowView.vue
│   │   └── editor/
│   │       ├── WorkflowEditor.vue     # 画布主体
│   │       └── nodes/                 # 自定义节点
│   ├── router/
│   ├── App.vue
│   └── main.ts
│
├── python_svc/                 # Python FastAPI 服务 (一体化)
│   ├── app/
│   │   ├── main.py                    # FastAPI + 调度引擎
│   │   └── executors/                 # 节点执行器
│   │       ├── base.py
│   │       ├── data_source.py
│   │       ├── preprocess.py
│   │       ├── train.py
│   │       ├── evaluate.py
│   │       └── visualize.py
│   ├── requirements.txt
│   └── pyproject.toml
│
└── docs/
    └── ARCHITECTURE.md          # 本文档
```

## 六、API 端点

| 端点                     | 方法 | 说明                    |
| ------------------------ | ---- | ----------------------- |
| `/`                      | GET  | 服务信息 + 可用节点类型 |
| `/api/health`            | GET  | 健康检查                |
| `/api/nodes`             | GET  | 列出所有节点 schema     |
| `/api/workflows/run`     | POST | 提交工作流执行          |
| `/api/tasks/{id}`        | GET  | 查询任务状态            |
| `/api/tasks/{id}/cancel` | POST | 取消任务                |
| `/api/nodes/execute`     | POST | 单节点执行（调试）      |
| `/ws/tasks/{id}`         | WS   | 实时任务进度            |

## 七、扩展节点

1. 在 `python_svc/app/executors/` 新建文件，实现 `BaseExecutor`：

```python
class MyExecutor(BaseExecutor):
    def execute(self, params, inputs):
        # 业务逻辑
        return {"output_key": result}

    def get_schema(self):
        return {
            "type": "my_node",
            "label": "我的节点",
            "params": {...},
            "inputs": [...],
            "outputs": [...],
        }
```

2. 在 `main.py` 注册：

```python
from app.executors.my_executor import MyExecutor
registry.register('my_node', MyExecutor())
```

3. 前端通过 `GET /api/nodes` 自动发现新节点。

## 八、迭代路线

| 阶段 | 内容                                                       |
| ---- | ---------------------------------------------------------- |
| M0   | UI 框架 ✅                                                 |
| M1   | 集成 Vue Flow，画布可编辑 ✅                               |
| M2   | 搭建 Python FastAPI 服务骨架 ✅                            |
| M3   | 5 类基础节点 (data/preprocess/train/evaluate/visualize) ✅ |
| M4   | WebSocket 实时进度 ✅                                      |
| M5   | 结果可视化展示 ✅                                          |
| M6   | 节点类型扩展（PyTorch 训练、XGBoost 等）                   |
| M7   | 异步任务队列（Celery/Redis）                               |
| M8   | 工作流模板市场                                             |
