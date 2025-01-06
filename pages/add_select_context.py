import streamlit as st
from lib.context_db import add_context, remove_context,get_all_context,remove_all_context
from st_multimodal_chatinput import multimodal_chatinput
import time
st.session_state['current_file_name'] = ''
st.title('Add Context')
# remove_all_context()
with st.form("my-form", clear_on_submit=True):
        image_input = st.file_uploader('Upload a document or image')
        submitted = st.form_submit_button("Upload")
        if submitted and image_input is not None:
            st.success('Context added')
            add_context(image_input.read(),image_input.name)

# image_input = st.file_uploader('Upload a document or image')
# if image_input and image_input.name != st.session_state['current_file_name']:
#     print(st.session_state['current_file_name'])
#     add_context(image_input.read(),image_input.name)
#     st.success('Context added')
#     st.session_state['current_file_name'] = image_input.name
    
# uploaded_files = chatinput["uploadedFiles"] ##list of ALL uploaded files (including images) along with type, name, and content.
# uploaded_images = chatinput["uploadedImages"] ## list of base 64 encoding of uploaded images
# text = chatinput["textInput"] ##submitted text

# for file in uploaded_files:
#     filename = file["name"]
#     filetype = file["type"] ## MIME type of the uploaded file
#     filecontent = file["content"] ## base 64 encoding of the uploaded file




namespaces = get_all_context()
st.title('Select Context')
namespace = st.selectbox(
    'Select your context',
    options = namespaces,
    index=None,
    placeholder ='context namespace'
)
