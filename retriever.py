from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CORPUS_PATH = Path(__file__).parent / "knowledge_base.txt"

def load_documents():
    raw = CORPUS_PATH.read_text(encoding="utf-8")
    return [x.strip() for x in raw.split("\n---\n") if x.strip()]

DOCUMENTS = load_documents()
VECTORIZER = TfidfVectorizer(stop_words="english")
MATRIX = VECTORIZER.fit_transform(DOCUMENTS)

def retrieve(query: str, k: int = 4):
    k = max(1, min(k, 4))
    q = VECTORIZER.transform([query])
    scores = cosine_similarity(q, MATRIX)[0]
    ranked = scores.argsort()[::-1][:k]
    return [
        {"text": DOCUMENTS[i], "score": float(scores[i])}
        for i in ranked
        if scores[i] > 0
    ]
