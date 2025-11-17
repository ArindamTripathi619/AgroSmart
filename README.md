# 🌾 AgroSmart - Smart Agriculture Prediction System

![React](https://img.shields.io/badge/React-18.3.1-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

**AgroSmart** is an AI-powered agricultural decision support system that helps farmers make informed decisions about crop selection, fertilizer application, and yield estimation based on soil composition, climate conditions, and environmental factors.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Usage Guide](#-usage-guide)
- [Model Information](#-model-information)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🌱 Crop Prediction
- Recommends optimal crops based on:
  - Soil type (Black, Red, Laterite, Alluvial, Clay)
  - NPK levels (Nitrogen, Phosphorus, Potassium)
  - Climate conditions (Temperature, Humidity, Rainfall)
  - Soil pH level
  - Geographic region
- Provides confidence scores and alternative crop suggestions

### 💧 Fertilizer Recommendation
- Personalized fertilizer suggestions including:
  - NPK ratio requirements
  - Recommended fertilizer types (Urea, DAP, SSP, MOP)
  - Application timing and quantity
  - Crop-specific guidance and notes

### 📈 Yield Estimation
- Predicts harvest yield based on:
  - Crop type and growing season
  - Environmental parameters
  - Soil nutrient levels
- Provides:
  - Estimated yield with confidence intervals
  - Comparison with regional averages
  - Optimal yield benchmarks

### 📊 Analytics Dashboard
- Real-time statistics and insights
- Prediction history tracking
- Visual data representation with charts
- Performance metrics

---

## 🛠️ Tech Stack

### Frontend
- **React 18.3.1** - UI library
- **TypeScript 5.5.3** - Type safety
- **Vite 5.4.2** - Build tool and dev server
- **TailwindCSS 3.4.1** - Styling framework
- **Framer Motion 12.23.24** - Animations
- **Recharts 3.3.0** - Data visualization
- **React Router DOM 7.9.5** - Routing
- **Lucide React** - Icons

### Backend (To be implemented)
- **Python 3.9+** - Programming language
- **FastAPI** - Web framework
- **Scikit-learn** - Machine learning
- **Pandas & NumPy** - Data processing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Database (Optional for Demo)
- **SQLite** - Local database for prediction history
- Alternative: No persistence (in-memory only)

---

## 📁 Project Structure

```
AgroSmart/
├── backend/                    # Python backend (to be created)
│   ├── main.py                # FastAPI application entry
│   ├── requirements.txt       # Python dependencies
│   ├── api/                   # API endpoints
│   │   ├── crop.py           # Crop prediction endpoint
│   │   ├── fertilizer.py     # Fertilizer recommendation
│   │   └── yield_pred.py     # Yield estimation
│   ├── models/               # ML models and logic
│   │   ├── crop_model.py     # Crop prediction logic
│   │   ├── fertilizer_model.py
│   │   └── yield_model.py
│   ├── schemas/              # Pydantic schemas
│   │   └── requests.py       # Request/Response models
│   └── utils/                # Helper functions
│       ├── preprocessing.py
│       └── validators.py
│
├── src/                       # Frontend React application
│   ├── components/           # Reusable UI components
│   │   ├── Layout.tsx        # App layout wrapper
│   │   ├── Navigation.tsx    # Navigation bar
│   │   └── ui/              # UI component library
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── FormField.tsx
│   │       └── LoadingSpinner.tsx
│   ├── pages/                # Page components
│   │   ├── Home.tsx          # Landing page
│   │   ├── CropPrediction.tsx
│   │   ├── FertilizerRecommendation.tsx
│   │   ├── YieldEstimation.tsx
│   │   ├── Dashboard.tsx
│   │   └── About.tsx
│   ├── services/             # API service layer (to be created)
│   │   └── api.ts           # API client functions
│   ├── context/              # React contexts
│   │   └── ThemeContext.tsx  # Dark/Light mode
│   ├── App.tsx               # Main app component
│   ├── main.tsx             # React entry point
│   └── index.css            # Global styles
│
├── public/                   # Static assets
├── .env                      # Environment variables
├── package.json             # Node dependencies
├── tsconfig.json            # TypeScript config
├── tailwind.config.js       # Tailwind configuration
├── vite.config.ts          # Vite configuration
└── README.md               # This file
```

---

## 📋 Prerequisites

### Required Software
- **Node.js** 18.x or higher
- **npm** or **yarn** package manager
- **Python** 3.9 or higher (for backend)
- **pip** package manager

### Optional
- **Git** for version control
- **VS Code** or any code editor

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/arindxm/AgroSmart.git
cd AgroSmart
```

### 2. Frontend Setup
```bash
# Install Node.js dependencies
npm install

# Create environment file
cp .env.example .env
```

### 3. Backend Setup (Coming Next)
```bash
# Create backend directory
mkdir backend
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies (after requirements.txt is created)
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Development Mode

#### Terminal 1: Start Frontend
```bash
# From project root directory
npm run dev
```
Frontend will run on: **http://localhost:5173**

#### Terminal 2: Start Backend (After Setup)
```bash
# From backend directory
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```
Backend API will run on: **http://localhost:8000**

#### Terminal 3: View API Documentation
Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Build
```bash
# Build frontend for production
npm run build

# Preview production build
npm run preview
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. Crop Prediction
**POST** `/api/predict-crop`

**Request Body:**
```json
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

**Response:**
```json
{
  "predicted_crop": "Rice",
  "confidence_score": 94.5,
  "alternative_crops": [
    {"crop": "Wheat", "score": 89.2},
    {"crop": "Maize", "score": 85.1}
  ]
}
```

#### 2. Fertilizer Recommendation
**POST** `/api/recommend-fertilizer`

**Request Body:**
```json
{
  "crop_type": "Rice",
  "current_n": 50,
  "current_p": 30,
  "current_k": 40,
  "soil_ph": 7,
  "soil_type": "Alluvial Soil"
}
```

**Response:**
```json
{
  "recommended_fertilizer": "Urea + DAP",
  "npk_ratio": {"n": 120, "p": 60, "k": 40},
  "quantity_per_hectare": 220,
  "application_timing": "Two split applications - 50% at planting, 50% at tillering",
  "notes": "Apply with adequate water. Avoid excess nitrogen in waterlogged conditions."
}
```

#### 3. Yield Estimation
**POST** `/api/estimate-yield`

**Request Body:**
```json
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

**Response:**
```json
{
  "estimated_yield": 5.2,
  "confidence_interval": {"lower": 4.8, "upper": 5.6},
  "regional_average": 4.9,
  "optimal_yield": 6.5
}
```

---

## 📖 Usage Guide

### 1. Crop Prediction
1. Navigate to **Crop Prediction** page
2. Select your soil type from dropdown
3. Adjust NPK levels using sliders
4. Enter temperature, humidity, rainfall, and pH
5. Select your region
6. Click **Predict Crop**
7. View results with confidence scores and alternatives

### 2. Fertilizer Recommendation
1. Go to **Fertilizer Recommendation** page
2. Select your crop type
3. Set current NPK levels
4. Enter soil pH and type
5. Click **Get Recommendation**
6. Review NPK ratios, quantities, and application timing

### 3. Yield Estimation
1. Visit **Yield Estimation** page
2. Choose crop type and season
3. Input environmental parameters
4. Set soil conditions
5. Click **Estimate Yield**
6. Compare your estimate with regional averages

### 4. Dashboard
- View total prediction statistics
- Analyze top predicted crops
- Track confidence score trends
- Visualize prediction distribution

---

## 🤖 Model Information

### Crop Prediction Model
- **Algorithm**: Random Forest Classifier (to be implemented)
- **Features**: 8 input features (soil type, NPK, climate, pH, region)
- **Output**: Crop recommendation with confidence score
- **Training Data**: Agricultural datasets from Kaggle

### Fertilizer Recommendation
- **Approach**: Rule-based system + ML (hybrid)
- **Features**: Crop type, current NPK, soil properties
- **Output**: Fertilizer type, NPK ratio, quantity, timing

### Yield Estimation Model
- **Algorithm**: Gradient Boosting Regressor (to be implemented)
- **Features**: 10+ environmental and soil parameters
- **Output**: Yield prediction with confidence interval

---

## 🎯 Current Status

### ✅ Completed
- [x] Frontend UI/UX design
- [x] React component architecture
- [x] Responsive design with dark mode
- [x] Navigation and routing
- [x] Form inputs with validation
- [x] Data visualization components
- [x] Animation and transitions

### 🔄 In Progress
- [ ] Backend API development
- [ ] ML model implementation
- [ ] API integration
- [ ] Database setup (optional)

### 📝 Todo
- [ ] Model training and optimization
- [ ] Error handling improvements
- [ ] Unit and integration tests
- [ ] Performance optimization
- [ ] Documentation completion

---

## 🐛 Troubleshooting

### Frontend Issues

**Port already in use:**
```bash
# Kill process on port 5173
kill -9 $(lsof -ti:5173)
# Or use a different port
npm run dev -- --port 3000
```

**Dependencies not installing:**
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Backend Issues (After Setup)

**CORS errors:**
- Ensure backend has CORS middleware configured
- Check frontend API URL matches backend URL

**Module not found:**
```bash
# Reinstall Python dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 🤝 Contributing

This is a demonstration project. For educational purposes only.

---

## 📄 License

This project is created for educational and demonstration purposes.

---

## 👥 Team

**AgroSmart** is developed as part of agricultural technology initiatives to support sustainable farming practices.

---

## 📧 Contact

For questions or feedback:
- **Email**: devcrewx@gmail.com
- **GitHub**: [ArindamTripathi619/AgroSmart](https://github.com/ArindamTripathi619/AgroSmart)

---

## 🙏 Acknowledgments

- Agricultural datasets from Kaggle
- Open-source community
- React and TypeScript communities
- Tailwind CSS team

---

**Made with ❤️ for sustainable agriculture**
