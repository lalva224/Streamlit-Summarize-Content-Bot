import streamlit as st
from lib.context_db import add_context, remove_context,get_all_context,remove_all_context
st.title('Add Context')
# remove_all_context()
with st.form("my-form", clear_on_submit=True):
        image_input = st.file_uploader('Upload a document you want saved',type=['pdf','docx','txt'])
        submitted = st.form_submit_button("Upload")
        if submitted and image_input is not None:
            # add_context(image_input.read(),image_input.name)
            add_context(image_input,image_input.name)
            

namespaces = get_all_context()
st.title('Select Context')
st.session_state['selected_namespace'] = 'None'
namespace = st.selectbox(
    'Select your context',
    options = namespaces,
    index=None,
    placeholder ='context namespace'
)

if namespace:
    st.session_state['selected_namespace'] = namespace


st.button('Remove Context',on_click=remove_context,args=[namespace])