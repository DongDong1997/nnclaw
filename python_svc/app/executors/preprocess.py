"""数据预处理节点"""
from typing import Dict, Any
import numpy as np
from .base import BaseExecutor


class PreprocessExecutor(BaseExecutor):
    """数据集划分 / 标准化等"""

    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        from sklearn.model_selection import train_test_split

        dataset = inputs.get("dataset", inputs.get("in"))
        if not dataset:
            raise ValueError("缺少输入: dataset")

        X = np.array(dataset["X"])
        y = np.array(dataset["y"])

        test_size = params.get("test_size", 0.2)
        random_state = params.get("random_state", 42)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        return {
            "X_train": X_train.tolist(),
            "X_test": X_test.tolist(),
            "y_train": y_train.tolist(),
            "y_test": y_test.tolist(),
        }

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "preprocess",
            "label": "数据预处理",
            "params": {
                "test_size": {"type": "number", "default": 0.2, "min": 0.1, "max": 0.5},
                "random_state": {"type": "number", "default": 42},
            },
            "inputs": [
                {"id": "in", "label": "dataset", "dataType": "dataset"}
            ],
            "outputs": [
                {"id": "X_train", "label": "X_train", "dataType": "dataset"},
                {"id": "X_test", "label": "X_test", "dataType": "dataset"},
                {"id": "y_train", "label": "y_train", "dataType": "dataset"},
                {"id": "y_test", "label": "y_test", "dataType": "dataset"},
            ],
        }
