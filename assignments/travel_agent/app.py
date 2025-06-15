import streamlit as st
from agent import TravelAgent
from utils import get_azure_openai_model

st.set_page_config(page_title="LangGraph Travel Assistant", layout="centered")
st.title("🌍 Travel Agent Powered by Azure OpenAI and Amadeus APIs")

user_input = st.text_input("Ask a travel question:")

if user_input:
    with st.spinner("Thinking..."):
        llm = get_azure_openai_model()
        agent = TravelAgent(llm)
        graph = agent.build_graph().compile()

        st.subheader("🤖 Response")
        response=graph.invoke({"messages" : [user_input]})
        st.info(response["messages"][-1].content)
