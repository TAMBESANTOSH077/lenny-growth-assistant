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

## Demo script (2–3 minutes)

1. Explain the user: Growth PM who wants actionable tactics without listening to 200+ hours.
2. Ask a product/growth question and show transcript sources.
3. Ask a follow-up to demonstrate context.
4. Switch to Ship 30 for 30 and generate the structured essay.
5. Show the Artifact Viewer.
6. Explain the model trade-off: Ollama is private/zero API cost for local evaluation; cloud models provide stronger generation for the public demo.
7. Explain the production path: FastAPI → PostgreSQL/pgvector → agent/router → React artifact viewer.

## Security

Generated HTML is treated as untrusted. The MVP strips `<script>` tags and renders the artifact through Streamlit's component boundary. The full assignment architecture should use DOMPurify plus an iframe with `sandbox="allow-scripts"` and no `allow-same-origin`, as specified in the brief.
