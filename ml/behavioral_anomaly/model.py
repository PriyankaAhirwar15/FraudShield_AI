import numpy as np
from sklearn.ensemble import IsolationForest
from ml.common import save_artifact, load_artifact

class BehavioralIsolationForest:
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.version = "behavior_iforest_v1"

    def fit(self, X: np.ndarray):
        self.model.fit(X)
        return self

    def score(self, X: np.ndarray) -> np.ndarray:
        raw_scores = self.model.decision_function(X)
        normalized = 1.0 / (1.0 + np.exp(raw_scores * 3.0))
        return np.clip(normalized, 0.0, 1.0)

    def save(self, path: str):
        save_artifact(self, path)

    @classmethod
    def load(cls, path: str):
        return load_artifact(path)
