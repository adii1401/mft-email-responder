import os
import streamlit as st
from groq import Groq
from sample_emails import past_emails
from dotenv import load_dotenv

import openpyxl
from docx import Document
import pdfplumber
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

st.set_page_config(page_title="MFT Email Responder", page_icon="📧", layout="wide")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── ChromaDB Setup (Persistent) ────────────────────────────────
@st.cache_resource
def setup_chromadb():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = chroma_client.get_or_create_collection(
        name="mft_docs",
        embedding_function=ef
    )
    return chroma_client, collection, ef

chroma_client, collection, embedding_model = setup_chromadb()

# ─── Doc readers ────────────────────────────────────────────────
def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def read_xlsx(path):
    wb = openpyxl.load_workbook(path)
    result = []
    for sheet in wb.sheetnames:
        ws = wb[sheet]
        for row in ws.iter_rows(values_only=True):
            row_text = " | ".join([str(c) for c in row if c is not None])
            if row_text.strip():
                result.append(row_text)
    return "\n".join(result)

def read_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

# ─── Chunking ────────────────────────────────────────────────────
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

# ─── Load past emails into ChromaDB ─────────────────────────────
def load_emails_into_chromadb(collection):
    existing = collection.get(where={"type": "email"})
    if existing["ids"]:
        return len(existing["ids"])

    documents, ids, metadatas = [], [], []
    for i, email in enumerate(past_emails):
        text = f"Query: {email['query']}\nReply: {email['reply']}"
        documents.append(text)
        ids.append(f"email_{i}")
        metadatas.append({"type": "email", "source": "past_emails"})

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    return len(documents)

# ─── Load docs into ChromaDB ─────────────────────────────────────
def load_docs_into_chromadb(collection, folder="docs"):
    if not os.path.exists(folder):
        return 0

    existing = collection.get(where={"type": "doc"})
    if existing["ids"]:
        return len(existing["ids"])

    all_chunks, all_ids, all_metadata = [], [], []
    chunk_id = 0
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            if filename.endswith(".txt"):
                text = read_txt(path)
            elif filename.endswith(".docx"):
                text = read_docx(path)
            elif filename.endswith(".xlsx"):
                text = read_xlsx(path)
            elif filename.endswith(".pdf"):
                text = read_pdf(path)
            else:
                continue

            chunks = chunk_text(text)
            for chunk in chunks:
                if chunk.strip():
                    all_chunks.append(chunk)
                    all_ids.append(f"chunk_{chunk_id}")
                    all_metadata.append({"type": "doc", "source": filename})
                    chunk_id += 1

        except Exception as e:
            st.warning(f"Error reading {filename}: {e}")

    if all_chunks:
        collection.add(documents=all_chunks, ids=all_ids, metadatas=all_metadata)

    return len(all_chunks)

# ─── Distance to Confidence % ────────────────────────────────────
def distance_to_confidence(distance):
    # ChromaDB L2 distance: 0 = identical, ~2 = completely different
    confidence = max(0.0, 1.0 - (distance / 2.0)) * 100
    return round(confidence, 1)

def confidence_badge(score):
    if score >= 70:
        return f"🟢 {score}% match"
    elif score >= 40:
        return f"🟡 {score}% match"
    else:
        return f"🔴 {score}% match"

# ─── Semantic search (emails + docs + confidence) ────────────────
def search_docs(collection, query, top_k=5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    sources = [m["source"] for m in metadatas]
    types = [m["type"] for m in metadatas]
    confidences = [distance_to_confidence(d) for d in distances]
    return chunks, sources, types, confidences

# ─── Load data on startup ────────────────────────────────────────
total_emails = load_emails_into_chromadb(collection)
total_doc_chunks = load_docs_into_chromadb(collection, "docs")

# ─── Streamlit UI ────────────────────────────────────────────────
st.title("📧 MFT Support Email Responder")
st.markdown("AI-powered draft replies for MFT/EDI support emails using RAG + LLaMA 3.3")

with st.sidebar:
    st.header("📂 Knowledge Base")
    st.markdown(f"**{len(past_emails)} past emails** indexed in ChromaDB 🧠")
    st.markdown(f"**{total_doc_chunks} doc chunks** indexed in ChromaDB 🧠")
    with st.expander("📄 Docs loaded"):
        if os.path.exists("docs") and os.listdir("docs"):
            for f in os.listdir("docs"):
                st.markdown(f"✅ {f}")
        else:
            st.markdown("No docs found in docs/ folder")
    for i, e in enumerate(past_emails, 1):
        with st.expander(f"Email {i}"):
            st.markdown(f"**Query:** {e['query']}")
            st.markdown(f"**Reply:** {e['reply']}")

st.subheader("New Email Query")
new_email = st.text_area("Paste the incoming email here:", height=150,
    placeholder="e.g. Our MFT transfer to partner XYZ is failing with error code 1234...")

if st.button("Generate Reply ✨", type="primary"):
    if new_email.strip():
        with st.spinner("Searching knowledge base..."):
            relevant_chunks, sources, types, confidences = search_docs(collection, new_email)
            retrieved_context = "\n\n".join([
                f"[{t.upper()} | Source: {src} | Confidence: {conf}%]\n{chunk}"
                for chunk, src, t, conf in zip(relevant_chunks, sources, types, confidences)
            ])

        # ─── Low confidence warning ──────────────────────────────
        top_confidence = confidences[0] if confidences else 0
        if top_confidence < 40:
            st.warning(
                f"⚠️ Low confidence match ({top_confidence}%) — no strong match found in knowledge base. "
                "Reply may be generic. Consider adding more relevant past emails or docs."
            )

        with st.spinner("Generating draft reply..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"""You are an MFT/EDI support assistant. Use the following retrieved knowledge base context to draft a professional reply.

RETRIEVED CONTEXT (semantically matched to this query):
{retrieved_context}

Now draft a professional reply to this new email:
{new_email}

Important: Follow approval rules strictly. If password reset is requested, mention JO approval is needed and CC the Job Owner."""}]
            )
            reply = response.choices[0].message.content

        st.subheader("📝 Draft Reply")
        st.markdown(reply)
        st.text_area("Copy from here:", value=reply, height=200)

        with st.expander("🔍 Retrieved context (what ChromaDB found)"):
            for chunk, src, t, conf in zip(relevant_chunks, sources, types, confidences):
                badge = confidence_badge(conf)
                st.markdown(f"**[{t.upper()}] Source: {src}** — {badge}")
                st.markdown(chunk)
                st.divider()
    else:
        st.warning("Please enter an email query first.")