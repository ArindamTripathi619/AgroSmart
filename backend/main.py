"""
AgroSmart Backend API
FastAPI application for agricultural predictions and recommendations.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api import crop_router, fertilizer_router, yield_router, health_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AgroSmart API",
    description="""
    🌾 **AgroSmart Agricultural Intelligence API**
    
    Provides ML-powered predictions and recommendations for:
    - Crop selection based on soil and climate
    - Fertilizer recommendations
    - Yield estimation
    
    Built with FastAPI and powered by agricultural domain knowledge.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "AgroSmart Team",
        "email": "info@agrosmart.com"
    },
    license_info={
        "name": "Educational Use",
    }
)

# CORS middleware - allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Exception handler for validation errors
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "status_code": 400,
            "error_type": "ValidationError"
        }
    )


# Exception handler for generic errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred",
            "status_code": 500,
            "error_type": "ServerError"
        }
    )


# Include routers
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(crop_router, prefix="/api", tags=["Crop Prediction"])
app.include_router(fertilizer_router, prefix="/api", tags=["Fertilizer"])
app.include_router(yield_router, prefix="/api", tags=["Yield Estimation"])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to AgroSmart API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "crop_prediction": "/api/predict-crop",
            "fertilizer_recommendation": "/api/recommend-fertilizer",
            "yield_estimation": "/api/estimate-yield"
        }
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("🌾 AgroSmart API starting up...")
    logger.info("📊 Loading ML prediction models...")
    
    # Initialize ML models
    try:
        from models import initialize_models
        success = initialize_models()
        if success:
            logger.info("✅ All ML models loaded successfully!")
        else:
            logger.warning("⚠️  Some models failed to load, check configuration")
    except Exception as e:
        logger.error(f"❌ Failed to load ML models: {e}")
        logger.info("📝 Will use fallback logic if available")
    
    logger.info("✅ API ready to serve predictions!")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("👋 AgroSmart API shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )
