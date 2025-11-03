import streamlit as st
import google.generativeai as genai
from utils.pdf_utils import extract_text_from_pdf
from utils.text_utils import chunk_text
from utils.rag_utils import create_embeddings_and_store



# Gemini API Key configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("AI Chatbot with PDFs")
st.caption("Upload a PDF and ask questions based on its content.")

if "history" not in st.session_state:
    st.session_state["history"] = []


# File uploader
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        create_embeddings_and_store(chunks, uploaded_file.name)
    st.success("PDF processed and ready to use.")

