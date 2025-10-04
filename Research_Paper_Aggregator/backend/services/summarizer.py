import re
import nltk
from collections import Counter
from string import punctuation

# Ensure required NLTK data is present (first run downloads automatically)
def _safe_nltk_download(pkg):
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg.split("/")[-1], quiet=True)

_safe_nltk_download("tokenizers/punkt")
_safe_nltk_download("tokenizers/punkt_tab")
_safe_nltk_download("corpora/stopwords")


from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

STOPWORDS = set(stopwords.words("english"))
PUNCT = set(punctuation)

def _normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def _sentence_scores(text: str):
    # Tokenize
    sentences = sent_tokenize(text)
    if not sentences:
        return [], []
    words = word_tokenize(text.lower())

    # Frequency of non-stopwords
    words = [w for w in words if w.isalpha() and w not in STOPWORDS and w not in PUNCT]
    freq = Counter(words)
    if not freq:
        return sentences, [0.0] * len(sentences)

    # Score each sentence by the sum of its word frequencies (classic, fast, robust)
    scores = []
    for s in sentences:
        tokens = word_tokenize(s.lower())
        score = sum(freq.get(w, 0) for w in tokens if w.isalpha())
        scores.append(float(score))

    # Normalize scores to [0,1]
    m = max(scores) if scores else 1.0
    scores = [s / m if m > 0 else 0.0 for s in scores]
    return sentences, scores

def summarize_text(text: str, max_sentences: int = 6) -> str:
    """
    Lightweight extractive summarizer:
    - tokenizes to sentences
    - scores sentences by word-frequency
    - returns top-N in original order
    """
    text = _normalize_text(text)
    sentences, scores = _sentence_scores(text)
    if not sentences:
        return ""

    max_sentences = max(1, min(max_sentences, len(sentences)))

    # Pick top indices by score
    ranked = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:max_sentences]
    ranked.sort()  # keep original reading order
    summary = " ".join(sentences[i] for i in ranked)
    return summary.strip()
