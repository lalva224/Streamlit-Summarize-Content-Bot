import streamlit as st
from groq import Groq
import os


client = Groq(
    # This is the default and can be omitted
    api_key=st.secrets["GROQ_API_KEY"],
)
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
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model="llama-3.3-70b-versatile",
)
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        add_context({'namespace':'hello'})
    st.session_state.messages.append({"role": "assistant", "content": response})