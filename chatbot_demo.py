# chatbot_demo.py
import streamlit as st
from response_engine import ResponseEngine

st.set_page_config(page_title="BSU Advisor AI Chatbot", layout="centered")
st.title("🎓 BSU Advisor AI Chatbot")
st.caption("Chat with BSU's Graduate Advisor AI. Ask about research, advisors, or anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "generator" not in st.session_state:
    st.session_state.generator = ResponseEngine()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_query := st.chat_input("Ask a question:"):
    st.chat_message("user").write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    answer = st.session_state.generator.generate_answer(user_query)
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
