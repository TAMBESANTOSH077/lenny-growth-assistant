# Lenny Growth Assistant — deadline-ready Streamlit MVP

A deployable RAG-style assistant for Lenny's Podcast transcripts, with:
- transcript-only retrieval and source attribution
- OpenAI cloud model or Ollama local model toggle
- Ship 30 for 30 content mode
- side-by-side artifact viewer
- graceful retrieval-only fallback
- Streamlit Community Cloud deployment

> **Assignment alignment:** The supplied assessment asks for FastAPI + PostgreSQL + an agent layer + a frontend artifact viewer. This implementation intentionally uses Streamlit to get a reliable public demo live quickly. In the handoff, describe this as the demo vertical slice and explicitly call out the architecture path to the full FastAPI/Postgres version.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

For Ollama:
```bash
ollama pull llama3.2:3b
ollama serve
```

For OpenAI:
```bash
set OPENAI_API_KEY=...
# PowerShell: $env:OPENAI_API_KEY="..."
streamlit run app.py
```

## Add transcript data

Place Markdown/TXT transcripts in `data/transcripts/`. The index automatically chunks them into ~550-word windows with overlap and uses TF-IDF cosine retrieval. This is a lightweight deployment-safe retrieval layer; the production architecture uses sentence-transformers + pgvector/HNSW.

The public archive used by the assignment is:
https://github.com/doncampbell/lennys-podcast-transcripts

## Streamlit Community Cloud

1. Push this repository to a GitHub repository you control.
2. Ensure `app.py` and `requirements.txt` are in the repository.
3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Create app → select repository → branch → `app.py` → Deploy.
5. In Advanced settings, add `OPENAI_API_KEY` as a secret if using OpenAI.
6. Use OpenAI mode on Community Cloud. Ollama is for the local evaluation demo.

Streamlit's current deployment docs recommend a `requirements.txt` and keeping secrets out of Git. See the official docs linked above.
