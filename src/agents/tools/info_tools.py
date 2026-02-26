import httpx
from typing import Dict, Any

def get_weather(city: str) -> Dict[str, Any]:
    """Retrieves the current weather report for a specified city using Open-Meteo API.

    Args:
        city (str): The name of the city (e.g., "Jakarta", "London", "Tokyo").

    Returns:
        dict: Geographic and weather information including status and report message.
    """
    try:
        # Step 1: Geocoding (get lat/lon for the city)
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        
        with httpx.Client() as client:
            geo_response = client.get(geocode_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                return {"status": "error", "error_message": f"City '{city}' not found."}
                
            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]
            
            # Step 2: Get weather data
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto"
            
            weather_response = client.get(weather_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            current = weather_data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            humidity = current.get("relative_humidity_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")
            
            report = f"The current weather in {city_name} is {temp}°C with {humidity}% humidity and wind speed of {wind} km/h."
            
            return {
                "status": "success",
                "report": report
            }
            
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to retrieve weather: {str(e)}"}


def get_country_info(country_name: str) -> Dict[str, Any]:
    """Retrieves basic information about a country using RestCountries API.

    Args:
        country_name (str): The name of the country.

    Returns:
        dict: A dictionary containing the country information (capital, region, population).
    """
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
        with httpx.Client() as client:
            response = client.get(url)
            if response.status_code == 404:
                 return {"status": "error", "error_message": f"Country '{country_name}' not found. Please try a different name (e.g., 'United States' or 'Japan')."}
            response.raise_for_status()
            
            data = response.json()[0]
            capital = data.get("capital", ["Unknown"])[0]
            region = data.get("region", "Unknown")
            population = data.get("population", "Unknown")
            
            report = f"Country: {data['name']['common']}, Capital: {capital}, Region: {region}, Population: {population:,}."
            return {"status": "success", "report": report}
    except Exception as e:
         return {"status": "error", "error_message": f"Failed to retrieve country info: {str(e)}"}


def get_exchange_rate(base_currency: str, target_currency: str) -> Dict[str, Any]:
    """Retrieves the current exchange rate between two currencies using open.er-api.com.

    Args:
        base_currency (str): The 3-letter currency code to convert from (e.g., 'USD').
        target_currency (str): The 3-letter currency code to convert to (e.g., 'EUR', 'IDR').

    Returns:
        dict: Exchange rate information.
    """
    base = base_currency.upper()
    target = target_currency.upper()
    try:
        # Using a free, no-key required endpoint for exchange rates
        url = f"https://open.er-api.com/v6/latest/{base}"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("result") != "success":
                return {"status": "error", "error_message": "Failed to fetch exchange rates."}
                
            rates = data.get("rates", {})
            if target not in rates:
                return {"status": "error", "error_message": f"Target currency '{target}' not found."}
                
            rate = rates[target]
            report = f"The current exchange rate is 1 {base} = {rate} {target}."
            return {"status": "success", "report": report}
    except Exception as e:
         return {"status": "error", "error_message": f"Failed to retrieve exchange rate: {str(e)}"}


def get_joke() -> Dict[str, Any]:
    """Retrieves a random programming or general joke.

    Returns:
        dict: A dictionary containing the joke setup and punchline.
    """
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            
            report = f"{data['setup']} ... {data['punchline']}"
            return {"status": "success", "report": report}
    except Exception as e:
         return {"status": "error", "error_message": f"Failed to retrieve joke: {str(e)}"}
