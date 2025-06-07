# framework from langchain
# Used primarily created for AI Flow

from IPython.display import Image,display
from langgraph.graph import Graph


def greet(state: str) -> str:
    name = state.get("name", "Guest")
    print(f"👋 Hello, {name}!")
    state["greeted"] = True
    return state

# Step 2: Goodbye
def goodbye(state: str) -> str:
    print("👋 Goodbye! Have a great day.")
    state["done"] = True
    return state

# Build the graph using `Graph` instead of `StateGraph`
graph = Graph()

graph.add_node(node="greet", action=greet)
graph.add_node(node="goodbye", action=goodbye)

# Define entry and transitions manually
graph.set_entry_point("greet")
graph.add_edge("greet", "goodbye")
graph.set_finish_point("goodbye")

# Compile and run the graph
compiledgraph = graph.compile()


display(Image(data=compiledgraph.get_graph().draw_mermaid_png()))