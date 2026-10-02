
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime fog",
    51: "Light drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Light snow",
    80: "Rain showers",
    95: "Thunderstorm",
}


def get_weather(city):
    # Find the city's latitude and longitude
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={"name": city, "count": 1, "language": "en"},
        timeout=10,
    )
    geo_response.raise_for_status()

    locations = geo_response.json().get("results", [])
    if not locations:
        return None

    place = locations[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Fetch current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,weather_code,wind_speed_10m"
            ),
            "timezone": "auto",
        },
        timeout=10,
    )
    weather_response.raise_for_status()

    current = weather_response.json()["current"]

    return {
        "city": place["name"],
        "country": place.get("country", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "condition": WEATHER_CODES.get(
            current["weather_code"], "Other conditions"
        ),
        "observed_at": current["time"],
    }


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #edf4ff;
            text-align: center;
            padding: 35px 12px;
        }
        .card {
            max-width: 440px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 20px #ccd6e5;
        }
        input, button {
            padding: 12px;
            margin: 6px;
            border-radius: 7px;
            border: 1px solid #bbb;
        }
        button {
            background: #1769e0;
            color: white;
            cursor: pointer;
        }
        .weather {
            text-align: left;
            line-height: 1.9;
            margin-top: 20px;
        }
        .error { color: #c62828; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Today's Time & Weather</h1>
        <p><b>Current Time (India):</b> {{ current_time }}</p>

        <form method="POST">
            <input name="city" placeholder="Enter city, e.g. Pune"
                   value="{{ city }}" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if weather %}
        <div class="weather">
            <h2>{{ weather.city }}, {{ weather.country }}</h2>
            <p>🌡️ Temperature: {{ weather.temperature }} °C</p>
            <p>🤗 Feels like: {{ weather.feels_like }} °C</p>
            <p>☁️ Condition: {{ weather.condition }}</p>
            <p>💧 Humidity: {{ weather.humidity }}%</p>
            <p>💨 Wind speed: {{ weather.wind }} km/h</p>
            <p>🕒 Weather observation: {{ weather.observed_at }}</p>
        </div>
        {% endif %}

        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if city:
            try:
                weather = get_weather(city)
                if weather is None:
                    error = "City not found. Please try another name."
            except requests.RequestException:
                app.logger.exception("Weather API request failed")
                error = "Weather service is unavailable. Try again later."
            except (KeyError, ValueError):
                app.logger.exception("Unexpected weather API response")
                error = "Could not process weather data."

    current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%d-%m-%Y %I:%M:%S %p")

    return render_template_string(
        HTML,
        current_time=current_time,
        city=city,
        weather=weather,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)