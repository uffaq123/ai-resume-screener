import re
from pathlib import Path
from pypdf import PdfReader
import docx


def extract_text_from_pdf(file_path_or_bytes) -> str:
    reader = PdfReader(file_path_or_bytes)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def extract_text_from_docx(file_path_or_bytes) -> str:
    doc = docx.Document(file_path_or_bytes)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def clean_text(raw_text: str) -> str:
    text = re.sub(r"\s+", " ", raw_text)
    return text.strip()


def extract_resume_text(uploaded_file, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        raw = extract_text_from_pdf(uploaded_file)
    elif ext == ".docx":
        raw = extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")
    return clean_text(raw)