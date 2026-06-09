"""节点执行器基类"""
from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseExecutor(ABC):
    """所有节点执行器的抽象基类"""

    @abstractmethod
    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行节点逻辑

        Args:
            params: 节点参数
            inputs: 上游节点的输出 (key=端口ID, value=数据)

        Returns:
            节点的输出, key 为输出端口ID
        """
        raise NotImplementedError

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """返回节点的 JSON Schema (前端用于动态生成参数表单)"""
        raise NotImplementedError
