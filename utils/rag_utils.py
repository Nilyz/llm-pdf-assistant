import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import streamlit as st
from google import genai


# Take the API key from Streamlit secrets and initialize Gemini client
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vector_store")
collection = chroma_client.get_or_create_collection("pdf_docs")

# Initialize local embedder
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Create local embeddings for each chunk and store them in Chroma.
def create_embeddings_and_store(chunks, file_name):

    for i, chunk in enumerate(chunks):
        emb = embedder.encode(chunk).tolist()
        collection.add(
            ids=[f"{file_name}_{i}"],
            embeddings=[emb],
            documents=[chunk]
        )
