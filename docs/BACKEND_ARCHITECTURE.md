# AgroSmart - Backend Architecture

## 🏗️ Backend Structure

This document outlines the backend architecture for the AgroSmart application.

## 📁 Directory Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (gitignored)
├── .env.example              # Environment template
│
├── api/                       # API route handlers
│   ├── __init__.py
│   ├── crop.py               # Crop prediction endpoints
│   ├── fertilizer.py         # Fertilizer recommendation endpoints
│   ├── yield_pred.py         # Yield estimation endpoints
│   └── health.py             # Health check endpoints
│
├── models/                    # ML models and prediction logic
│   ├── __init__.py
│   ├── crop_model.py         # Crop prediction model
│   ├── fertilizer_model.py   # Fertilizer recommendation logic
│   └── yield_model.py        # Yield estimation model
│
├── schemas/                   # Pydantic models for validation
│   ├── __init__.py
│   ├── requests.py           # Request schemas
│   └── responses.py          # Response schemas
│
├── utils/                     # Helper utilities
│   ├── __init__.py
│   ├── preprocessing.py      # Data preprocessing functions
│   ├── validators.py         # Custom validators
│   └── config.py             # Configuration management
│
└── tests/                     # Test files
    ├── __init__.py
    ├── test_crop.py
    ├── test_fertilizer.py
    └── test_yield.py
```

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/predict-crop` | Crop prediction |
| POST | `/recommend-fertilizer` | Fertilizer recommendation |
| POST | `/estimate-yield` | Yield estimation |
| GET | `/statistics` | Get prediction statistics (optional) |

### Swagger Documentation
Once running, visit: `http://localhost:8000/docs`

## 🔧 Technology Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Scikit-learn** - Machine learning
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

## 📦 Dependencies

See `requirements.txt` for full list:

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
```

## 🚀 Running the Backend

### Development Mode
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_crop.py
```

## 🔐 Environment Variables

Create `.env` file in backend directory:

```env
# API Configuration
API_HOST=localhost
API_PORT=8000
API_DEBUG=True

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Optional: Database (if using SQLite)
DATABASE_URL=sqlite:///./agrosmart.db

# Optional: Model paths
CROP_MODEL_PATH=models/crop_model.pkl
YIELD_MODEL_PATH=models/yield_model.pkl
```

## 📊 Prediction Logic

### 1. Crop Prediction
- **Input**: Soil type, NPK levels, climate, pH, region
- **Process**: Feature encoding → Model prediction → Confidence calculation
- **Output**: Top crop + alternatives with scores

### 2. Fertilizer Recommendation
- **Input**: Crop type, current NPK, soil properties
- **Process**: Rule-based logic + nutrient gap analysis
- **Output**: Fertilizer type, NPK ratio, quantity, timing

### 3. Yield Estimation
- **Input**: Crop, season, environmental & soil parameters
- **Process**: Feature scaling → Regression model → Confidence interval
- **Output**: Yield estimate + regional comparison

## 🎯 Model Development Approaches

### Option A: Rule-Based (Quick Start)
- Expert knowledge rules
- No training required
- Fast implementation
- Good for demo

### Option B: Machine Learning (Advanced)
- Train on real datasets
- Better predictions
- Requires data preprocessing
- More impressive results

## 📈 Performance Considerations

- **Response Time**: Target < 200ms per prediction
- **Concurrent Users**: Handle 10+ simultaneous requests
- **Model Loading**: Load models on startup, not per request
- **Caching**: Cache common predictions (optional)

## 🔍 Error Handling

All endpoints return consistent error format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "error_type": "ValidationError"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (validation error)
- `422`: Unprocessable entity
- `500`: Internal server error

## 🛡️ Security

- **CORS**: Configured for local frontend
- **Input Validation**: Pydantic models validate all inputs
- **Rate Limiting**: Not implemented (demo only)
- **Authentication**: Not required (demo only)

## 📝 Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

## 🔄 Development Workflow

1. **Write Schema** (Pydantic models)
2. **Implement Model Logic** (prediction functions)
3. **Create API Endpoint** (FastAPI route)
4. **Write Tests** (pytest)
5. **Update Documentation** (docstrings)
6. **Test Manually** (Swagger UI)

## 🎨 Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small
- Write descriptive variable names

## 📚 Next Steps

1. ✅ Create `main.py` with FastAPI app
2. ✅ Define Pydantic schemas
3. ✅ Implement prediction models
4. ✅ Create API endpoints
5. ✅ Add error handling
6. ✅ Write tests
7. ✅ Connect to frontend

## 🤝 Contributing

See main CONTRIBUTING.md for guidelines.

---

**Ready to build the backend!** 🚀
