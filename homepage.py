import streamlit as st
from groq import Groq
import os
from lib.pinecone import perform_rag



st.title("Multimodal context answer engine")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = perform_rag(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})