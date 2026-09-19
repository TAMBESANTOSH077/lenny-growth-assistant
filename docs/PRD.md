# PRD — Lenny Growth Assistant

## Discovery brief

**User:** Product/growth PM or growth leader.

**Job:** Find concrete product and growth tactics from Lenny's Podcast without manually searching/listening through hundreds of hours of interviews.

**Pain removed:** Slow discovery, fragmented knowledge, and uncertainty about whether an answer is actually supported by a source.

## Success metrics

- Retrieval/source citation accuracy: ≥90% on a manually sampled evaluation set.
- Local Ollama first-token latency: target <4s.
- Artifact rendering: 0 known XSS paths in security tests.
- Public demo: evaluator can start the app and ask a grounded question in <5 minutes.

## Assumptions

1. Podcast transcripts are the authoritative knowledge source.
2. Unsupported questions should produce an explicit insufficiency response.
3. Ollama is mandatory for the local demo; cloud inference is a deployment convenience.
4. The deadline favors a working vertical slice over infrastructure that cannot be demonstrated.
5. Streamlit is used for the public demo; the target production architecture remains FastAPI + Postgres/pgvector + React.

## Scope

### Included
- Transcript ingestion/chunking.
- Grounded retrieval.
- Source attribution.
- Follow-up chat session in UI.
- Ship 30 for 30 content skill.
- Artifact preview.
- Local/cloud provider toggle.
- Public Streamlit deployment path.
- Documentation and tests.

### Intentionally excluded from the MVP
- Multi-user authentication.
- Production PostgreSQL persistence.
- Full agent SDK orchestration.
- Automated transcript refresh jobs.
- Enterprise observability stack.

These are documented as the production hardening path rather than hidden omissions.

## Risks / trade-offs

| Risk | Mitigation |
|---|---|
| Hallucination | Transcript-only prompt + retrieval threshold + explicit insufficiency |
| Local model quality | Keep Ollama model configurable; use cloud provider for stronger generation |
| API cost | Retrieval-only mode and local Ollama |
| Unsafe HTML | Strip scripts in MVP; production uses DOMPurify + sandboxed iframe |
| Cold start | Lightweight TF-IDF MVP; production uses pgvector/HNSW |
| Data freshness | Versioned transcript ingestion script |

## Acceptance criteria

- User can submit a product/growth question.
- Relevant transcript chunks are shown with similarity scores.
- Model response is grounded and source-attributed.
- Unsupported query returns insufficiency behavior.
- Ship 30 mode generates the requested structure when a model is configured.
- Artifact is displayed beside chat.
- App runs from `streamlit run app.py`.
