import os
import streamlit as st
from groq import Groq
from sample_emails import past_emails
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

context = "\n\n".join([
    f"Query: {e['query']}\nReply: {e['reply']}" 
    for e in past_emails
])

# --- Page Config ---
st.set_page_config(page_title="MFT Email Responder", page_icon="📧", layout="wide")

st.title("📧 MFT Support Email Responder")
st.markdown("AI-powered draft replies for MFT/EDI support emails using RAG + LLaMA 3.3")

# --- Sidebar ---
with st.sidebar:
    st.header("📂 Knowledge Base")
    st.markdown(f"**{len(past_emails)} past emails** loaded as context")
    for i, e in enumerate(past_emails, 1):
        with st.expander(f"Email {i}"):
            st.markdown(f"**Query:** {e['query']}")
            st.markdown(f"**Reply:** {e['reply']}")

# --- Main Input ---
st.subheader("New Email Query")
new_email = st.text_area("Paste the incoming email here:", height=150, placeholder="e.g. Our MFT transfer to partner XYZ is failing with error code 1234...")

if st.button("Generate Reply ✨", type="primary"):
    if new_email.strip():
        with st.spinner("Generating draft reply..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Based on these past MFT support emails:\n{context}\n\nDraft a professional reply to:\n{new_email}"}]
            )
            reply = response.choices[0].message.content

        st.subheader("📝 Draft Reply")
        st.markdown(reply)

        # Copy-friendly text box
        st.text_area("Copy from here:", value=reply, height=200)
    else:
        st.warning("Please enter an email query first.")