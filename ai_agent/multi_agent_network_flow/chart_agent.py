from langchain_experimental.tools import PythonREPLTool
from langgraph.prebuilt import create_react_agent
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from state import AgentState
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from typing import Literal
from langgraph.graph import END
from prompt import make_system_prompt

token_provider = get_bearer_token_provider(DefaultAzureCredential(),"https://cognitiveservices.azure.com/.default")
model= AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    model= "gpt-4o-mini"
)

# Create the agent
#memory = MemorySaver()

@tool
def python_run_tool(code: str) -> str:
    """ This tool will help to excute the python code and print the chart"""
    print("in code tool")
    code_tool = PythonREPLTool()
    result = code_tool.run(code)
    result_str = f"Successfully executed: python\n{code}\n\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )

code_agent = create_react_agent(
    model=model,
    #checkpointer=memory,
    tools=[python_run_tool],
    prompt="You are a code agent who generates a chart. When done, reply with 'chart complete'."
    )

def chart_node(state: AgentState) -> Command[Literal["search_agent_node",END]]:
    print("in chart node")
    result= code_agent.invoke(state)    
    if "FINAL MESSAGE" in result["messages"][-1].content:
        return Command(goto=END,update={"messages" : state.messages,})
    elif "chart complete" in result["messages"][-1].content.lower():
        return Command(goto=END,update={"messages" : state.messages,})
    state.messages[-1]=HumanMessage(
        content=result["messages"][-1].content
    )
    state.sender="chart_node"       
    return Command(goto="search_agent_node",update={"messages" : state.messages,})
