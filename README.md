# Botzy PDF
Botzy PDF is an interactive AI assistant that can answer questions based on the content of any PDF. Upload a PDF, ask questions, and get precise, context-aware responses.

## Preview
![Botzy PDF Preview](./images/preview.png "Botzy PDF")

## About
Botzy PDF is a web app built with Streamlit and the Google Gemini API. It uses a **Retrieval-Augmented Generation (RAG)** workflow to ensure the AI provides accurate answers based on your PDFs.

### How it works
1. **Upload PDF** → The content is split into chunks.
2. **Generate embeddings** → Each chunk is converted into a vector representation and stored in a vector database.
3. **User asks a question** → The app converts the question into a vector too.
4. **Retrieve relevant chunks** → The system finds the chunks most similar to the question.
5. **LLM generates answer** → The AI uses only the relevant context to provide a grounded, accurate response.

This workflow prevents AI "hallucinations" (made-up answers) and ensures that all responses are based on the actual content of the PDFs.

## Features to highlight
- Upload PDFs and get instant AI-powered answers.
- Avoids hallucinations by using RAG: only relevant chunks are used for responses.
- Interactive chat interface built with Streamlit.
- Supports multiple queries in a single session.
- Easy to extend to more document types or AI models.

## Technologies
Botzy PDF is built with:
- `Python`
- `Streamlit` for the frontend and chat interface
- `Google Generative AI (Gemini)` for LLM responses
- `PyPDF2` for PDF parsing
- `chromadb` and `sentence-transformers` for embeddings and vector database
- Custom Python utilities for text chunking and RAG workflow

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/Nilyz/llm-pdf-assistant.git
cd llm-pdf-assistant
pip install -r requirements.txt
