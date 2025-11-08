"""
Pydantic schemas for request validation and response formatting.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


# ==================== Crop Prediction Schemas ====================

class CropPredictionRequest(BaseModel):
    """Request schema for crop prediction endpoint."""
    
    soil_type: str = Field(..., description="Type of soil (e.g., 'Black Soil', 'Red Soil')")
    n_level: float = Field(..., ge=0, le=200, description="Nitrogen level in ppm")
    p_level: float = Field(..., ge=0, le=100, description="Phosphorus level in ppm")
    k_level: float = Field(..., ge=0, le=200, description="Potassium level in ppm")
    temperature: float = Field(..., ge=-10, le=60, description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    rainfall: float = Field(..., ge=0, description="Rainfall in mm")
    ph_level: float = Field(..., ge=0, le=14, description="Soil pH level")
    region: str = Field(..., description="Geographic region")
    
    @field_validator('soil_type')
    @classmethod
    def validate_soil_type(cls, v: str) -> str:
        valid_types = ['Black Soil', 'Red Soil', 'Laterite Soil', 'Alluvial Soil', 'Clay Soil']
        if v not in valid_types:
            raise ValueError(f"Soil type must be one of: {', '.join(valid_types)}")
        return v
    
    @field_validator('region')
    @classmethod
    def validate_region(cls, v: str) -> str:
        valid_regions = ['North India', 'South India', 'East India', 'West India', 'Central India']
        if v not in valid_regions:
            raise ValueError(f"Region must be one of: {', '.join(valid_regions)}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "soil_type": "Alluvial Soil",
                "n_level": 80,
                "p_level": 40,
                "k_level": 50,
                "temperature": 25,
                "humidity": 70,
                "rainfall": 100,
                "ph_level": 7,
                "region": "North India"
            }
        }


class AlternativeCrop(BaseModel):
    """Alternative crop suggestion with score."""
    crop: str
    score: float = Field(..., ge=0, le=100)


class CropPredictionResponse(BaseModel):
    """Response schema for crop prediction."""
    
    predicted_crop: str
    confidence_score: float = Field(..., ge=0, le=100)
    alternative_crops: List[AlternativeCrop]
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_crop": "Rice",
                "confidence_score": 94.5,
                "alternative_crops": [
                    {"crop": "Wheat", "score": 89.2},
                    {"crop": "Maize", "score": 85.1}
                ]
            }
        }


# ==================== Fertilizer Recommendation Schemas ====================

class FertilizerRequest(BaseModel):
    """Request schema for fertilizer recommendation endpoint."""
    
    crop_type: str = Field(..., description="Type of crop to be grown")
    current_n: float = Field(..., ge=0, le=200, description="Current nitrogen level in ppm")
    current_p: float = Field(..., ge=0, le=100, description="Current phosphorus level in ppm")
    current_k: float = Field(..., ge=0, le=200, description="Current potassium level in ppm")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH level")
    soil_type: str = Field(..., description="Type of soil")
    
    @field_validator('crop_type')
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        valid_crops = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Soybean', 
                       'Peanut', 'Coconut', 'Lentil', 'Chickpea']
        if v not in valid_crops:
            raise ValueError(f"Crop type must be one of: {', '.join(valid_crops)}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_type": "Rice",
                "current_n": 50,
                "current_p": 30,
                "current_k": 40,
                "soil_ph": 7,
                "soil_type": "Alluvial Soil"
            }
        }


class NPKRatio(BaseModel):
    """NPK ratio model."""
    n: float
    p: float
    k: float


class FertilizerResponse(BaseModel):
    """Response schema for fertilizer recommendation."""
    
    recommended_fertilizer: str
    npk_ratio: NPKRatio
    quantity_per_hectare: float = Field(..., gt=0)
    application_timing: str
    notes: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "recommended_fertilizer": "Urea + DAP",
                "npk_ratio": {"n": 120, "p": 60, "k": 40},
                "quantity_per_hectare": 220,
                "application_timing": "Two split applications - 50% at planting, 50% at tillering",
                "notes": "Apply with adequate water. Avoid excess nitrogen in waterlogged conditions."
            }
        }


# ==================== Yield Estimation Schemas ====================

class YieldRequest(BaseModel):
    """Request schema for yield estimation endpoint."""
    
    crop_type: str = Field(..., description="Type of crop")
    area_hectares: float = Field(..., ge=0.1, description="Area in hectares")
    season: str = Field(..., description="Growing season")
    temperature: float = Field(..., ge=-10, le=60, description="Average temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Average humidity percentage")
    rainfall: float = Field(..., ge=0, description="Total rainfall in mm")
    soil_type: str = Field(..., description="Type of soil")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH level")
    n_level: float = Field(..., ge=0, le=200, description="Nitrogen level in ppm")
    p_level: float = Field(..., ge=0, le=100, description="Phosphorus level in ppm")
    k_level: float = Field(..., ge=0, le=200, description="Potassium level in ppm")
    
    @field_validator('season')
    @classmethod
    def validate_season(cls, v: str) -> str:
        valid_seasons = ['Kharif', 'Rabi', 'Zaid']
        if v not in valid_seasons:
            raise ValueError(f"Season must be one of: {', '.join(valid_seasons)}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_type": "Rice",
                "season": "Kharif",
                "temperature": 25,
                "humidity": 70,
                "rainfall": 100,
                "soil_type": "Alluvial Soil",
                "soil_ph": 7,
                "n_level": 80,
                "p_level": 40,
                "k_level": 50
            }
        }


class ConfidenceInterval(BaseModel):
    """Confidence interval for yield prediction."""
    lower: float
    upper: float


class YieldResponse(BaseModel):
    """Response schema for yield estimation."""
    
    estimated_yield: float = Field(..., gt=0)
    confidence_interval: ConfidenceInterval
    regional_average: float = Field(..., gt=0)
    optimal_yield: float = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "estimated_yield": 5.2,
                "confidence_interval": {"lower": 4.8, "upper": 5.6},
                "regional_average": 4.9,
                "optimal_yield": 6.5
            }
        }


# ==================== General Schemas ====================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str
    version: str = "1.0.0"


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    status_code: int
    error_type: Optional[str] = None


class StatisticsResponse(BaseModel):
    """Statistics response (optional)."""
    total_predictions: int
    crops: int
    fertilizers: int
    yields: int
