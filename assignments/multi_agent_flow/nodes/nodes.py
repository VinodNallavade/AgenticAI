from state.agentstate import AgentState
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END
from typing import Literal
from agents.webagent import web_agent
from agents.chartagent import chart_agent
from langgraph.types import Command

def get_next_node(last_message: BaseMessage, goto: str):
    if "FINAL ANSWER" in last_message.content:
        # Any agent decided the work is done
        return END
    return goto


def research_node(
    state: AgentState,
) -> Command[Literal["chart_generator", END]]:
    print("research_node called ......")
    result = web_agent.invoke({"state": state})
    goto = get_next_node(result, "chart_generator")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result.messages[-1] = HumanMessage(
        content=result.messages[-1].content, name="researcher"
    )
    return Command(
        update={
            # share internal message history of research agent with other agents
            "messages": result.messages,
             "search_results": result.search_results,      # preserve output
            "python_output": result.python_output          # even if None
        },
        goto=goto,
    )

def chart_node(state: AgentState) -> Command[Literal["researcher", END]]:
    print("chart node called.....")
    result = chart_agent.invoke({"state": state})
    goto = get_next_node(result["messages"][-1], "researcher")
    # wrap in a human message, as not all providers allow
    # AI message at the last position of the input messages list
    result["messages"][-1] = HumanMessage(
        content=result["messages"][-1].content, name="chart_generator"
    )
    return Command(
        update={
            # share internal message history of chart agent with other agents
            "messages": result["messages"],
            "python_output": result.python_output          # even if None
        },
        goto=goto,
    )