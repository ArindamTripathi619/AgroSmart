"""
Fertilizer recommendation API endpoint.
"""
from fastapi import APIRouter, HTTPException
from schemas.requests import FertilizerRequest, FertilizerResponse, NPKRatio
from models import recommend_fertilizer

router = APIRouter()


@router.post("/recommend-fertilizer", response_model=FertilizerResponse)
async def recommend_fertilizer_endpoint(request: FertilizerRequest):
    """
    Recommend fertilizer based on crop type and current soil nutrient levels.
    
    - **crop_type**: Type of crop to be grown
    - **current_n**: Current nitrogen level in ppm (0-200)
    - **current_p**: Current phosphorus level in ppm (0-100)
    - **current_k**: Current potassium level in ppm (0-200)
    - **soil_ph**: Soil pH level (0-14)
    - **soil_type**: Type of soil
    
    Returns fertilizer recommendation with NPK ratio, quantity, and application timing.
    """
    try:
        # Call ML recommendation model
        result = recommend_fertilizer(
            soil_type=request.soil_type,
            crop_type=request.crop_type,
            n_level=request.current_n,
            p_level=request.current_p,
            k_level=request.current_k,
            temperature=25.0,  # Default temperature
            humidity=70.0,     # Default humidity
            moisture=50.0      # Default moisture
        )
        
        # Extract fertilizer name and application rate
        fertilizer_name = result['fertilizer_name']
        application_rate = result['application_rate']
        
        # Create default NPK ratio based on fertilizer type
        npk_ratio = NPKRatio(n=0, p=0, k=0)
        if 'urea' in fertilizer_name.lower():
            npk_ratio = NPKRatio(n=46, p=0, k=0)
        elif 'dap' in fertilizer_name.lower():
            npk_ratio = NPKRatio(n=18, p=46, k=0)
        elif 'mop' in fertilizer_name.lower() or 'potash' in fertilizer_name.lower():
            npk_ratio = NPKRatio(n=0, p=0, k=60)
        else:
            npk_ratio = NPKRatio(n=10, p=10, k=10)
        
        # Format response
        return FertilizerResponse(
            recommended_fertilizer=fertilizer_name,
            npk_ratio=npk_ratio,
            quantity_per_hectare=application_rate,
            application_timing="Apply at planting and during growth stages",
            notes=f"Recommendation based on ML model (confidence: {result.get('confidence', 1.0):.2%})"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation error: {str(e)}"
        )
