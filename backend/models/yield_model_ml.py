"""
ML-based Yield Estimation Model
Uses trained RandomForest regressor for yield predictions
"""
import joblib
import numpy as np
import os

# Global model objects
yield_model = None
yield_scaler = None
yield_features = None
yield_encoders = None

def load_models():
    """Load trained models into memory"""
    global yield_model, yield_scaler, yield_features, yield_encoders
    
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
    
    yield_model = joblib.load(os.path.join(model_dir, 'yield_model.pkl'))
    yield_scaler = joblib.load(os.path.join(model_dir, 'yield_scaler.pkl'))
    yield_features = joblib.load(os.path.join(model_dir, 'yield_features.pkl'))
    yield_encoders = joblib.load(os.path.join(model_dir, 'yield_encoders.pkl'))
    
    return True

def estimate_yield(
    crop_type: str,
    area_hectares: float,
    season: str,
    rainfall: float,
    temperature: float,
    fertilizer_used: float
) -> float:
    """
    Estimate crop yield using trained ML model.
    
    Returns:
        Estimated yield in kg/ha
    """
    global yield_model, yield_scaler, yield_features, yield_encoders
    
    # Load models if not already loaded
    if yield_model is None:
        load_models()
    
    # Prepare features
    # Feature order from training varies, use what we have
    features_dict = {}
    
    for feat in yield_features:
        if feat == 'Area':
            features_dict[feat] = area_hectares
        elif feat == 'Item':
            # Encode crop type
            if 'Item' in yield_encoders:
                try:
                    features_dict[feat] = yield_encoders['Item'].transform([crop_type])[0]
                except:
                    features_dict[feat] = 0
            else:
                features_dict[feat] = 0
        elif feat == 'Year':
            features_dict[feat] = 2025  # Current year
        elif feat == 'average_rain_fall_mm_per_year':
            features_dict[feat] = rainfall * 10  # Convert to yearly estimate
        elif feat == 'pesticides_tonnes':
            features_dict[feat] = fertilizer_used / 100  # Rough conversion
        elif feat == 'avg_temp':
            features_dict[feat] = temperature
        elif 'Unnamed' in feat:
            features_dict[feat] = 0  # Index column, use 0
        else:
            features_dict[feat] = 0
    
    # Create feature array
    X = np.array([[features_dict[feat] for feat in yield_features]])
    
    # Scale features
    X_scaled = yield_scaler.transform(X)
    
    # Predict yield (in hg/ha, need to convert to kg/ha)
    yield_hg_ha = yield_model.predict(X_scaled)[0]
    yield_kg_ha = yield_hg_ha / 10  # Convert hectogram to kilogram
    
    # Ensure positive yield
    yield_kg_ha = max(100, yield_kg_ha)  # Minimum 100 kg/ha
    
    return float(yield_kg_ha)
