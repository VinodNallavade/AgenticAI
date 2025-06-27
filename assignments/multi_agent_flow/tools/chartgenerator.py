from langchain.tools import tool
from langchain_experimental.tools import PythonREPLTool
from state.agentstate import AgentState

python_repl = PythonREPLTool()

@tool
def run_python(state: AgentState) -> AgentState:
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user. Don't save to any file"""
    print("Python tool called-----")
    print(state.search_results)
    code = state.search_results
    print(code)
    if not code.strip():
        print("No Python code found in search_results.")
        return state
    try:
        result = python_repl.invoke(code)
        print("Python execution result:", result)
        state.python_output=result[0]["content"]
        return state
    except Exception as e:
        print("Python execution failed:", e)
        return state  # Return state unchanged on failure