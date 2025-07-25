from src.graph.agent import TravelAgent
from utils import get_azure_openai_model

def main():
    llm = get_azure_openai_model()
    agent = TravelAgent(llm)
    compiledgraph = agent.build_graph().compile()

    response=compiledgraph.invoke({"messages" : "What is the weather in Pune?"})
    for m in response["messages"]:
      m.pretty_print()

if __name__ == "__main__":
    main()
