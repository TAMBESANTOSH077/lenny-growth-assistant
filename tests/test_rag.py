from pathlib import Path
from rag import TranscriptIndex

def test_empty_index(tmp_path):
    idx = TranscriptIndex(tmp_path)
    assert idx.search("product growth") == []

def test_retrieval(tmp_path):
    p = tmp_path / "episode.md"
    p.write_text("---\nguest: Test Guest\ntitle: Growth Tactics\n---\nRetention is a product growth lever. Teams should measure activation and retention.", encoding="utf-8")
    idx = TranscriptIndex(tmp_path)
    result = idx.search("retention growth", top_k=1, threshold=0.0)
    assert result
    assert result[0]["guest"] == "Test Guest"
