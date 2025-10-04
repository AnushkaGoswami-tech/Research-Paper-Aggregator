# backend/services/arxiv_client.py

import urllib.parse
import requests
import feedparser
from datetime import datetime
import re

ARXIV_API = "https://export.arxiv.org/api/query"


def _parse_entry(entry):
    """Convert a feedparser entry into a dict we use in the app."""
    authors = [a.name for a in getattr(entry, "authors", [])]

    pdf_url, landing = None, None
    for link in entry.links:
        if getattr(link, "rel", None) == "alternate":
            landing = link.href
        if getattr(link, "type", None) == "application/pdf":
            pdf_url = link.href

    published = None
    if hasattr(entry, "published"):
        try:
            published = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ").isoformat()
        except Exception:
            published = entry.published

    return {
        "id": entry.id,
        "title": entry.title.strip().replace("\n", " "),
        "summary": entry.summary.strip(),
        "authors": authors,
        "published": published,
        "link": landing or entry.id,
        "pdf_url": pdf_url,
    }


def _is_advanced(q: str) -> bool:
    """Detect if the user already used arXiv operators; if so, pass-through."""
    ql = q.lower()
    return any(tok in ql for tok in ["ti:", "abs:", "au:", "cat:", " and ", " or ", "(", ")", '"'])


def _normalize(s: str) -> str:
    """Normalize strings for comparison (lowercase + collapse spaces)."""
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def _build_search_query(user_query: str) -> str:
    """
    Build arXiv API query.
    - If advanced syntax: pass through
    - Else: restrict to title search only (ti:)
    """
    q = (user_query or "").strip()
    if not q:
        return "all:__none__"

    if _is_advanced(q):
        return q

    phrase = q.replace('"', '\\"')
    return f'ti:"{phrase}"'   # 👈 Title-only search


def search_arxiv(query: str, max_results: int = 20):
    """
    Call arXiv's Atom API and return parsed results.
    """
    arxiv_q = _build_search_query(query)

    params = {
        "search_query": arxiv_q,
        "start": 0,
        "max_results": max(1, min(int(max_results), 50)),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    print("DEBUG: Querying arXiv URL:", url)  # 👈 for debugging in backend logs

    r = requests.get(url, timeout=20)
    r.raise_for_status()

    feed = feedparser.parse(r.text)
    items = [_parse_entry(e) for e in feed.entries]

    # Extra safety: filter locally too
    needle = _normalize(query)
    items = [it for it in items if needle in _normalize(it["title"])]

    return items
