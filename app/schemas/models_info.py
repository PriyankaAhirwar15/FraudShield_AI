from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, List

class ModelMetric(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    model_type: str
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    pr_auc: float
    threshold: float
    training_date: str

class ModelRegistryResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    active_models: Dict[str, str]
    benchmarks: List[ModelMetric]
