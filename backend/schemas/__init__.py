"""
Schemas package initialization.
"""
from .requests import (
    CropPredictionRequest,
    CropPredictionResponse,
    AlternativeCrop,
    FertilizerRequest,
    FertilizerResponse,
    NPKRatio,
    YieldRequest,
    YieldResponse,
    ConfidenceInterval,
    HealthResponse,
    ErrorResponse,
    StatisticsResponse
)

__all__ = [
    "CropPredictionRequest",
    "CropPredictionResponse",
    "AlternativeCrop",
    "FertilizerRequest",
    "FertilizerResponse",
    "NPKRatio",
    "YieldRequest",
    "YieldResponse",
    "ConfidenceInterval",
    "HealthResponse",
    "ErrorResponse",
    "StatisticsResponse"
]
