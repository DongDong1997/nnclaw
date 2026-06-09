"""模型训练节点"""
from typing import Dict, Any
import numpy as np
import pickle
import base64
from .base import BaseExecutor


class TrainExecutor(BaseExecutor):
    """支持多种 sklearn 模型"""

    ALGOS = {
        "RandomForest": "sklearn.ensemble.RandomForestClassifier",
        "LogisticRegression": "sklearn.linear_model.LogisticRegression",
        "SVM": "sklearn.svm.SVC",
        "KNN": "sklearn.neighbors.KNeighborsClassifier",
        "DecisionTree": "sklearn.tree.DecisionTreeClassifier",
    }

    def execute(self, params: Dict[str, Any], inputs: Dict[str, Any]) -> Dict[str, Any]:
        algo = params.get("algorithm", "RandomForest")
        X_train = np.array(inputs.get("X_train"))
        y_train = np.array(inputs.get("y_train"))

        if algo == "RandomForest":
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(
                n_estimators=params.get("n_estimators", 100),
                max_depth=params.get("max_depth", 5),
                random_state=42,
            )
        elif algo == "LogisticRegression":
            from sklearn.linear_model import LogisticRegression
            model = LogisticRegression(max_iter=1000)
        elif algo == "SVM":
            from sklearn.svm import SVC
            model = SVC()
        elif algo == "KNN":
            from sklearn.neighbors import KNeighborsClassifier
            model = KNeighborsClassifier(n_neighbors=params.get("n_neighbors", 5))
        elif algo == "DecisionTree":
            from sklearn.tree import DecisionTreeClassifier
            model = DecisionTreeClassifier(max_depth=params.get("max_depth", 5))
        else:
            raise ValueError(f"Unknown algorithm: {algo}")

        model.fit(X_train, y_train)

        # 序列化模型为 base64 (实际生产中应该用对象存储)
        model_bytes = pickle.dumps(model)
        model_b64 = base64.b64encode(model_bytes).decode("utf-8")

        return {
            "model": {
                "type": algo,
                "serialized": model_b64,
                "train_score": float(model.score(X_train, y_train)),
            }
        }

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "train",
            "label": "模型训练",
            "params": {
                "algorithm": {
                    "type": "select",
                    "options": list(self.ALGOS.keys()),
                    "default": "RandomForest",
                },
                "n_estimators": {"type": "number", "default": 100},
                "max_depth": {"type": "number", "default": 5},
            },
            "inputs": [
                {"id": "X_train", "label": "X_train", "dataType": "dataset"},
                {"id": "y_train", "label": "y_train", "dataType": "dataset"},
            ],
            "outputs": [
                {"id": "model", "label": "model", "dataType": "model"}
            ],
        }
