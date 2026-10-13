from flask import Flask, jsonify, render_template, request, send_file
import get_location as get_location
import weather_forecast as weather_forecast
import ml_model
import io
import os
import pandas as pd


app = Flask(__name__)


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/api/get-weather", methods=["GET"])
def get_weather_api():
  user_input = request.args.get("city", "New York").strip()
  lat, lon, display_name = get_location.get_coordinates(user_input)
  weather_data, error_msg = weather_forecast.get_weather_forecast(lat, lon)

  return jsonify({
      "success": True,
      "city": weather_data["city"],
      "state": weather_data["state"],
      "displayName": display_name,
      "periods": weather_data["periods"],
  })


@app.route("/api/download-csv", methods=["GET"])
def download_csv_api():
  city_name = request.args.get("city", "New York").strip()

  # 1. Get coordinates
  lat, lon, display_name = get_location.get_coordinates(city_name)

  # 2. Get the clean CSV text directly from your function
  csv_data = weather_forecast.get_clean_weather_csv(
      lat=lat,
      lon=lon,
      start_date=weather_forecast.start_date,
      end_date=weather_forecast.end_date,
  )

  if not csv_data:
    return (
        jsonify({"success": False, "error": "Could not generate CSV data."}),
        500,
    )

  # 3. Convert string to a bytes stream in memory
  csv_buffer = io.BytesIO(csv_data.encode("utf-8"))

  # 4. Define download filename
  safe_city_name = city_name.lower().replace(" ", "_")
  filename = f"{safe_city_name}_weather_1_year.csv"

  # 5. Send directly to user's download folder without saving to project directory
  return send_file(
      csv_buffer,
      mimetype="text/csv",
      as_attachment=True,
      download_name=filename,
  )

@app.route("/forecast-hub")
def forecast_hub():
  # Grab city from query parameter, default to "New York"
  city = request.args.get("city", "New York").strip()
  return render_template("forecast_hub.html", default_city=city)


@app.route("/api/ml-forecast", methods=["GET"])
def ml_forecast_api():
  city_name = request.args.get("city", "New York").strip()

  # 1. Get coordinates for the requested city
  lat, lon, display_name = get_location.get_coordinates(city_name)

  # 2. Get the DataFrame directly from weather_forecast in memory
  df = weather_forecast.get_1_year_dataframe(
      lat=lat,
      lon=lon,
      start_date=weather_forecast.start_date,
      end_date=weather_forecast.end_date,
  )

  if df is None or df.empty:
    return (
        jsonify({
            "success": False,
            "error": f"Could not fetch weather dataframe for {city_name}.",
        }),
        500,
    )

  try:
    # 3. Pass the DataFrame into ml_model and return predictions
    result = ml_model.get_30_day_forecast(df)
    return jsonify(result)
  except Exception as e:
    return (
        jsonify({
            "success": False,
            "error": f"Could not run ML model: {str(e)}",
        }),
        500,
    )