from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing import Sequence, Literal,Annotated
from langchain_core.messages import BaseMessage
import operator

class AgentState(BaseModel):
    messages : Annotated[Sequence[BaseMessage],operator.add]
    sender : str

