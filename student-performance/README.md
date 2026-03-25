# Student Performance Predictor v2

A modern full-stack application for predicting student academic performance using machine learning.

## Overview

This is an upgraded version of the basic Flask ML application, featuring:
- **Modern React Frontend** with Tailwind CSS
- **REST API Backend** with Flask
- **User-Selectable Features** for prediction
- **Responsive Glass-Morphism UI**

## Project Structure

```
student-performance/
├── api/                    # Flask REST API
│   ├── app.py             # Main application
│   ├── config.py           # Configuration
│   ├── routes/            # API endpoints
│   │   ├── features.py    # Feature endpoints
│   │   └── predict.py     # Prediction endpoints
│   └── ml/                # ML module
│       ├── features.py    # Feature definitions
│       └── model.py       # Model wrapper
├── frontend/              # React frontend (Vite)
│   ├── src/
│   │   ├── components/    # React components
│   │   └── services/      # API service
│   └── package.json
├── models/                # ML models
├── data/                  # Dataset
├── notebooks/            # EDA notebooks
├── requirements.txt
└── README.md
```

## Quick Start

### Backend Setup

1. Create virtual environment:
```bash
cd student-performance
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API server:
```bash
cd api
python app.py
```

The API will be available at: http://localhost:5000

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at: http://localhost:3000

## API Endpoints

### Health Check
```
GET /api/health
```

### Features
```
GET /api/features           # All features with metadata
GET /api/features/numeric   # Only numeric features
GET /api/features/categorical  # Only categorical features
GET /api/features/defaults  # Default feature selection
```

### Predictions
```
POST /api/predict
Content-Type: application/json

{
    "features": {
        "studytime": 2,
        "failures": 0,
        "absences": 3
    },
    "selected_features": ["studytime", "failures", "absences"]
}
```

### Response Format
```json
{
    "success": true,
    "data": {
        "prediction": 12.5,
        "confidence": 0.85,
        "min_score": 0,
        "max_score": 20,
        "unit": "grade (0-20)"
    }
}
```

## Features

The system supports 32 features for prediction:

### Numeric Features
- age, Medu, Fedu, traveltime, studytime, failures
- famrel, freetime, goout, Dalc, Walc, health, absences
- G1, G2

### Categorical Features
- school (GP/MS), sex (F/M), address (U/R), famsize (GT3/LE3)
- Pstatus (T/A), Mjob, Fjob, reason, guardian
- schoolsup, famsup, paid, activities, nursery, higher, internet, romantic

## Model

The application uses a Random Forest Regressor trained on student performance data to predict final grades (G3) on a scale of 0-20.

## Development

### Running Both Servers

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd student-performance
venv\Scripts\activate
cd api
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd student-performance\frontend
npm install
npm run dev
```

### Environment Variables

Create `.env` files as needed:

**Backend (api/.env):**
```
FLASK_ENV=development
PORT=5000
```

**Frontend (frontend/.env):**
```
VITE_API_URL=/api
```

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS, scikit-learn, pandas
- **Frontend:** React 18, Vite, Tailwind CSS, Axios
- **ML:** scikit-learn, Random Forest Regressor

## License

MIT License
