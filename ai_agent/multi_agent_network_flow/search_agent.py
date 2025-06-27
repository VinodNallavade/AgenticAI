from langchain_community.tools import DuckDuckGoSearchRun,tavily_search
from langgraph.prebuilt import create_react_agent
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from typing import Literal
from langgraph.graph import END
from prompt import make_system_prompt
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

tavily_key = os.getenv("TAVILY_APIKEY")

token_provider = get_bearer_token_provider(DefaultAzureCredential(),"https://cognitiveservices.azure.com/.default")
model= AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    model= "gpt-4o-mini"
)

# Create the agent
memory = MemorySaver()
# Use the agent
#config = {"configurable": {"thread_id": "abc123"}}


search_tool = tavily_search.TavilySearchResults(max_results =3 , tavily_api_key=tavily_key)

@tool
def duckduck_search_tool(input: str) -> str:
    """ This tool will help to fecth data from internet"""
    print("in search tool")
    search_tool = DuckDuckGoSearchRun(max_results =2)
    result = search_tool.invoke(input)
    result_str = f"data collected from internet :  {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )


search_agent = create_react_agent(
    model, 
    [search_tool],
    #checkpointer=memory,
    prompt="You are a research-only agent. When you find data, output it and say **handover to chart agent**."
    )

def search_node(state: AgentState) -> Command[Literal["chart_node", END]]:
    print(f"in search node state : {state}")
    result= search_agent.invoke(state) 
    print(result)       
    if "FINAL MESSAGE" in result["messages"][-1].content:
        return Command(goto=END,update={"messages" : state.messages,}) 
    elif "handover to chart agent" in result["messages"][-1].content.lower():
        state.messages[-1]=HumanMessage(
        content=result["messages"][-1].content
        )
        state.sender="search_node"
        return Command(goto="chart_node",update={"messages" : state.messages,})
    else :
        state.messages[-1]=HumanMessage(
        content=result["messages"][-1].content
        )
        state.sender="search_node"
        return Command(goto="chart_node",update={"messages" : state.messages,})
