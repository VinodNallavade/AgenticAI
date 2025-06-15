from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph,MessagesState,START,END
from langgraph.prebuilt import ToolNode,tools_condition
from IPython.display import display,Image


token_provider= get_bearer_token_provider(DefaultAzureCredential(),"https://cognitiveservices.azure.com/.default")
chatmodel = AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    model= "gpt-4o-mini"
)

## Custom Tools
@tool
def multipy(a:int,b:int)-> int:
    """ 
    Multiply two integers
    
    Args :
      a : first arg of Interger Type
      b : second arg of Interger Type

    Return :
        Return product as integer 
    """
    return a*b

@tool
def add(a:int,b:int)-> int:
    """ 
    sum two integers
    
    Args :
      a : first arg of Interger Type
      b : second arg of Interger Type

    Return :
        Return sum as integer 
    """
    return a+b

@tool
def divide(a: int, b: int) -> float:
    """
    Divide two integers.

    Args:
        a (int): The numerator.
        b (int): The denominator (must not be 0).

    Returns:
        float: The result of division.
    """
    if b == 0:
        raise ValueError("Denominator cannot be zero.")
    return a / b


## Pre-Built Tools
def websearch(input:str)->str:
    """ Help to search internet"""
    search= DuckDuckGoSearchRun()
    return search.invoke(input)


tools= [multipy,add,divide,websearch]
llm_with_tools = chatmodel.bind_tools(tools)

def llm_decision_step(state:MessagesState) -> MessagesState:
    input = state["messages"]
    response = llm_with_tools.invoke(input)
    state['messages']=response
    return state

graphbuilder = StateGraph(MessagesState)

graphbuilder.add_node("llm_decision_step",llm_decision_step)
graphbuilder.add_node("tools",ToolNode(tools))


graphbuilder.add_edge(START,"llm_decision_step")

graphbuilder.add_conditional_edges("llm_decision_step",tools_condition)
graphbuilder.add_edge("tools","llm_decision_step")


compiledgraph= graphbuilder.compile()


for output in compiledgraph.stream({"messages" : "what is the current age of TATA Group? And Multiply it with 15"}):
    for key,value in output.items():
        print(f"here is output from {key}")
        print("_______")
        print(value)
        print("\n")