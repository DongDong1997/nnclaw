"""模型评估节点"""
from typing import Dict, Any
import numpy as np
import pickle
import base64
from .base import BaseExecutor


class EvaluateExecutor(BaseExecutor):
    """计算 accuracy / f1 等指标"""

    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        from sklearn.metrics import accuracy_score, f1_score, classification_report

        model_data = inputs.get("model", {}).get("model", inputs.get("model"))
        if isinstance(model_data, dict) and "serialized" in model_data:
            model_bytes = base64.b64decode(model_data["serialized"])
            model = pickle.loads(model_bytes)
        else:
            raise ValueError("无效的模型输入")

        X_test = np.array(inputs.get("X_test"))
        y_test = np.array(inputs.get("y_test"))

        y_pred = model.predict(X_test)

        return {
            "metrics": {
                "accuracy": float(accuracy_score(y_test, y_pred)),
                "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
                "f1_weighted": float(f1_score(y_test, y_pred, average="weighted")),
                "report": classification_report(y_test, y_pred, output_dict=True),
                "n_test": int(len(y_test)),
            },
            "predictions": y_pred.tolist(),
        }

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "evaluate",
            "label": "模型评估",
            "params": {},
            "inputs": [
                {"id": "model", "label": "model", "dataType": "model"},
                {"id": "X_test", "label": "X_test", "dataType": "dataset"},
                {"id": "y_test", "label": "y_test", "dataType": "dataset"},
            ],
            "outputs": [
                {"id": "metrics", "label": "metrics", "dataType": "metric"}
            ],
        }
