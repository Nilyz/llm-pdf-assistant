import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import streamlit as st
from google import genai


# Take the API key from Streamlit secrets and initialize Gemini client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"].strip())

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vector_store")
collection = chroma_client.get_or_create_collection("pdf_docs")

# Initialize local embedder
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# Create local embeddings for each chunk and store them in Chroma.
def create_embeddings_and_store(chunks, file_name):
    for i, chunk in enumerate(chunks):
        emb = embedder.encode(chunk).tolist()
        collection.add(
            ids=[f"{file_name}_{i}"],
            embeddings=[emb],
            documents=[chunk]
        )


# Retrieve relevant context using local embeddings
def retrieve_context(query, k=3):
    q_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    return "\n".join(results["documents"][0])


# Generate answer using gemini-2.5-flash model
def generate_answer_gemini(query, context, history=[]):

    # Build prompt with neutral labels
    history_text = ""
    for turn in history:
        role = turn["role"]
        content = turn["content"]
        history_text += f"{role.upper()}: {content}\n"

    prompt = f"{history_text}\nContext:\n{context}\n\nQuestion: {query}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

