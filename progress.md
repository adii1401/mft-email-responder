# Aditya's AI Journey

## Personal Context
- Name: Aditya Kumar Gupta
- Current: Cognizant, 6.7 LPA, MFT/EDI/Seeburger team
- Goal: AI Automation Engineer, 15-18 LPA by Feb 2027

## Project: MFT Support Email Responder
- GitHub: github.com/adii1401/mft-email-responder
- Live: [your streamlit URL]
- Stack: Python, Groq, LLaMA 3.3, Streamlit, ChromaDB, all-MiniLM-L6-v2, RAG

## What's Built
- RAG pipeline with past emails as context ✅
- Reads PDF, DOCX, XLSX, TXT docs ✅
- Streamlit UI ✅
- Deployed on Streamlit Cloud ✅
- Dummy MFT docs (TP master list, rules, escalation guide) ✅
- ChromaDB vector database (proper semantic search) ✅
- Text chunking with overlap (500 words, 50 overlap) ✅
- all-MiniLM-L6-v2 semantic embeddings ✅
- Top-K semantic retrieval (only relevant chunks sent to LLM) ✅
- Retrieved context viewer (debug expander in UI) ✅
- Secrets management (.env excluded, Streamlit secrets used) ✅

## Day Log
| Day | What was done |
|-----|--------------|
| Day 1 | Project setup, Groq + LLaMA integration, basic UI |
| Day 2 | RAG with past emails, doc readers (PDF/DOCX/XLSX/TXT), deployed |
| Day 3 | ChromaDB integration, semantic chunking, all-MiniLM-L6-v2 embeddings, redeployed |

## Next Steps
- [ ] Microsoft Graph API (Outlook integration — auto-read emails)
- [ ] BIS REST API integration (fetch transfer status automatically)
- [ ] Follow-up email tracker
- [ ] Persistent ChromaDB (disk-based, survives restarts)

## Long Term Vision
Auto-read emails from Outlook → fetch BIS status → 
generate reply using RAG + ChromaDB → CC Job Owner → track follow-ups