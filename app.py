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

# ← ADD THIS HERE (must be first Streamlit command)
st.set_page_config(page_title="MFT Email Responder", page_icon="📧", layout="wide")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── Simple Pure-Python Embedding Function (no torch/onnx needed) ──
@st.cache_resource
def setup_chromadb():
    chroma_client = chromadb.Client()
    ef = embedding_functions.DefaultEmbeddingFunction()
    collection = chroma_client.get_or_create_collection(
        name="mft_docs",
        embedding_function=ef
    )
    return chroma_client, collection, ef

chroma_client, collection, embedding_model = setup_chromadb()

# ─── Load past emails as context ───────────────────────────────
email_context = "\n\n".join([
    f"Query: {e['query']}\nReply: {e['reply']}"
    for e in past_emails
])

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

# ─── Chunking ───────────────────────────────────────────────────
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

# ─── Load docs into ChromaDB ────────────────────────────────────
def load_docs_into_chromadb(folder="docs"):
    if not os.path.exists(folder):
        return 0

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    all_chunks = []
    all_ids = []
    all_metadata = []

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
                    all_metadata.append({"source": filename})
                    chunk_id += 1

        except Exception as e:
            st.warning(f"Error reading {filename}: {e}")

    if all_chunks:
        collection.add(
            documents=all_chunks,
            ids=all_ids,
            metadatas=all_metadata
        )

    return len(all_chunks)

# ─── Semantic search ────────────────────────────────────────────
def search_docs(query, top_k=5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return chunks, sources

# ─── Load docs on startup ───────────────────────────────────────
total_chunks = load_docs_into_chromadb("docs")

# ─── Streamlit UI ───────────────────────────────────────────────
st.title("📧 MFT Support Email Responder")
st.markdown("AI-powered draft replies for MFT/EDI support emails using RAG + LLaMA 3.3")

with st.sidebar:
    st.header("📂 Knowledge Base")
    st.markdown(f"**{len(past_emails)} past emails** loaded")
    st.markdown(f"**{total_chunks} chunks** indexed in ChromaDB 🧠")
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
            relevant_chunks, sources = search_docs(new_email)
            docs_context = "\n\n".join([
                f"[Source: {src}]\n{chunk}"
                for chunk, src in zip(relevant_chunks, sources)
            ])

        with st.spinner("Generating draft reply..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"""You are an MFT/EDI support assistant. Use the following knowledge base to draft a professional reply.

PAST SUPPORT EMAILS:
{email_context}

RELEVANT MFT DOCUMENTATION (semantically matched to this query):
{docs_context}

Now draft a professional reply to this new email:
{new_email}

Important: Follow approval rules strictly. If password reset is requested, mention JO approval is needed and CC the Job Owner."""}]
            )
            reply = response.choices[0].message.content

        st.subheader("📝 Draft Reply")
        st.markdown(reply)
        st.text_area("Copy from here:", value=reply, height=200)

        with st.expander("🔍 Retrieved context (what ChromaDB found)"):
            for chunk, src in zip(relevant_chunks, sources):
                st.markdown(f"**Source: {src}**")
                st.markdown(chunk)
                st.divider()
    else:
        st.warning("Please enter an email query first.")