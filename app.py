from flask import Flask, jsonify, render_template, request, send_file
import get_location as get_location
import weather_forecast as weather_forecast
import os

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
  
  # 1. Get coordinates for the requested city
  lat, lon, display_name = get_location.get_coordinates(city_name)
  
  # 2. Define filename based on city
  safe_city_name = city_name.lower().replace(" ", "_")
  filename = f"{safe_city_name}_weather_1_year.csv"
  
  # 3. Call your function to fetch and build the clean CSV file
  weather_forecast.download_1_year_weather_csv(
      lat=lat, 
      lon=lon, 
      start_date=weather_forecast.start_date, 
      end_date=weather_forecast.end_date, 
      filename=filename
  )
  
  # 4. Check if file exists and send it as an attachment download
  if os.path.exists(filename):
    return send_file(filename, as_attachment=True)
  else:
    return jsonify({"success": False, "error": "Could not generate CSV file."}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)