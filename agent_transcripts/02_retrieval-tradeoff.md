# Agent Transcript — Retrieval Trade-off

## Attempt
Use pgvector and sentence-transformers for the first public deployment.

## Issue
That adds database provisioning, embedding model cold-start, and deployment complexity.

## Correction
Use TF-IDF cosine retrieval for the deadline-safe demo and document the production migration to sentence-transformers + pgvector/HNSW.

## Result
The app remains a genuine retrieval-grounded vertical slice and can deploy with a small Python dependency set.
