# AuraWeather: Full-Stack Weather Dashboard & ML Analytics Hub

AuraWeather is a full-stack meteorological web application featuring real-time weather tracking, 365-day historical data exports, and a machine learning intelligence hub powered by Scikit-Learn and Flask.

---

## 🌟 Key Features

- **Live Weather Dashboard (`index.html`)**: Search any location to view current meteorological metrics (temperature, humidity, wind speed, pressure, visibility) and 5-day forecasts.
- **Dynamic Unit Toggle**: Instantly switch between Celsius (°C) and Fahrenheit (°F).
- **In-Memory CSV Export**: Download a clean 365-day historical weather dataset directly to your browser's download folder using an in-memory `io.BytesIO` buffer (zero local file clutter).
- **ML Analytics Hub (`forecast_hub.html`)**: Visualize 30-day seasonal weather trends using Scikit-Learn Ordinary Least Squares (OLS) Linear Regression with trigonometric seasonal encoding ($\sin/\cos$) to accurately forecast approaching seasonal changes (such as winter cooling trends).
- **Production-Ready WSGI**: Configured to run on Windows using the Waitress WSGI server, bypassing Flask development server warnings.

---

## 📂 Project Structure

```text
WeatherApp/
│
├── app.py                 # Main Flask server application routes
├── ml_model.py            # Scikit-Learn seasonal regression prediction engine
├── get_location.py        # OSM Nominatim geocoding module
├── weather_forecast.py    # NWS Weather.gov & Open-Meteo API integration
├── wsgi.py                # Production WSGI server runner (Waitress)
├── requirements.txt       # Python package dependencies
│
└── templates/
    ├── index.html         # Main weather dashboard frontend
    └── forecast_hub.html  # ML analytics and regression chart hub
```

---

## 🚀 Getting Started & Installation

### 1. Clone or Open the Repository
Ensure all project files are placed in your working directory.

### 2. Install Dependencies
Install the required Python packages (`Flask`, `requests`, `pandas`, `scikit-learn`, `waitress`):
```bash
pip install flask requests pandas scikit-learn waitress
```

### 3. Run the Application in Production Mode
Start the production WSGI server using Waitress:
```bash
python wsgi.py
```

### 4. Access the Website
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🛠️ API & Data Sources

- **Geocoding**: [OpenStreetMap Nominatim API](https://nominatim.openstreetmap.org)
- **Current Forecasts**: [National Weather Service (NWS) API](https://www.weather.gov)
- **Historical Archive**: [Open-Meteo Archive API](https://open-meteo.com)
- **Machine Learning**: `scikit-learn` Linear Regression with cyclical time encoding (`day_of_year` transformed via sine/cosine waves).

---

## 🚀 Deployment

To deploy this app live on cloud hosts like **Render** or **Railway**:
1. Ensure your `requirements.txt` is generated (`pip freeze > requirements.txt`).
2. Add a `Procfile` containing:
   ```text
   web: python wsgi.py
   ```
3. Connect your GitHub repository to your cloud hosting platform of choice.