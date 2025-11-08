"""
ML-based Crop Prediction Model
Uses trained RandomForest model for crop recommendations
"""
import joblib
import numpy as np
from typing import Dict, List, Tuple
import os

# Global model objects
crop_model = None
crop_scaler = None
crop_features = None

def load_models():
    """Load trained models into memory"""
    global crop_model, crop_scaler, crop_features
    
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'trained_models')
    
    crop_model = joblib.load(os.path.join(model_dir, 'crop_model.pkl'))
    crop_scaler = joblib.load(os.path.join(model_dir, 'crop_scaler.pkl'))
    crop_features = joblib.load(os.path.join(model_dir, 'crop_features.pkl'))
    
    return True

def predict_crop(
    n_level: int,
    p_level: int,
    k_level: int,
    temperature: float,
    humidity: float,
    ph_level: float,
    rainfall: float
) -> Tuple[str, float, List[Dict[str, float]]]:
    """
    Predict the most suitable crop using trained ML model.
    
    Args:
        n_level: Nitrogen content in soil (kg/ha)
        p_level: Phosphorus content in soil (kg/ha)
        k_level: Potassium content in soil (kg/ha)
        temperature: Temperature in Celsius
        humidity: Relative humidity (%)
        ph_level: Soil pH level
        rainfall: Rainfall in mm
    
    Returns:
        Tuple of (predicted_crop, confidence, alternative_crops)
    """
    global crop_model, crop_scaler, crop_features
    
    # Load models if not already loaded
    if crop_model is None:
        load_models()
    
    # Prepare input features in correct order
    # Expected order: ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    features = {
        'N': n_level,
        'P': p_level,
        'K': k_level,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph_level,
        'rainfall': rainfall
    }
    
    # Create feature array in the same order as training
    X = np.array([[features[feat] for feat in crop_features]])
    
    # Scale features
    X_scaled = crop_scaler.transform(X)
    
    # Get prediction and probabilities
    predicted_crop = crop_model.predict(X_scaled)[0]
    probabilities = crop_model.predict_proba(X_scaled)[0]
    
    # Get class names
    classes = crop_model.classes_
    
    # Get confidence for predicted crop
    predicted_idx = np.where(classes == predicted_crop)[0][0]
    confidence = float(probabilities[predicted_idx])
    
    # Get top 3 alternative crops
    top_indices = np.argsort(probabilities)[-4:][::-1]  # Top 4 (including predicted)
    alternatives = []
    
    for idx in top_indices[1:]:  # Skip first one (it's the prediction)
        alternatives.append({
            'crop': str(classes[idx]),
            'score': float(probabilities[idx])  # Changed from 'probability' to 'score'
        })
    
    return predicted_crop, confidence, alternatives
