# state/agent_state.py

from typing import Dict, Optional, List
from pydantic import BaseModel

class AgentState(BaseModel):
    user_input: Optional[str] = None
    location: Optional[str] = None  # e.g., "Paris"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    attractions: List[str] = []
    restaurants: List[str] = []
    activities: List[str] = []
    transportation: List[str] = []
    
    current_weather: Optional[str] = None
    weather_forecast: Optional[str] = None

    hotels: List[str] = []
    hotel_cost_estimate: Optional[float] = None
    budget_range: Optional[str] = None

    total_cost: Optional[float] = None
    daily_budget: Optional[float] = None

    exchange_rate: Optional[float] = None
    converted_budget: Optional[float] = None

    itinerary: List[str] = []
    summary: Optional[str] = None
    final_plan: Optional[str] = None
