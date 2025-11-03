from PyPDF2 import PdfReader

# Extract text from PDF and return as a single string

def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()
