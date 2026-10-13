import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def get_30_day_forecast(df: pd.DataFrame):
    # 1. Standardize column names
    df = df.rename(
        columns={
            "time": "date",
            "temperature_2m (°C)": "temperature",
            "relative_humidity_2m (%)": "humidity",
            "precipitation (mm)": "precipitation",
            "wind_speed_10m (km/h)": "wind_speed",
        }
    )

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 2. Resample to daily averages
    df.set_index("date", inplace=True)
    df = (
        df.resample("D")
        .agg({
            "temperature": "mean",
            "humidity": "mean",
            "precipitation": "sum",
            "wind_speed": "mean",
        })
        .reset_index()
    )

    df = df.dropna(
        subset=["temperature", "humidity", "precipitation", "wind_speed"]
    )

    # 3. Add seasonal sine/cosine wave encoding
    df["day_of_year"] = df["date"].dt.dayofyear
    df["sin_day"] = np.sin(2 * np.pi * df["day_of_year"] / 365.25)
    df["cos_day"] = np.cos(2 * np.pi * df["day_of_year"] / 365.25)

    feature_cols = ["humidity", "precipitation", "wind_speed", "sin_day", "cos_day"]
    X = df[feature_cols]
    y = df["temperature"]

    # 4. Train Linear Regression
    model = LinearRegression()
    model.fit(X, y)

    # Compute metrics for the Hub display
    r2 = model.score(X, y)

    # 5. Generate future 30 days
    last_row = df.iloc[-1]
    last_date = last_row["date"]
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 31)]
    future_df = pd.DataFrame({"date": future_dates})

    future_df["humidity"] = last_row["humidity"]
    future_df["precipitation"] = last_row["precipitation"]
    future_df["wind_speed"] = last_row["wind_speed"]
    future_df["sin_day"] = np.sin(
        2 * np.pi * future_df["date"].dt.dayofyear / 365.25
    )
    future_df["cos_day"] = np.cos(
        2 * np.pi * future_df["date"].dt.dayofyear / 365.25
    )

    future_preds_c = model.predict(future_df[feature_cols])

    # Compile results into a clean dictionary list
    forecast_list = []
    for d, temp_c in zip(future_dates, future_preds_c):
        temp_f = temp_c * 9 / 5 + 32
        forecast_list.append({
            "date": d.strftime("%Y-%m-%d"),
            "temp_c": round(float(temp_c), 1),
            "temp_f": round(float(temp_f), 1),
        })

    avg_next_month_c = sum(future_preds_c) / len(future_preds_c)
    avg_next_month_f = avg_next_month_c * 9 / 5 + 32

    return {
        "success": True,
        "r2_score": round(float(r2), 3),
        "predicted_avg_c": round(float(avg_next_month_c), 1),
        "predicted_avg_f": round(float(avg_next_month_f), 1),
        "forecast": forecast_list,
    }