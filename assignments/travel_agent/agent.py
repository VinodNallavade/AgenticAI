from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import BaseMessage
from tools import multiply, get_city_attractions


class TravelAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model
        self.tools = [multiply, get_city_attractions, DuckDuckGoSearchRun()]

    def llm_node(self, state: MessagesState) -> MessagesState:
        bound_llm = self.chat_model.bind_tools(self.tools)
        response = bound_llm.invoke(state["messages"])
        state["messages"] = response
        return state

    def build_graph(self) -> StateGraph:
        graph = StateGraph(MessagesState)
        graph.add_node("llm_step", self.llm_node)
        graph.add_node("tools", ToolNode(self.tools))
        graph.add_edge(START, "llm_step")
        graph.add_conditional_edges("llm_step", tools_condition)
        graph.add_edge("tools", "llm_step")
        graph.add_edge("llm_step", END)
        return graph
