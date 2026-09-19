import os
import re
import html
from pathlib import Path

import streamlit as st
from rag import TranscriptIndex
from llm import generate_answer, generate_ship30

st.set_page_config(page_title="Lenny Growth Assistant", page_icon="🚀", layout="wide")

BASE = Path(__file__).parent
DATA_DIR = BASE / "data" / "transcripts"

@st.cache_resource
def load_index():
    return TranscriptIndex(DATA_DIR)

index = load_index()

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; max-width: 1500px;}
.small {font-size: .85rem; color: #6b7280;}
.answer {font-size: 1.02rem; line-height: 1.65;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Lenny Growth Assistant")
st.caption("Grounded product & growth intelligence from Lenny's Podcast transcripts")

with st.sidebar:
    st.header("Controls")
    provider = st.selectbox("LLM Provider", ["OpenAI", "Ollama", "Demo / Retrieval-only"])
    model = st.text_input(
        "Model",
        value=("gpt-4o-mini" if provider == "OpenAI" else "llama3.2:3b" if provider == "Ollama" else "retrieval"),
    )
    mode = st.radio("Mode", ["Grounded Q&A", "Ship 30 for 30"], index=0)
    top_k = st.slider("Retrieved sources", 3, 6, 5)
    threshold = st.slider("Similarity threshold", 0.05, 0.80, 0.15, 0.05)
    st.divider()
    st.write(f"**Indexed chunks:** {index.size}")
    st.write("**Grounding:** transcript-only")
    st.info("For the required local demo, run Ollama locally. Streamlit Community Cloud should use OpenAI or retrieval-only mode.")

if "messages" not in st.session_state:
    st.session_state.messages = []

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("sources"):
                with st.expander("Sources"):
                    for s in m["sources"]:
                        st.markdown(
                            f"**{s['episode']}** — {s.get('guest','Unknown')}  \n"
                            f"Score: `{s['score']:.3f}`  \n{s['text'][:500]}…"
                        )

    prompt = st.chat_input("Ask a product or growth question…")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        results = index.search(prompt, top_k=top_k, threshold=threshold)
        with st.chat_message("assistant"):
            if not results:
                answer = "I do not have sufficient information in Lenny's podcast archive to answer this."
                st.warning(answer)
                sources = []
            else:
                if mode == "Ship 30 for 30":
                    answer = generate_ship30(prompt, results, provider, model)
                else:
                    answer = generate_answer(prompt, results, provider, model)
                st.markdown(answer)
                sources = results
                if sources:
                    with st.expander("Grounding sources"):
                        for s in sources:
                            st.markdown(f"**[{s['episode']}: {s.get('guest','Unknown')}]** — score `{s['score']:.3f}`")
                            st.caption(s["text"][:700])

        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
        st.rerun()

with right:
    st.subheader("Artifact Viewer")
    st.caption("Generated artifacts are displayed separately from the chat.")

    if st.session_state.messages:
        latest = next((m for m in reversed(st.session_state.messages) if m["role"] == "assistant"), None)
        if latest:
            artifact_type = st.selectbox("Artifact type", ["Markdown", "HTML/CSS"])
            if st.button("Create artifact from latest answer"):
                if artifact_type == "Markdown":
                    st.markdown(latest["content"])
                else:
                    # Sandboxed iframe-like preview through Streamlit's component boundary.
                    body = latest["content"].replace("```html", "").replace("```", "")
                    safe = re.sub(r"<script.*?</script>", "", body, flags=re.I | re.S)
                    doc = f"""<!doctype html><html><head><meta charset='utf-8'>
                    <style>body{{font-family:Inter,Arial,sans-serif;padding:24px;line-height:1.6}}
                    pre{{white-space:pre-wrap}}</style></head><body>{html.escape(safe)}</body></html>"""
                    import streamlit.components.v1 as components
                    components.html(doc, height=620, scrolling=True)
    else:
        st.info("Ask a question first, then generate a Markdown or HTML/CSS artifact.")
