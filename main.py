from AI_helper import groqValidateInput
from flask import Flask, request, render_template

from weather import get_lat_long, get_current_weather, get_forecast
from secrets_helper import get_api_key
from datetime import datetime
import json

OWM_API_KEY = get_api_key("OWM_API_KEY")

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) # Allow use of zip() in our HTML templates
## create cache data to temporary store data also set the default value
cached_data={ # Default to San Antonio, if no GET args are provided
    'city':"San Antonio",
    'state': 'TX',
    'country' : "United States",
    'current': None,
    'forecast': None,
}

@app.route("/")
def show_weather():
    current_date = datetime.now().strftime("%A - %B %d, %Y") # i.e., format as Monday - July 27, 2025
    error = None

    city = cached_data['city'] 
    state = cached_data['state'] 
    country = cached_data['country']
    current = cached_data['current']
    forecast = cached_data['forecast']

    if request.args.get("searchInput"): # If we have an arg for searchInput in URL...
        jsonString = groqValidateInput(request.args.get("searchInput")) # Have Groq validate it, returning results as JSON
        parsed = json.loads(jsonString) # Convert that JSON into a Python Object

        if 'Error' in parsed: # If Groq returned an error...
            # Set error to an error message
            error = "We could not match your input to a valid location. Please try again using city, state (if applicable), and country."
        else: # Load the results for City, State, and Country from Groq
            city = cached_data['city'] = parsed['city']
            state = cached_data['state'] = parsed['state']
            country = cached_data['country']= parsed["country"]
    
    if error is None: # Groq input validation was successful
        lat, lon = get_lat_long(city, state, country, OWM_API_KEY) # Get latitude and longitude of the location

        if lat is None or lon is None: # If OWM API returns an error...
            # Set error
            error = f"City not found: {city}"
        else: # Use lat/lon to get current weather and forecast from Open-Meteo API
            current = cached_data['current'] = get_current_weather(lat, lon)
            forecast = cached_data['forecast'] = get_forecast(lat, lon)
    
    # Render the page template (Flask uses Jinja2)
    return render_template(
      "index.html",
      city = city,
      state = state,
      country = country,
      error = error,
      current = current,
      forecast = forecast,
      current_date = current_date # Will swap this out later to match time at the inputted location
    )

# Run via the Flask development server if running main.py directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
