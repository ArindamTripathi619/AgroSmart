"""
ML-based Fertilizer Recommendation Model
Uses trained RandomForest model for fertilizer recommendations
"""
import joblib
import numpy as np
from typing import Dict
import os

# Global model objects
fert_model = None
fert_scaler = None
fert_features = None
fert_encoders = None

def load_models():
    """Load trained models into memory"""
    global fert_model, fert_scaler, fert_features, fert_encoders
    
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
    
    fert_model = joblib.load(os.path.join(model_dir, 'fertilizer_model.pkl'))
    fert_scaler = joblib.load(os.path.join(model_dir, 'fertilizer_scaler.pkl'))
    fert_features = joblib.load(os.path.join(model_dir, 'fertilizer_features.pkl'))
    fert_encoders = joblib.load(os.path.join(model_dir, 'fertilizer_encoders.pkl'))
    
    return True

def recommend_fertilizer(
    soil_type: str,
    crop_type: str,
    n_level: int,
    p_level: int,
    k_level: int,
    temperature: float,
    humidity: float,
    moisture: float
) -> Dict[str, any]:
    """
    Recommend fertilizer using trained ML model.
    
    Returns:
        Dictionary with fertilizer_name and application_rate
    """
    global fert_model, fert_scaler, fert_features, fert_encoders
    
    # Load models if not already loaded
    if fert_model is None:
        load_models()
    
    # Prepare features
    # Feature order from training: Temperature, Moisture, Rainfall, PH, Nitrogen, Phosphorous, Potassium, Carbon, Soil, Crop, Remark
    # We'll use what we have and fill missing with defaults
    features_dict = {}
    
    for feat in fert_features:
        if feat == 'Temperature':
            features_dict[feat] = temperature
        elif feat == 'Moisture':
            features_dict[feat] = moisture
        elif feat == 'Rainfall':
            features_dict[feat] = 0  # Default, not provided in API
        elif feat == 'PH':
            features_dict[feat] = 7.0  # Default neutral pH
        elif feat == 'Nitrogen':
            features_dict[feat] = n_level
        elif feat == 'Phosphorous':
            features_dict[feat] = p_level
        elif feat == 'Potassium':
            features_dict[feat] = k_level
        elif feat == 'Carbon':
            features_dict[feat] = 20  # Default carbon level
        elif feat == 'Soil':
            # Encode soil type
            if 'Soil' in fert_encoders:
                try:
                    features_dict[feat] = fert_encoders['Soil'].transform([soil_type])[0]
                except:
                    features_dict[feat] = 0
            else:
                features_dict[feat] = 0
        elif feat == 'Crop':
            # Encode crop type
            if 'Crop' in fert_encoders:
                try:
                    features_dict[feat] = fert_encoders['Crop'].transform([crop_type])[0]
                except:
                    features_dict[feat] = 0
            else:
                features_dict[feat] = 0
        elif feat == 'Remark':
            features_dict[feat] = 0  # Default
        else:
            features_dict[feat] = 0
    
    # Create feature array
    X = np.array([[features_dict[feat] for feat in fert_features]])
    
    # Scale features
    X_scaled = fert_scaler.transform(X)
    
    # Predict
    fertilizer_name = fert_model.predict(X_scaled)[0]
    
    # Get confidence
    probabilities = fert_model.predict_proba(X_scaled)[0]
    classes = fert_model.classes_
    predicted_idx = np.where(classes == fertilizer_name)[0][0]
    confidence = float(probabilities[predicted_idx])
    
    # Calculate application rate based on NPK levels
    total_npk = n_level + p_level + k_level
    if total_npk < 100:
        application_rate = 225.0  # High (200-250 kg/ha)
        rate_description = "High (200-250 kg/ha)"
    elif total_npk < 200:
        application_rate = 125.0  # Medium (100-150 kg/ha)
        rate_description = "Medium (100-150 kg/ha)"
    else:
        application_rate = 75.0   # Low (50-100 kg/ha)
        rate_description = "Low (50-100 kg/ha)"
    
    return {
        'fertilizer_name': str(fertilizer_name),
        'application_rate': application_rate,
        'rate_description': rate_description,
        'confidence': confidence
    }
