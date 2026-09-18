import os
import json
from fastapi import APIRouter, HTTPException
from app.config import settings
from app.schemas.models_info import ModelRegistryResponse

router = APIRouter(prefix="/models", tags=["Model Registry & Benchmarks"])

@router.get("/registry", response_model=ModelRegistryResponse)
def get_model_registry():
    path = settings.MODEL_REGISTRY_PATH
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Model registry metadata not found")
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "active_models": data.get("models", {}),
            "benchmarks": data.get("benchmarks", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read model registry: {str(e)}")
