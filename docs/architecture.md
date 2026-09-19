# Architecture

## MVP topology

`Streamlit UI → Retriever → LLM provider → Source/Artifact rendering`

### Retrieval
1. Markdown/TXT transcript files are loaded.
2. YAML frontmatter is parsed when present.
3. Text is chunked into overlapping windows.
4. TF-IDF vectors are built at startup.
5. Query vector is compared using cosine similarity.
6. Top K chunks above threshold are passed to the model.

### Model routing

`provider=OpenAI` → OpenAI Chat Completions API

`provider=Ollama` → `http://localhost:11434/api/chat`

`provider=Demo` → retrieval-only evidence display

The interface is intentionally provider-neutral.

## Production target

`React/Next.js → FastAPI → Agent Router → Retriever → PostgreSQL/pgvector`

- PostgreSQL stores sessions/messages/artifacts.
- pgvector stores embeddings with HNSW cosine index.
- FastAPI exposes `/api/sessions`, `/api/chat`, `/api/health`.
- Agent skills are isolated into grounded QA, Ship 30, and artifact generation.
- Model provider is selected through configuration or request metadata.

## Security

Generated HTML is untrusted. The production viewer should:
- sanitize using DOMPurify;
- render in `<iframe sandbox="allow-scripts">`;
- omit `allow-same-origin`;
- never expose parent cookies/storage/DOM.

## Resilience

- missing OpenAI key → clear UI error/fallback
- unavailable Ollama → actionable error
- empty retrieval → explicit insufficiency response
- model timeout → surfaced error
- invalid input → validation before generation
