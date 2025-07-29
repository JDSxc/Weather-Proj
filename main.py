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
cached_data={
    'city':"San Antonio",
    'state': 'TX',
    'country' : "United States",
    'current': None,
    'forecast': None,
}

@app.route("/")
def show_weather():
    current_date = datetime.now().strftime("%A - %B %d, %Y") # i.e., format as Monday - July 27, 2025
    # Default to San Antonio, if no GET args are provided, ok i might need to figure out how to work around this one
    """
    city = cached_data['city'] = request.args.get("city", "San Antonio").title() # Normalize capitalization
    state= cached_data['state'] = request.args.get("state", "TX").upper()
    country =cached_data['country'] = request.args.get("country", "United States").title() 
    """
    city = cached_data['city'] 
    state = cached_data['state'] 
    country = cached_data['country']

    
    if request.args.get("searchInput") is None:
        True
    else:
        print(request.args.get("searchInput"))
        jsonString = groqValidateInput(request.args.get("searchInput"))
        parsed = json.loads(jsonString)
        if 'Error' in parsed:
            print(parsed)
            return render_template(
                "index.html",
                city = cached_data['city'],
                state = cached_data['state'],
                country = cached_data['country'],
                error = "We could not match your input to a real location. Please try again using city, states or/and country",
                current = cached_data['current'],
                forecast = cached_data['forecast'],
                current_date = current_date
            )
        
        city = cached_data['city'] = parsed['city']
        state = cached_data['state'] = parsed['state']
        country = cached_data['country']= parsed["country"]
    
    lat, lon = get_lat_long(city, state, country, OWM_API_KEY)


    # This checks if lat or lon is returned based on city name input (Assuming state and country are always valid).
    if lat is None or lon is None:
        return render_template(
                "index.html",
                city = city,
                state = state,
                country = country,
                error = f"City not found: {city}",
                current = None,
                forecast = None,
                current_date = current_date
        )

    current = cached_data['current'] = get_current_weather(lat, lon)
    forecast = cached_data['forecast'] = get_forecast(lat, lon)

    
    # Render the page template (Flask uses Jinja2)
    return render_template(
      "index.html",
      city = city,
      state = state,
      country = country,
      error = None,
      current = current,
      forecast = forecast,
      current_date = current_date
    )

# Run via the Flask development server if running main.py directly
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
