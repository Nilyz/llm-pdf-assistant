import streamlit as st
import google.generativeai as genai
from utils.pdf_utils import extract_text_from_pdf
from utils.text_utils import chunk_text
from utils.rag_utils import (
    create_embeddings_and_store,
    retrieve_context,
    generate_answer_gemini,
    retrieve_context_with_scores
)
import pandas as pd
import altair as alt

# Gemini API Key configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("AI Chatbot with PDFs")
st.caption("Upload a PDF and ask questions based on its content.")

# Initialize session state
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

# User query input
query = st.chat_input("Make a query about the PDF...")

if query and query.strip() != "":
    with st.spinner("Searching for answer..."):
        
        # Retrieve context and scores
        chunks, scores = retrieve_context_with_scores(query)

        # Display each chunk with score
        clean_chunks = [" ".join(c.split()) for c in chunks]
        for i, (chunk, score) in enumerate(zip(clean_chunks, scores)):
            st.markdown(f"### Chunk {i+1} — Score: {score:.2f}")
            st.markdown(f"{chunk}")
            st.divider()

        # Display similarity graph
        labels = [" ".join(c.split()[:5]) + "..." for c in clean_chunks]  # primeras 5 palabras como label
        df = pd.DataFrame({"Chunk": labels, "Similarity": scores})
        chart = alt.Chart(df).mark_bar(color="#4CAF50").encode(
            x='Chunk',
            y='Similarity',
            tooltip=['Chunk', 'Similarity']
        ).properties(width=700, height=300)
        st.altair_chart(chart)

        # Generate answer
        context = "\n".join(clean_chunks)
        answer = generate_answer_gemini(query, context, history=st.session_state["history"])

        # Update chat history
        st.session_state["history"].append({"role": "user", "content": query})
        st.session_state["history"].append({"role": "assistant", "content": answer})

# Display chat history
for msg in st.session_state["history"]:
    st.chat_message(msg["role"]).write(msg["content"])
