import streamlit as st
from langchain_core.messages import HumanMessage, ToolMessage
from agent import agent_app

st.set_page_config(page_title="AI Agent Tool Calling", page_icon="🤖")
st.title("🤖 LangGraph AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Ask a question (e.g., 'What is 45 * 12?' or 'Weather in Islamabad?')")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            output = agent_app.invoke({"messages": [HumanMessage(content=user_input)]})
            
            for msg in output["messages"]:
                if isinstance(msg, ToolMessage):
                    st.info(f"🛠️ **Tool Executed ({msg.name}):** `{msg.content}`")

            final_response = output["messages"][-1].content
            st.markdown(final_response)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
