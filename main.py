from flask import Flask, request, render_template

from weather import get_lat_long, get_current_weather, get_forecast
from secrets_helper import get_api_key
from datetime import datetime

API_KEY = get_api_key()

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) # Allow use of zip() in our HTML templates

@app.route("/")
def show_weather():
    # Default to San Antonio, if no GET args are provided
    city = request.args.get("city", "San Antonio").title() # Normalize capitalization
    state = request.args.get("state", "TX").upper()
    country = request.args.get("country", "United States").title() 

    lat, lon = get_lat_long(city, state, country, API_KEY)

    current_date = datetime.now().strftime("%A - %B %d, %Y") # i.e., format as Monday - July 27, 2025

    # This checks if lat or lon is returned based on city name input (Assuming state and country are always valid).
    if lat is None or lon is None:
        return render_template(
                "index.html",
                city=city,
                state=state,
                country=country,
                error=f"City not found: {city}",
                current=None,
                forecast=None,
                current_date=current_date
        )

    current = get_current_weather(lat, lon)
    forecast = get_forecast(lat, lon)

    # Render the page template (Flask uses Jinja2)
    return render_template(
      "index.html",
      city=city,
      state=state,
      country=country,
      error=None,
      current=current,
      forecast=forecast,
      current_date=current_date
    )

# Run via the Flask development server if running main.py directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
