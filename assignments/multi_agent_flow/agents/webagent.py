from utils.azure_models import chat_model
from tools.websearch import web_search
from utils.prompts import make_system_prompt
from langgraph.prebuilt import create_react_agent

web_agent = create_react_agent(
    chat_model,
    tools=[web_search],
    prompt=make_system_prompt(
        "You can only do research. You are working with a chart generator colleague."
    ),
)