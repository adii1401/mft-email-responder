# 📧 MFT Support Email Responder

An AI-powered email reply generator for MFT/EDI support teams, built using RAG (Retrieval-Augmented Generation) with ChromaDB vector search, LLaMA 3.3 and Groq.

## 🚀 Demo

Paste any MFT/EDI support email query and get a professional draft reply instantly — powered by semantic search over a knowledge base of 30 past support emails + MFT documentation.

## 🛠️ Tech Stack

- **LLaMA 3.3 70B** — LLM for generating replies
- **Groq API** — Ultra-fast inference
- **ChromaDB** — Vector database for semantic search
- **all-MiniLM-L6-v2** — Sentence embedding model (via ChromaDB)
- **RAG** — Past emails + MFT docs used as context for accurate replies
- **Streamlit** — Web UI
- **Python** — Core logic

## 📋 Features

- 30 past MFT/EDI support emails as knowledge base
- MFT documentation support — PDF, DOCX, XLSX, TXT
- ChromaDB semantic vector search (finds relevant context by meaning, not just keywords)
- Text chunking with overlap for better retrieval
- Approval matrix enforcement (JO approval for password resets, etc.)
- Retrieved context viewer — see exactly what the AI used to generate the reply
- Clean Streamlit UI with sidebar knowledge base viewer
- Copy-ready output text area

## ⚙️ Setup

1. Clone the repo
```bash
git clone https://github.com/adii1401/mft-email-responder.git
cd mft-email-responder
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create a `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
```

4. Add your MFT docs to the `docs/` folder (PDF, DOCX, XLSX, TXT supported)

5. Run the app
```bash
streamlit run app.py
```

## 💡 Use Case

MFT/EDI support teams handle repetitive email queries daily. This tool uses past resolved tickets and internal documentation as a semantic knowledge base to draft accurate, policy-compliant replies — reducing response time significantly.

## 🗺️ Roadmap

- [x] RAG pipeline with past emails
- [x] Multi-format doc support (PDF, DOCX, XLSX, TXT)
- [x] ChromaDB vector database
- [x] Semantic embeddings (all-MiniLM-L6-v2)
- [ ] Microsoft Graph API (auto-read Outlook emails)
- [ ] BIS REST API integration
- [ ] Follow-up email tracker

## 👤 Author

**Aditya Kumar Gupta**  
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/adii1401)