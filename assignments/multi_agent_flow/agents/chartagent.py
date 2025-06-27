from utils.azure_models import chat_model
from tools import chartgenerator
from utils.prompts import make_system_prompt
from langgraph.prebuilt import create_react_agent

chart_agent = create_react_agent(
    chat_model,
    tools=[chartgenerator.run_python],
    prompt=make_system_prompt(
        "You can only generate charts, For the given python code. You are working with a researcher colleague."
    ),
)