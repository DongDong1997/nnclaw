# Python ML Algorithm Service

为 NNClaw 工作流引擎提供 ML 算法执行能力。

## 安装

```bash
cd python_svc
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 启动

```bash
cd python_svc
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

### GET `/api/nodes`

列出所有可用节点类型及其 JSON Schema。

### POST `/api/tasks/submit`

提交一个工作流任务。

```json
{
  "task_id": "task-001",
  "nodes": [
    {
      "id": "n1",
      "type": "data_source",
      "params": { "source": "iris" },
      "inputs": {}
    },
    {
      "id": "n2",
      "type": "train",
      "params": { "algorithm": "RandomForest", "n_estimators": 100 },
      "inputs": {
        "X_train": [...],
        "y_train": [...]
      }
    }
  ]
}
```

### GET `/api/tasks/{task_id}`

查询任务状态和结果。

### WS `/ws/tasks/{task_id}`

WebSocket 实时获取任务进度。

## 扩展新节点

1. 在 `app/executors/` 下新建文件，实现 `BaseExecutor`：

```python
from .base import BaseExecutor

class MyExecutor(BaseExecutor):
    def execute(self, params, inputs):
        # 你的逻辑
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

2. 在 `app/main.py` 中注册：

```python
from app.executors.my_executor import MyExecutor
registry.register('my_node', MyExecutor())
```

前端可通过 `GET /api/nodes` 自动发现新节点。
