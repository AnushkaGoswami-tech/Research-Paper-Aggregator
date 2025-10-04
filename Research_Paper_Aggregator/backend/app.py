import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from services.arxiv_client import search_arxiv
from services.summarizer import summarize_text
from services.pdf_utils import extract_text_from_pdf_url

app = Flask(
    __name__,
    static_folder="../frontend",       # serve the simple frontend directly
    static_url_path=""
)
CORS(app)

# ---------- Health ----------
@app.get("/api/health")
def health():
    return jsonify({"status": "ok"}), 200

# ---------- Search papers (arXiv) ----------
@app.get("/api/search")
def api_search():
    query = request.args.get("query", "").strip()
    max_results = int(request.args.get("max_results", 20))
    if not query:
        return jsonify({"error": "Missing ?query= parameter"}), 400
    try:
        results = search_arxiv(query, max_results=max_results)
        return jsonify({"query": query, "count": len(results), "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Summarize raw text ----------
@app.post("/api/summarize")
def api_summarize():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    sentences = int(data.get("sentences", 6))
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        summary = summarize_text(text, max_sentences=sentences)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Summarize a PDF by URL (e.g., arXiv PDF) ----------
@app.post("/api/summarize_url")
def api_summarize_url():
    data = request.get_json(silent=True) or {}
    pdf_url = data.get("pdf_url", "").strip()
    sentences = int(data.get("sentences", 7))
    max_pages = int(data.get("max_pages", 4))
    if not pdf_url:
        return jsonify({"error": "No pdf_url provided"}), 400
    try:
        text = extract_text_from_pdf_url(pdf_url, max_pages=max_pages)
        if not text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 422
        summary = summarize_text(text, max_sentences=sentences)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Serve frontend ----------
@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    # Use a fixed port and host so the instructions below work verbatim
    app.run(host="127.0.0.1", port=8000, debug=False)
