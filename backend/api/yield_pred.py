"""
Yield estimation API endpoint.
"""
from fastapi import APIRouter, HTTPException
from schemas.requests import YieldRequest, YieldResponse, ConfidenceInterval
from models import estimate_yield

router = APIRouter()


@router.post("/estimate-yield", response_model=YieldResponse)
async def estimate_yield_endpoint(request: YieldRequest):
    """
    Estimate crop yield based on environmental and soil parameters.
    
    - **crop_type**: Type of crop
    - **season**: Growing season (Kharif, Rabi, Zaid)
    - **temperature**: Average temperature in Celsius
    - **humidity**: Average humidity percentage (0-100)
    - **rainfall**: Total rainfall in mm
    - **soil_type**: Type of soil
    - **soil_ph**: Soil pH level (0-14)
    - **n_level**: Nitrogen level in ppm (0-200)
    - **p_level**: Phosphorus level in ppm (0-100)
    - **k_level**: Potassium level in ppm (0-200)
    
    Returns yield estimation with confidence interval and regional comparison.
    """
    try:
        # Call ML estimation model (it only needs specific parameters)
        estimated_yield_kg_ha = estimate_yield(
            crop_type=request.crop_type,
            area_hectares=request.area_hectares,
            season=request.season,
            rainfall=request.rainfall,
            temperature=request.temperature,
            fertilizer_used=float(request.n_level + request.p_level + request.k_level)
        )
        
        # Calculate confidence interval (±10%)
        lower = estimated_yield_kg_ha * 0.9
        upper = estimated_yield_kg_ha * 1.1
        
        # Regional average (85% of estimated)
        regional_avg = estimated_yield_kg_ha * 0.85
        
        # Optimal yield (120% of estimated)
        optimal = estimated_yield_kg_ha * 1.2
        
        # Format response
        return YieldResponse(
            estimated_yield=estimated_yield_kg_ha,
            confidence_interval=ConfidenceInterval(lower=lower, upper=upper),
            regional_average=regional_avg,
            optimal_yield=optimal
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Estimation error: {str(e)}"
        )
