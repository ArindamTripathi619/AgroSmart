# AgroSmart Backend API

FastAPI backend for AgroSmart agricultural prediction system.

## Features

- **Crop Prediction**: Recommends suitable crops based on soil and climate
- **Fertilizer Recommendation**: Suggests optimal fertilizers and quantities
- **Yield Estimation**: Predicts harvest yield with confidence intervals

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --port 8000

# Or using Python directly
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /api/health
```

### Crop Prediction
```
POST /api/predict-crop
Content-Type: application/json

{
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
```

### Fertilizer Recommendation
```
POST /api/recommend-fertilizer
Content-Type: application/json

{
  "crop_type": "Rice",
  "current_n": 50,
  "current_p": 30,
  "current_k": 40,
  "soil_ph": 7,
  "soil_type": "Alluvial Soil"
}
```

### Yield Estimation
```
POST /api/estimate-yield
Content-Type: application/json

{
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
```

## Testing

### Using Swagger UI
1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"

### Using curl
```bash
# Health check
curl http://localhost:8000/api/health

# Crop prediction
curl -X POST http://localhost:8000/api/predict-crop \
  -H "Content-Type: application/json" \
  -d '{
    "soil_type": "Alluvial Soil",
    "n_level": 80,
    "p_level": 40,
    "k_level": 50,
    "temperature": 25,
    "humidity": 70,
    "rainfall": 100,
    "ph_level": 7,
    "region": "North India"
  }'
```

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── api/                 # API endpoints
│   ├── crop.py
│   ├── fertilizer.py
│   ├── yield_pred.py
│   └── health.py
├── models/              # Prediction models
│   ├── crop_model.py
│   ├── fertilizer_model.py
│   └── yield_model.py
├── schemas/             # Pydantic models
│   └── requests.py
└── utils/               # Utilities (if needed)
```

## Development

### Adding New Features
1. Create schema in `schemas/requests.py`
2. Implement model logic in `models/`
3. Create API endpoint in `api/`
4. Register router in `main.py`

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Write descriptive variable names

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --reload --port 8001
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Errors
Check that frontend URL is in CORS allowed origins in `main.py`

## License

Educational use only.
