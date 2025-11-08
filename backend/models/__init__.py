"""
Models package for AgroSmart prediction system.
Now using trained ML models instead of rule-based logic.
"""
# Import ML-based prediction functions
from .crop_model_ml import predict_crop, load_models as load_crop_model
from .fertilizer_model_ml import recommend_fertilizer, load_models as load_fert_model
from .yield_model_ml import estimate_yield, load_models as load_yield_model

# Export functions
__all__ = [
    "predict_crop",
    "recommend_fertilizer",
    "estimate_yield",
    "load_crop_model",
    "load_fert_model",
    "load_yield_model"
]

# Load all models on import
def initialize_models():
    """Initialize all ML models"""
    try:
        load_crop_model()
        load_fert_model()
        load_yield_model()
        return True
    except Exception as e:
        print(f"Warning: Could not load all models: {e}")
        return False
