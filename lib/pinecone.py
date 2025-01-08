from .load_document import load_file
import streamlit as st
from transformers import AutoModel
import torch
from pinecone import Pinecone
from groq import Groq
from openai import OpenAI
import requests
import re

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pinecone = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pinecone.Index('summary-bot')
client = Groq(
    # This is the default and can be omitted
    api_key=st.secrets["GROQ_API_KEY"],
)

def perform_rag(query):
    context = ""
    websites = extract_urls(query)
    #if user provides websites in query, those websites are scraped, before getting embedded.
    if websites:
        website_data = ""
        for website in websites:
            website_data += f"## {website}\n"
            website_data += scrape_page(website)
            website_data += "\n\n"
        #new query is not scraped data + old query (links and non url text)
        query = website_data + "\n\n" + query
        print(query)
    if 'selected_namespace' in st.session_state:
        namespace = st.session_state['selected_namespace']
        embeddings = get_text_embeddings(query)
        result = index.query(
        namespace=namespace,
        vector=embeddings,
        top_k=5, #this is the number of results that are returned
        include_values=False,
        include_metadata=True,
        
        )
        matches = [match['metadata']['document_content'] for match in result['matches']]
        print(matches)
        context = '\n'.join(matches)
        print(context)
    else:
        print("No namespace selected")
    system_prompt = f"""
You are a helpful assistant that will answer questions based on provided context.
Context: {context}
"""
    
    chat_completion = client.chat.completions.create(
            messages=[{'role':'system','content':system_prompt}]
            +
            [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model="llama-3.3-70b-versatile",
    )
    response = chat_completion.choices[0].message.content
    return response
    
def scrape_page(website_url):
    headers = {
        'Authorization': 'Bearer ' + st.secrets["JINA_API_KEY"]
    }
    URL = f'https://r.jina.ai/https://{website_url}'
    response = requests.get(URL, headers=headers)
    return response.text

def extract_urls(query):
    url_pattern = r'(https?://[^\s]+)'
    websites = re.findall(url_pattern, query)
    return websites

def upsert_context_pinecone(file,file_name):
    document_data = load_file(file,file_name)
    chunks = split_into_chunks(document_data)
    print(chunks)
    vectors = []
    for i, chunk in enumerate(chunks):
        embeddings = get_text_embeddings(chunk)
        vector = {
            'id':f'{file_name}-{i}',
            'values':embeddings,
            'metadata':{
                'document_content':chunk
            }
        }
        vectors.append(vector)
    index.upsert(vectors=vectors,namespace=file_name)
    print(f"Context {file_name} added successfully")
    st.success(f"Context {file_name} added successfully")

def split_into_chunks(text,chunk_size=1000,overlap=100):
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def remove_context_pinecone(file_name):
    index.delete(ids=[file_name],namespace=file_name)
    print(f"Context {file_name} removed successfully")
    st.success(f"Context {file_name} removed successfully")

def get_text_embeddings(text):
    #load embedding model through cuda gpu, using torch
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
    embeddings = embedding_model.encode(text).tolist()
    #need faster embedding model
#     response = client.embeddings.create(
#     input=text,
#     model="text-embedding-3-small"
# )
    # return response.data[0].embedding
    return embeddings
def get_image_embeddings(image):
    pass

def get_embeddings(file,file_name):
    if file_name.endswith('.docx') or file_name.endswith('.pdf') or file_name.endswith('.txt'):
        return get_text_embeddings(load_file(file,file_name))
    # elif file_name.endswith('.png') or file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
    #     return get_image_embeddings(load_file(file,file_name))
    else:
        return None


