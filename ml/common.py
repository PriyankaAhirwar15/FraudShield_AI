import os
import json
import joblib
import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc,
    confusion_matrix
)
from app.core.logging import logger

def calculate_all_metrics(y_true, y_prob, threshold=0.5):
    y_pred = (np.array(y_prob) >= threshold).astype(int)
    y_t = np.array(y_true).astype(int)
    
    precision = float(precision_score(y_t, y_pred, zero_division=0))
    recall = float(recall_score(y_t, y_pred, zero_division=0))
    f1 = float(f1_score(y_t, y_pred, zero_division=0))
    
    try:
        roc_auc = float(roc_auc_score(y_t, y_prob))
    except Exception:
        roc_auc = 0.5
        
    try:
        precisions, recalls, _ = precision_recall_curve(y_t, y_prob)
        pr_auc = float(auc(recalls, precisions))
    except Exception:
        pr_auc = 0.0
        
    cm = confusion_matrix(y_t, y_pred).tolist()
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "threshold": round(threshold, 3),
        "confusion_matrix": cm
    }

def save_artifact(obj, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(obj, filepath)
    logger.info(f"Saved artifact to {filepath}")

def load_artifact(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model artifact not found at {filepath}")
    return joblib.load(filepath)

def update_model_registry(registry_path: str, model_data: dict):
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    registry = {"models": {}, "benchmarks": []}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            logger.warning(f"Could not parse existing registry: {e}")
            registry = {"models": {}, "benchmarks": []}
            
    registry["models"][model_data["model_key"]] = model_data["model_version"]
    
    benchmarks = [b for b in registry.get("benchmarks", []) if b.get("model_name") != model_data.get("model_name")]
    benchmarks.append(model_data)
    registry["benchmarks"] = benchmarks
    
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    logger.info(f"Updated model registry at {registry_path}")
