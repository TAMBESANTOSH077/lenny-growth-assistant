import os
import json
import requests

def _context(results):
    return "\n\n".join(
        f"[Episode: {r['episode']}; Guest: {r.get('guest','Unknown')}; Topic: {r.get('timestamp') or 'transcript section'}]\n{r['text']}"
        for r in results
    )

SYSTEM = """You are Lenny Growth Assistant. Answer strictly from the supplied Lenny's Podcast transcript context.
Do not invent facts. If the context does not support the answer, say:
'I do not have sufficient information in Lenny's podcast archive to answer this.'
Cite claims inline using [Episode: Guest, Topic]. Prefer concise, actionable product/growth guidance."""

def _openai(messages, model):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": 0.2},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def _ollama(messages, model):
    url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    r = requests.post(
        f"{url}/api/chat",
        json={"model": model, "messages": messages, "stream": False, "options": {"temperature": 0.2}},
        timeout=90,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]

def generate_answer(query, results, provider, model):
    context = _context(results)
    messages = [
        {"role":"system","content":SYSTEM},
        {"role":"user","content":f"Transcript context:\n{context}\n\nQuestion:\n{query}"},
    ]
    if provider == "OpenAI":
        try:
            result = _openai(messages, model)
            if result: return result
        except Exception as e:
            return f"Cloud model error: {e}. Switch to Demo / Retrieval-only or configure OPENAI_API_KEY."
    if provider == "Ollama":
        try:
            return _ollama(messages, model)
        except Exception as e:
            return f"Ollama error: {e}. Start Ollama and ensure the model is installed."
    # Safe fallback: do not synthesize unsupported facts.
    snippets = "\n\n".join(f"**[{r['episode']}]** {r['text'][:900]}" for r in results)
    return f"### Retrieved evidence\n\n{snippets}\n\n*Retrieval-only mode: the model was not used.*"

SHIP = """You are an expert ghostwriter using a Ship 30 for 30-inspired structure.
Write approximately 1,250 words using only the supplied transcript context.
Requirements: a curiosity-driven hook, short 1–3 sentence paragraphs, H2/H3 headings,
bold anchors, bullets, clear transitions, attributed claims, and a concrete checklist.
Never introduce a claim not supported by the transcript context."""

def generate_ship30(query, results, provider, model):
    context = _context(results)
    messages = [
        {"role":"system","content":SHIP},
        {"role":"user","content":f"Context:\n{context}\n\nTopic/request:\n{query}"},
    ]
    if provider == "OpenAI":
        try:
            result = _openai(messages, model)
            if result: return result
        except Exception as e:
            return f"Cloud model error: {e}."
    if provider == "Ollama":
        try:
            return _ollama(messages, model)
        except Exception as e:
            return f"Ollama error: {e}."
    return "Enable OpenAI/Ollama to generate the full Ship 30 for 30 essay. Retrieved evidence:\n\n" + _context(results)
