from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found")

client = genai.Client(api_key=api_key)

def get_weather(city:str):
    """Fethes the current weather for the given city using API
    
    args:
    city(str): city name(eg. Dehradun)
    
    return:
    dict: weather details in JSON format"""
    
    try:
        api_key=os.getenv("OPEN_WEATHER_API_KEY")
        url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response =requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}

def temperature_of_city(city:str):
    system_instructions = """
        You are given weather data in JSON format from the OpenWeather API.
        Your job is to convert it into a clear, human-friendly weather update.  
        
        Guidelines:
        1. Always mention the city and country.
        2. Convert temperature from Kelvin to Celsius (°C), rounded to 1 decimal.
        3. Include: current temperature, feels-like temperature, main weather description,
            humidity, wind speed, and sunrise/sunset times (converted from UNIX timestamp).
        4. Use natural, conversational language.
        5. Based on the current conditions, suggest what the person should carry or wear.
            - If rain/clouds: suggest umbrella/raincoat.
            - If very hot (>30°C): suggest light cotton clothes, sunglasses, stay hydrated.
            - If cold (<15°C): suggest warm clothes, jacket.
            - If windy: suggest windbreaker, secure loose items.
            - If humid: suggest breathable clothes, water bottle.
        6. If any field is missing, gracefully ignore it.
        
        """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents =f"Generate a clear, friendly weather report with temperatures in °C, humidity, wind, sunrise/sunset for the {city} and practical suggestions on what to wear or carry.",
        config = types.GenerateContentConfig(system_instruction=system_instructions,tools=[get_weather])

    )
    return(response.candidates[0].content.parts[0].text)
