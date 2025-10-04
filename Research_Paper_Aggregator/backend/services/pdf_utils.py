import io
import requests
from PyPDF2 import PdfReader

def extract_text_from_pdf_url(url: str, max_pages: int = 4) -> str:
    """
    Downloads a PDF and extracts text from the first `max_pages` pages.
    Returns plain text (best-effort).
    """
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    raw = io.BytesIO(resp.content)
    reader = PdfReader(raw)
    pages_to_read = min(max_pages, len(reader.pages))
    parts = []
    for i in range(pages_to_read):
        try:
            txt = reader.pages[i].extract_text() or ""
            parts.append(txt)
        except Exception:
            continue
    return "\n".join(parts)
