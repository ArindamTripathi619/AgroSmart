"""
Health check and utility endpoints.
"""
from fastapi import APIRouter
from schemas.requests import HealthResponse, StatisticsResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns server status and version information.
    """
    return HealthResponse(
        status="healthy",
        message="AgroSmart API is running successfully",
        version="1.0.0"
    )


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics():
    """
    Get prediction statistics (optional endpoint for dashboard).
    
    Note: This is a placeholder. In a real application with database,
    this would query actual prediction history.
    """
    return StatisticsResponse(
        total_predictions=0,
        crops=0,
        fertilizers=0,
        yields=0
    )
