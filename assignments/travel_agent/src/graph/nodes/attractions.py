from langchain_core.tools import tool
from amadeus import Client, ResponseError
import logging
from typing import List, Dict
import os,pyowm
from dotenv import load_dotenv
from state.agent_state import AgentState 

load_dotenv()
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
api_key=os.getenv("AMADEUS_CLIENT_ID")
api_secret=os.getenv("AMADEUS_CLIENT_SECRET")
client = Client(client_id=api_key, client_secret=api_secret)   


class AmedeusCustomWrapper:  

        @tool
        def get_city_geocodes(city: str,state: AgentState) -> AgentState :
            """ Given the city provide the lantitude and longitude details using Amadeus APIs"""
            print("get_city_geocodes Tool Called....")
            try:
                    location_data = client.reference_data.locations.get(
                        keyword=city,
                        subType="CITY"
                    )
                    geo = location_data.data[0]["geoCode"]
                    lat, lon = geo["latitude"], geo["longitude"]
                    state.latitude=lat
                    state.longitude=lon
            except Exception as e:
                    logger.error(f"Geo lookup failed for {city}: {e}")
                    return f"Could not get location for {city}."

        @tool
        def search_attractions(city: str,state: AgentState) -> AgentState :
                """
                Fetches tourist attractions for a city using Amadeus API.

                Args:
                    city (str): City name

                Returns:
                    str: A list of top attractions
                """
                print("search_attractions Tool Called....")
                try:
                    response = client.shopping.activities.get(longitude=state.latitude,latitude=state.longitude, radius=20)
                    activities = response.data[:5]
                    if not activities:
                        return f"No attractions found for {city}."
                    return "\n".join(f"- {a['name']} ({a.get('category', 'N/A')})" for a in activities)
                except ResponseError as e:
                    logger.error(f"Attraction lookup failed: {e}")
                    return "Error fetching attractions."


        @tool
        def search_restaurants(state: AgentState) -> AgentState :
            """ Given the lantitude and longitude details this tool will return hotels using Amadeus APIs"""
            print("hotels tool called...")
            hotels_data = client.reference_data.locations.hotels.by_geocode.get(longitude=state.latitude,latitude=state.longitude)
            state.hotels= hotels_data
            return state

        def search_activities(state: AgentState) -> AgentState :
            state.activities = ["Snorkeling", "City Tour"]
            return state

        def search_transportation(state: AgentState) -> AgentState :
            state.transportation = ["Bus", "Taxi", "Bike Rental"]
            return state