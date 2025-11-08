"""
API package initialization.
"""
from .crop import router as crop_router
from .fertilizer import router as fertilizer_router
from .yield_pred import router as yield_router
from .health import router as health_router

__all__ = [
    "crop_router",
    "fertilizer_router",
    "yield_router",
    "health_router"
]
