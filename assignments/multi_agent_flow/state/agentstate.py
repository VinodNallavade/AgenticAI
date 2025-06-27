from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from typing import Annotated,Sequence,Optional
import operator

class AgentState(BaseModel):
    messages:Annotated[Sequence[BaseMessage],operator.add]
    search_results: Optional[str] = None
    python_output: Optional[str] = None