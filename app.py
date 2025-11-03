import streamlit as st
import google.generativeai as genai

# Gemini API Key configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("AI Chatbot with PDFs")
st.caption("Upload a PDF and ask questions based on its content.")

if "history" not in st.session_state:
    st.session_state["history"] = []




