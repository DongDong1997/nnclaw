"""可视化节点"""
from typing import Dict, Any
import base64
import io
from .base import BaseExecutor


class VisualizeExecutor(BaseExecutor):
    """生成混淆矩阵等图表, 返回 base64 PNG"""

    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            return {"image": None, "error": "matplotlib not installed"}

        chart_type = params.get("chart", "confusion_matrix")
        metrics = inputs.get("metrics")

        if chart_type == "confusion_matrix" and metrics:
            from sklearn.metrics import confusion_matrix
            report = metrics.get("report", {})
            y_true = None
            y_pred = inputs.get("predictions")

            # 重新计算 (这里简化处理)
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.text(0.5, 0.5, f"Accuracy: {metrics.get('accuracy', 0):.2%}\n"
                    f"F1: {metrics.get('f1_macro', 0):.2%}",
                    ha="center", va="center", fontsize=20, color="#FFD500")
            ax.axis("off")
            ax.set_facecolor("#0a0a0a")
            fig.patch.set_facecolor("#0a0a0a")

        elif chart_type == "metrics_bar":
            fig, ax = plt.subplots(figsize=(6, 4))
            labels = ["Accuracy", "F1 (macro)", "F1 (weighted)"]
            values = [
                metrics.get("accuracy", 0) if metrics else 0,
                metrics.get("f1_macro", 0) if metrics else 0,
                metrics.get("f1_weighted", 0) if metrics else 0,
            ]
            ax.bar(labels, values, color="#FFD500")
            ax.set_ylim(0, 1)
            ax.set_facecolor("#0a0a0a")
            fig.patch.set_facecolor("#0a0a0a")
        else:
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.text(0.5, 0.5, "No data", ha="center", va="center")
            ax.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", facecolor="#0a0a0a")
        buf.seek(0)
        image_b64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        return {"image": image_b64}

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "visualize",
            "label": "可视化",
            "params": {
                "chart": {
                    "type": "select",
                    "options": ["confusion_matrix", "metrics_bar"],
                    "default": "confusion_matrix",
                }
            },
            "inputs": [
                {"id": "metrics", "label": "metrics", "dataType": "metric"}
            ],
            "outputs": [
                {"id": "image", "label": "image", "dataType": "image"}
            ],
        }
