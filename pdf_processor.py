from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set Poppler path
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"

def is_scanned_pdf(documents):
    total_text = " ".join([doc.page_content for doc in documents]).strip()
    return len(total_text) < 100

def ocr_pdf(pdf_path, source_file_name):
    images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    documents = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang="eng")
        if text.strip():
            documents.append(Document(
                page_content=text,
                metadata={"page": i, "source_file": source_file_name}
            ))
    return documents

def process_pdf(uploaded_file):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Try normal text extraction first
    loader = PyMuPDFLoader(tmp_path)
    documents = loader.load()

    # Add filename as metadata
    for doc in documents:
        doc.metadata["source_file"] = uploaded_file.name

    # Filter empty pages
    documents = [doc for doc in documents if doc.page_content.strip()]

    # If scanned PDF — use OCR automatically
    if is_scanned_pdf(documents):
        documents = ocr_pdf(tmp_path, uploaded_file.name)

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # Cleanup temp file
    os.unlink(tmp_path)

    return chunks


def process_multiple_pdfs(uploaded_files):
    all_chunks = []
    for uploaded_file in uploaded_files:
        chunks = process_pdf(uploaded_file)
        all_chunks.extend(chunks)
    return all_chunks