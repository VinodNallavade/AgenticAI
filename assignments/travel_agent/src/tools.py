from langchain_core.tools import tool
from amadeus import Client, ResponseError
import logging
from typing import List, Dict
import os
from dotenv import load_dotenv


load_dotenv()
# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
api_key=os.getenv("AMADEUS_CLIENT_ID")
api_secret=os.getenv("AMADEUS_CLIENT_SECRET")
client = Client(client_id=api_key, client_secret=api_secret)







@tool(return_direct=True)
def get_city_attractions(city: str) -> str:
        """
        Fetches tourist attractions for a city using Amadeus API.

        Args:
            city (str): City name

        Returns:
            str: A list of top attractions
        """
        try:
            location_data = client.reference_data.locations.get(
                keyword=city,
                subType="CITY"
            )
            geo = location_data.data[0]["geoCode"]
            lat, lon = geo["latitude"], geo["longitude"]
            print(lat)
            print(lon)
        except Exception as e:
            logger.error(f"Geo lookup failed for {city}: {e}")
            return f"Could not get location for {city}."

        try:
            response = client.shopping.activities.get(latitude=lat, longitude=lon, radius=20)
            activities = response.data[:5]
            if not activities:
                return f"No attractions found for {city}."
            return "\n".join(f"- {a['name']} ({a.get('category', 'N/A')})" for a in activities)
        except ResponseError as e:
            logger.error(f"Attraction lookup failed: {e}")
            return "Error fetching attractions."


