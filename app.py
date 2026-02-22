import os
import streamlit as st
from groq import Groq
from sample_emails import past_emails
from dotenv import load_dotenv

# Doc readers
import openpyxl
from docx import Document
import pdfplumber

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── Load past emails as context ───────────────────────────────
email_context = "\n\n".join([
    f"Query: {e['query']}\nReply: {e['reply']}"
    for e in past_emails
])

# ─── Load docs from docs/ folder ───────────────────────────────
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

def load_all_docs(folder="docs"):
    docs_text = []
    if not os.path.exists(folder):
        return ""
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        try:
            if filename.endswith(".txt"):
                docs_text.append(f"[{filename}]\n{read_txt(path)}")
            elif filename.endswith(".docx"):
                docs_text.append(f"[{filename}]\n{read_docx(path)}")
            elif filename.endswith(".xlsx"):
                docs_text.append(f"[{filename}]\n{read_xlsx(path)}")
            elif filename.endswith(".pdf"):
                docs_text.append(f"[{filename}]\n{read_pdf(path)}")
        except Exception as e:
            docs_text.append(f"[{filename}] Error reading: {e}")
    return "\n\n".join(docs_text)

docs_context = load_all_docs("docs")

# ─── Streamlit UI ───────────────────────────────────────────────
st.set_page_config(page_title="MFT Email Responder", page_icon="📧", layout="wide")

st.title("📧 MFT Support Email Responder")
st.markdown("AI-powered draft replies for MFT/EDI support emails using RAG + LLaMA 3.3")

with st.sidebar:
    st.header("📂 Knowledge Base")
    st.markdown(f"**{len(past_emails)} past emails** loaded")
    with st.expander("📄 Docs loaded"):
        if docs_context:
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
        with st.spinner("Generating draft reply..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"""You are an MFT/EDI support assistant. Use the following knowledge base to draft a professional reply.

PAST SUPPORT EMAILS:
{email_context}

MFT DOCUMENTATION (rules, TP details, approval matrix):
{docs_context}

Now draft a professional reply to this new email:
{new_email}

Important: Follow approval rules strictly. If password reset is requested, mention JO approval is needed and CC the Job Owner."""}]
            )
            reply = response.choices[0].message.content

        st.subheader("📝 Draft Reply")
        st.markdown(reply)
        st.text_area("Copy from here:", value=reply, height=200)
    else:
        st.warning("Please enter an email query first.")