from AI_helper import groqValidateInput
from flask import Flask, request, render_template

from weather import get_lat_long, get_current_weather, get_forecast
from secrets_helper import get_api_key
from graph import dict_creator, graph, average_data, graph_generator
from datetime import datetime
import json
import pytz

OWM_API_KEY = get_api_key("OWM_API_KEY")

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip) # Allow use of zip() in our HTML templates
## create cache data to temporary store data also set the default value
cached_data={ # Default to San Antonio, if no GET args are provided
    'city':"San Antonio",
    'state': 'Texas',
    'country' : "United States",
    'current': None,
    'forecast': None,
    'timezone': None
}

@app.route("/")
def show_weather():
    error = None

    city = cached_data['city'] 
    state = cached_data['state'] 
    country = cached_data['country']

    if request.args.get("searchInput"): # If we have an arg for searchInput in URL...
        jsonString = groqValidateInput(request.args.get("searchInput")) # Have Groq validate it, returning results as JSON
        parsed = json.loads(jsonString) # Convert that JSON into a Python Object
        print("GROQ: jsonString =", repr(jsonString))

        if 'Error' in parsed: # If Groq returned an error...
            print("Groq returned an error while attempting to validate searchInput\n")
            error = "We could not match your input to a valid location. Please try again using city, state (if applicable), and country."
        else: # Load the results for City, State, and Country from Groq
            parsed_city = parsed['city'].title()
            parsed_state = parsed['state'].title()
            parsed_country = parsed['country'].title()
            print(f"Groq successfully validated searchInput\n"
                  f"  parsed_city: '{parsed_city}'\n" 
                  f"  parsed_sate: '{parsed_state}'\n" 
                  f"  parsed_country: '{parsed_country}'\n")

            if ( # Only update the cache data if the user's input is different
                parsed_city != cached_data['city'] or
                parsed_state != cached_data['state'] or
                parsed_country != cached_data['country']
            ):
                print("New data detected. Updating cached data...\n")
                city = cached_data['city'] = parsed_city
                state = cached_data['state'] = parsed_state
                country = cached_data['country'] = parsed_country
                cached_data['current'] = None  # Invalidate the old data
                cached_data['forecast'] = None
                print(f"Cached data updated.\n" 
                      f"  city: '{city}'\n"
                      f"  state: '{state}'\n" 
                      f"  country: '{country}'\n")
            else: # User submitted the same location, reuse existing data
                print("Using previously cached data for City/State/Country\n")
                city = cached_data['city']
                state = cached_data['state']
                country = cached_data['country']
    else:
        print("No searchInput. Using previously cached data for City/State/Country\n")

    # No errors, and no weather data yet for current City/State/Country
    if error is None and (cached_data['current'] is None or cached_data['forecast'] is None):
        print("Fetching lat/lon from City/State/Country through Open Weather Map API\n")
        lat, lon = get_lat_long(city, state, country, OWM_API_KEY) # Get lat/lon through OWM API

        if lat is None or lon is None: # If OWM API returns an error...
            print("Open Weather Map API returned 'None' for lat/lon\n")
            error = f"City not found: {city}"
        else: # Use lat/lon to get current weather and forecast from Open-Meteo API
            print("Fetching fresh weather data from Open-Meteo using Lat/Lon\n")
            cached_data['current'] = get_current_weather(lat, lon)
            cached_data['forecast'] = get_forecast(lat, lon)

            print("Converting Open-Meteo timezone response to datetime object\n")
            timezone_str = cached_data['current'].timezone
            cached_data['timezone'] = pytz.timezone(timezone_str)

    current = cached_data['current']
    forecast = cached_data['forecast']

    highTempData  = dict_creator(forecast.dates, forecast.temps_max)
    lowTempData  = dict_creator(forecast.dates, forecast.temps_min)
    avgTempData = dict_creator(forecast.dates, average_data(forecast.temps_max, forecast.temps_min))
    print(highTempData)
    print(lowTempData)
    print(avgTempData)
    graph_generator(avgTempData,highTempData,lowTempData)

    local_time = datetime.now(cached_data['timezone']).strftime("%I:%M %p") # Format as 3:00 PM

    print(f"Local time in {city}: {local_time}\n")
    
    # Render the page template (Flask uses Jinja2)

    return render_template(
      "index.html",
      city = city,
      state = state,
      country = country,
      error = error,
      current = current,
      forecast = forecast,
      local_time = local_time
    )

# Run via the Flask development server if running main.py directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
