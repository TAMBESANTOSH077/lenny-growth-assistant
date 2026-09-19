from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TranscriptIndex:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.chunks = self._load()
        texts = [c["text"] for c in self.chunks] or ["No transcript data available."]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), min_df=1)
        self.matrix = self.vectorizer.fit_transform(texts)

    @property
    def size(self):
        return len(self.chunks)

    def _load(self):
        chunks = []
        for path in sorted(self.data_dir.rglob("*.md")) + sorted(self.data_dir.rglob("*.txt")):
            raw = path.read_text(encoding="utf-8", errors="ignore")
            guest = "Unknown"
            title = path.stem
            fm = re.search(r"^---\s*(.*?)\s*---", raw, flags=re.S)
            if fm:
                meta = fm.group(1)
                g = re.search(r"guest:\s*(.+)", meta)
                t = re.search(r"title:\s*(.+)", meta)
                if g: guest = g.group(1).strip().strip("'\"")
                if t: title = t.group(1).strip().strip("'\"")
                raw = raw[fm.end():]
            text = re.sub(r"\s+", " ", raw).strip()
            words = text.split()
            step = 550
            overlap = 100
            for start in range(0, len(words), step-overlap):
                piece = " ".join(words[start:start+step])
                if len(piece.split()) >= 10:
                    chunks.append({
                        "episode": title,
                        "guest": guest,
                        "text": piece,
                        "timestamp": "",
                    })
                if start + step >= len(words):
                    break
        return chunks

    def search(self, query, top_k=5, threshold=0.15):
        if not self.chunks:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        idxs = scores.argsort()[::-1]
        out = []
        for i in idxs[:top_k]:
            if scores[i] >= threshold:
                item = dict(self.chunks[i])
                item["score"] = float(scores[i])
                out.append(item)
        return out
