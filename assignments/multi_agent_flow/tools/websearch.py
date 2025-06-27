from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
import os
from dotenv import load_dotenv
from state.agentstate import AgentState
from utils.azure_models import chat_model
from pydantic import BaseModel

class WebSearchInput(BaseModel):
    state: AgentState

load_dotenv()
TAVILY_API_KEY=os.getenv("TAVILY_APIKEY")


@tool(args_schema=WebSearchInput)
def web_search(state: AgentState) -> AgentState:
    """Search the web using Tavily with the user's input. Details should be in the table format. So that the next tools can use it for analysis"""
    print("Web Search tool called-----")
    query = ""
    for msg in reversed(state.messages):
        if msg.type == "human":
            query = msg.content
            break
    try:
        results = TavilySearchResults(max_results=4,tavily_api_key=TAVILY_API_KEY).invoke(query)    
        state.messages[-1]= results[0]["content"]    
        state.search_results=results[0]["content"]
        return state
    except Exception as e:
        print(e)




