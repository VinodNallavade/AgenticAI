from langchain_core.tools import tool
from amadeus import Client, ResponseError
import logging
from typing import List, Dict
import os,pyowm
from dotenv import load_dotenv
from langchain.utilities import OpenWeatherMapAPIWrapper
from state.agent_state import AgentState 

load_dotenv()
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
api_key=os.getenv("AMADEUS_CLIENT_ID")
api_secret=os.getenv("AMADEUS_CLIENT_SECRET")
client = Client(client_id=api_key, client_secret=api_secret)


class openweathermap_custom_wrapper:

    def __init__(self):
        pass


    def get_city_weather(state:AgentState) ->  AgentState:
        """ Given a city this tool will get whether details using openweathermap"""
        print("get_city_weather Tool Called....")
        try:
            weather_tool = OpenWeatherMapAPIWrapper()
            weather_data =weather_tool.run(state.location)
            return weather_data
        except Exception as e:
            logger.error(f"Failed to fetch weather report from OpenWeatherMap for : {state.location}: {e}")
            return f"Could not get weather report for {state.location}."
