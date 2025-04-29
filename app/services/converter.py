from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


def extract_text(file_path: str) -> str: 
    ext = Path(file_path). suffix.lower()
    if ext == ".pdf":
        reader =  PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs) 
    else:
        return Path(file_path).read_text(encoding="utf-8", errors="ignore")