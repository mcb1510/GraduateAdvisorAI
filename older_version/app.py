import streamlit as st
from older_version.data_loader import load_data, build_index
from older_version.rag_engine import retrieve_info, generate_response 

st.set_page_config(page_title="Academic Advisor AI", layout="wide")
st.title("Academic Advisor AI")
st.caption("Ask questions about university professors and their research areas."
)

@st.cache_resource
def setup():
    df = load_data()
    model, index, embeddings = build_index(df)
    return df, model, index
df, model, index = setup()

if "chat" not in st.session_state:
    st.session_state.chat = []

user_query = st.chat_input("Ask a question about university professors:")
if user_query:
    st.chat_message("user").write(user_query)
    context = retrieve_info(user_query, model, index, df)
    answer = generate_response(user_query, context)
    st.chat_message("assistant").write(answer)
    st.session_state.chat.append((user_query, answer))

for q, a in st.session_state.chat:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)