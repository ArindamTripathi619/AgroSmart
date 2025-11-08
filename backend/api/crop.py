"""
Crop prediction API endpoint.
"""
from fastapi import APIRouter, HTTPException
from schemas.requests import CropPredictionRequest, CropPredictionResponse, AlternativeCrop
from models import predict_crop

router = APIRouter()


@router.post("/predict-crop", response_model=CropPredictionResponse)
async def predict_crop_endpoint(request: CropPredictionRequest):
    """
    Predict the most suitable crop based on soil and climate conditions.
    
    - **soil_type**: Type of soil (Black, Red, Laterite, Alluvial, Clay)
    - **n_level**: Nitrogen level in ppm (0-200)
    - **p_level**: Phosphorus level in ppm (0-100)
    - **k_level**: Potassium level in ppm (0-200)
    - **temperature**: Average temperature in Celsius
    - **humidity**: Average humidity percentage (0-100)
    - **rainfall**: Rainfall in mm
    - **ph_level**: Soil pH level (0-14)
    - **region**: Geographic region
    
    Returns the predicted crop with confidence score and alternatives.
    """
    try:
        # Call ML prediction model (only uses NPK, temp, humidity, ph, rainfall)
        predicted_crop, confidence_score, alternative_crops_list = predict_crop(
            n_level=request.n_level,
            p_level=request.p_level,
            k_level=request.k_level,
            temperature=request.temperature,
            humidity=request.humidity,
            ph_level=request.ph_level,
            rainfall=request.rainfall
        )
        
        # Format response
        alternative_crops = [
            AlternativeCrop(**crop) for crop in alternative_crops_list
        ]
        
        return CropPredictionResponse(
            predicted_crop=predicted_crop,
            confidence_score=confidence_score,
            alternative_crops=alternative_crops
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )
