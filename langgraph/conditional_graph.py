from langchain_openai import AzureOpenAIEmbeddings,AzureChatOpenAI
from azure.identity import DefaultAzureCredential,get_bearer_token_provider
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_chroma import Chroma 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel,Field
from typing import TypedDict,Annotated,Sequence,Literal
from langchain_core.messages import BaseMessage
import operator
from langgraph.graph import StateGraph,END
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

token_provider= get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

embeddingmodel= AzureOpenAIEmbeddings(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "text-embedding-ada-002",
    model= "text-embedding-ada-002"
)
embeddings_date=embeddingmodel.embed_query("hello")
#print(len(embeddings_date))


model= AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://azopenai-langchain.openai.azure.com/",
    azure_ad_token_provider= token_provider,
    azure_deployment= "gpt-4o-mini",
    model= "gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


###  Data into Vector DB
#Loader
loader = DirectoryLoader("./data", glob="**/*.txt", show_progress=True)
docs = loader.load()
#print(docs[0].page_content)

#Textsplitting
text_splitter=RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=10)
chunks=text_splitter.split_documents(docs)
#print(chunks)

#Store in Chroma
vector_store =Chroma("ChinaData",embedding_function=embeddingmodel)
vector_store.add_documents(chunks)
results = vector_store.similarity_search(
    "For how many years will the recruited experts serve in the think tank?",
    k=2
)
#print(results)

#Creating Pydantic Classes
class RoutingDecisionWithReason(BaseModel):
    route: Literal["LLM Call", "Rag Call"] = Field(description="Routing decision")
    reasoning: str = Field(description="Reasoning behind the routing decision")

# Parser
parser = PydanticOutputParser(pydantic_object=RoutingDecisionWithReason)

# Prompt template with partial_variables for parser instructions
supervisorprompt = PromptTemplate(
    template=(
        "Given the user input below, decide the appropriate routing for processing. If the quetion is based on Focus then go for RAG call\n"
        "Respond in JSON format matching the schema.\n\n"
        "{format_instructions}\n\n"
        "User input: {user_input}"
    ),
    input_variables=["user_input"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

#State management class
class AgentState(TypedDict):
    messages:Annotated[Sequence[BaseMessage],operator.add]
    route_decision: RoutingDecisionWithReason

# Adding Functions for LangGraph
def Supervisor(state: AgentState):
    question = state["messages"][-1]
    chain = supervisorprompt | model | parser
    response = chain.invoke({"user_input":question})
    print(f"🚦 Routing Decision: {response.route}")
    print(f"💡 Reasoning: {response.reasoning}")
    state["route_decision"] =response.route
    return state


def ragcall(state: AgentState):
    print("Rag called")
    return state

def llmcall(state: AgentState):
    print("LLM called")
    return state

def router(state: AgentState):
    print(state)
    return state["route_decision"]


workflow=StateGraph(AgentState)

workflow.add_node("Supervisor",Supervisor)
workflow.add_node("CALL RAG",ragcall)
workflow.add_node("CALL LLM",llmcall)

workflow.set_entry_point("Supervisor")
workflow.add_conditional_edges(
        "Supervisor",
         router,
         {
             "Rag Call" : "CALL RAG",
             "LLM Call" : "CALL LLM"

         }
)

workflow.add_edge("CALL RAG",END)
workflow.add_edge("CALL LLM",END)

app = workflow.compile()
initial_state = {"messages": ["Why do we need Focus."]}
final_state = app.invoke(initial_state)
