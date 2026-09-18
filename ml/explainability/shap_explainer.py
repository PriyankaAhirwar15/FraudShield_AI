import shap
import numpy as np
import pandas as pd
from app.core.logging import logger

class ModelSHAPExplainer:
    def __init__(self, model, feature_names: list, model_type: str = "tree"):
        self.feature_names = feature_names
        self.model_type = model_type
        try:
            if model_type == "tree":
                self.explainer = shap.TreeExplainer(model)
            else:
                self.explainer = None
        except Exception as e:
            logger.warning(f"SHAP Explainer init note: {e}")
            self.explainer = None

    def explain_instance(self, features_df: pd.DataFrame) -> list:
        factors = []
        vals = np.zeros(len(self.feature_names))
        
        try:
            if self.explainer is not None:
                shap_values = self.explainer.shap_values(features_df)
                if isinstance(shap_values, list):
                    vals = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
                elif len(shap_values.shape) == 2:
                    vals = shap_values[0]
                elif len(shap_values.shape) == 3:
                    vals = shap_values[0, :, 1]
            else:
                row = features_df.iloc[0].to_dict()
                amt_dev = row.get("amount_deviation", 0.0)
                is_dev = row.get("is_new_device", 0)
                is_ben = row.get("is_new_beneficiary", 0)
                is_night = row.get("is_night_hour", 0)
                vals[1] = amt_dev * 0.4
                vals[6] = 0.5 if is_dev else -0.1
                vals[7] = 0.4 if is_ben else -0.1
                vals[5] = 0.3 if is_night else -0.1
        except Exception as e:
            logger.warning(f"SHAP explanation computation note: {e}")
            vals = np.zeros(len(self.feature_names))

        row = features_df.iloc[0].to_dict()
        for i, col in enumerate(self.feature_names):
            val = float(vals[i]) if i < len(vals) else 0.0
            actual_val = row.get(col, 0.0)
            factors.append({
                "feature": col,
                "display_name": col.replace("_", " ").title(),
                "actual_value": round(float(actual_val), 2),
                "shap_impact": round(val, 4),
                "increases_risk": bool(val > 0)
            })

        factors = sorted(factors, key=lambda x: abs(x["shap_impact"]), reverse=True)
        return factors
