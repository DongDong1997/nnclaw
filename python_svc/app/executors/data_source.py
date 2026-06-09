"""数据源节点"""
from typing import Dict, Any
from .base import BaseExecutor


class DataSourceExecutor(BaseExecutor):
    """从内置数据集或文件加载数据"""

    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        source = params.get("source", "iris")

        if source == "iris":
            from sklearn.datasets import load_iris
            data = load_iris()
            return {
                "dataset": {
                    "X": data.data.tolist(),
                    "y": data.target.tolist(),
                    "feature_names": list(data.feature_names),
                    "target_names": list(data.target_names),
                    "n_samples": len(data.data),
                }
            }
        elif source == "boston":
            from sklearn.datasets import fetch_california_housing
            data = fetch_california_housing()
            return {
                "dataset": {
                    "X": data.data.tolist(),
                    "y": data.target.tolist(),
                    "feature_names": list(data.feature_names),
                    "n_samples": len(data.data),
                }
            }
        else:
            raise ValueError(f"Unknown data source: {source}")

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "data_source",
            "label": "数据源",
            "params": {
                "source": {
                    "type": "select",
                    "options": ["iris", "boston"],
                    "default": "iris",
                }
            },
            "inputs": [],
            "outputs": [
                {"id": "dataset", "label": "dataset", "dataType": "dataset"}
            ],
        }
