import streamlit as st
import google.generativeai as genai
import base64
import os
from utils.pdf_utils import extract_text_from_pdf
from utils.text_utils import chunk_text
from utils.rag_utils import (
    create_embeddings_and_store,
    generate_answer_gemini,
    retrieve_context
)


# --- Función para codificar la imagen a Base64 ---
def get_base64_image(image_path):
    """Convierte una imagen local a una cadena Base64 para incrustarla en HTML/CSS."""
    try:
        if not os.path.exists(image_path):
            # No usa st.error aquí para evitar duplicar el mensaje si el logo es opcional
            return None
            
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        # Falla silenciosamente si hay un error de lectura, mostrando solo el título
        return None

# --- CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")

# --- Configure Gemini API ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- PAGE SETUP (TITLE AND FAVICON) ---
st.set_page_config(
    page_title="Botzy PDF",
    page_icon="images/botzy_logo.png", 
    layout="wide"
)

# --------------------------HEADER WITH LOGO AND TITLE (Using Base64 for compatibility)--------------------------
LOGO_PATH = "images/botzy_logo.png"
logo_base64 = get_base64_image(LOGO_PATH)

if logo_base64:
    logo_src = f"data:image/png;base64,{logo_base64}"
    
    st.markdown(
        f"""
        <div style="
            display: flex; 
            align-items: center; 
            justify-content: center; /* Centrado horizontal */
            gap: 5px;
            padding-top: 10px;
        ">
            <img class="logo-img"
                src="{logo_src}" 
                alt="Botzy Logo" 
            >
            <h1 class="app-title" style="margin: 0; font-size: 2.5rem; text-align: center;">Botzy PDF</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("<h1>Botzy PDF</h1>", unsafe_allow_html=True)

st.markdown('<p class="app-subtitle">Upload a PDF and ask questions based on its content.</p>', unsafe_allow_html=True)


# --- Initialize chat history in session state ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- File uploader ---
uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

# --- Placeholder for success message ---
success_placeholder = st.empty()

# --- Variable controlling whether to show the chat ---
show_chat = False

if uploaded_file:
    with st.spinner("Processing PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        create_embeddings_and_store(chunks, uploaded_file.name)
    
    success_placeholder.success("PDF processed and ready to use.")
    show_chat = True 

query = st.chat_input("Make a query about the PDF...")

# --- Handle user query ---
if query:
    context = retrieve_context(query)
    answer = generate_answer_gemini(query, context, history=st.session_state["history"])
    st.session_state["history"].append({"role": "user", "content": query})
    st.session_state["history"].append({"role": "assistant", "content": answer})
    show_chat = True

# --- Show chat area only if PDF uploaded or there are messages ---
if show_chat:
    chat_html = """
    <div class="chat-container">
        <h3>Chat Area</h3>
        <div class="chat-box">
    """
    if st.session_state["history"]:
        for msg in st.session_state["history"]:
            role_class = "user-msg" if msg["role"] == "user" else "assistant-msg"
            chat_html += f"<div class='{role_class}'>{msg['content']}</div>"
    else:
        chat_html += "<p style='color: #682993;'>No messages yet. Start by asking a question!</p>"

    chat_html += "</div></div>"
    st.markdown(chat_html, unsafe_allow_html=True)

