"""节点执行器注册表"""
from typing import Dict, Optional
from .base import BaseExecutor


class ExecutorRegistry:
    def __init__(self):
        self._executors: Dict[str, BaseExecutor] = {}

    def register(self, node_type: str, executor: BaseExecutor):
        self._executors[node_type] = executor

    def get(self, node_type: str) -> Optional[BaseExecutor]:
        return self._executors.get(node_type)

    def all(self) -> Dict[str, BaseExecutor]:
        return self._executors

    def list_types(self) -> list:
        return list(self._executors.keys())


registry = ExecutorRegistry()
