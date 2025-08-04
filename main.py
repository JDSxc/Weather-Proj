from AI_helper import groqValidateInput
from flask import Flask, request, render_template,send_file

from weather import get_lat_long, get_current_weather, get_forecast
from secrets_helper import get_api_key
from graph import dict_creator, average_data, graph_generator, celsius_dict
from weather_code_info import weather_code_desc
import json
import time

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
    t0_total = time.perf_counter()

    error = None

    city = cached_data['city'] 
    state = cached_data['state'] 
    country = cached_data['country']

    if request.args.get("searchInput"): # If we have an arg for searchInput in URL...
        t0 = time.perf_counter()
        jsonString = groqValidateInput(request.args.get("searchInput")) # Have Groq validate it, returning results as JSON
        t1 = time.perf_counter()
        print(f"Input validation took {(t1 - t0) * 1000:.2f} ms")

        print("Groq response (raw): " + jsonString)
        parsed = json.loads(jsonString) # Convert that JSON into a Python Object
        print("Groq response (parsed) " + repr(jsonString) + "\n")

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
        print("Fetching lat/lon from City/State/Country through Open Weather Map API")

        t0 = time.perf_counter()
        lat, lon = get_lat_long(city, state, country, OWM_API_KEY) # Get lat/lon through OWM API
        t1 = time.perf_counter()
        print(f"  Lat/Lon lookup took {(t1 - t0) * 1000:.2f} ms\n")

        if lat is None or lon is None: # If OWM API returns an error...
            print("Open Weather Map API returned 'None' for lat/lon\n")
            error = f"City not found: {city}"
        else: # Use lat/lon to get current weather and forecast from Open-Meteo API
            print("Fetching fresh weather data from Open-Meteo using Lat/Lon")

            t0 = time.perf_counter()
            cached_data['current'] = get_current_weather(lat, lon)
            t1 = time.perf_counter()
            print(f"  Current weather fetch took {(t1 - t0) * 1000:.2f} ms")

            cached_data['forecast'] = get_forecast(lat, lon)
            t1 = time.perf_counter()
            print(f"  Forecast fetch took {(t1 - t0) * 1000:.2f} ms\n")

            #print("Converting Open-Meteo timezone response to datetime object\n")
            
            #timezone_str = cached_data['current'].timezone
            cached_data['timezone'] = cached_data['current'].timezone
            #cached_data['timezone'] = pytz.timezone(timezone_str)

    current = cached_data['current']
    forecast = cached_data['forecast']


    highTempData  = dict_creator(forecast.dates, forecast.temps_max)
    lowTempData  = dict_creator(forecast.dates, forecast.temps_min)
    avgTempData = dict_creator(forecast.dates, average_data(forecast.temps_max, forecast.temps_min))
    print(f"High Temps: {highTempData}")
    print(f"Low Temps:  {lowTempData}")
    print(f"Avg Temps:  {avgTempData}\n")

    t0 = time.perf_counter()
    graph_generator(avgTempData, highTempData, lowTempData, "F")
    t1 = time.perf_counter()
    print(f"  F graph took {(t1-t0)*1000:.2f} ms")
    
    t0 = time.perf_counter()
    graph_generator(
        celsius_dict(avgTempData),
        celsius_dict(highTempData),
        celsius_dict(lowTempData),
        "C"
    )
    t1 = time.perf_counter()
    print(f"  C graph took {(t1-t0)*1000:.2f} ms\n")

    #graph_generator_interactive(avgTempData,highTempData,lowTempData)

    #local_time = datetime.now(cached_data['timezone']).strftime("%I:%M %p") # Format as 3:00 PM
    local_time = cached_data['timezone']
    print(f"Timezone: {cached_data['timezone']}\n")
    # print(f"Local time in {city}: {local_time}\n")
    
    t1_total = time.perf_counter()
    print(f"show_weather() took {(t1_total - t0_total) * 1000:.2f} ms\n")

    # Render the page template (Flask uses Jinja2)
    return render_template(
      "index.html",
      city = city,
      state = state,
      country = country,
      error = error,
      current = current,
      forecast = forecast,
      local_time = local_time,
      img_code = list(weather_code_desc.keys())[list(weather_code_desc.values()).index(current.description)]
    )


@app.route("/graph_f")
def serve_graph_F():
    return send_file("/tmp/graph/graph_F.png", mimetype="image/png")
@app.route("/graph_c")
def serve_graph_C():
    return send_file("/tmp/graph/graph_C.png", mimetype="image/png")

# Run via the Flask development server if running main.py directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

