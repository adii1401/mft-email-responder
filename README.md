# 📧 MFT Support Email Responder

An AI-powered email reply generator for MFT/EDI support teams, built using RAG (Retrieval-Augmented Generation) with LLaMA 3.3 and Groq.

## 🚀 Demo

Paste any MFT/EDI support email query and get a professional draft reply instantly — powered by a knowledge base of 30 past support emails.

## 🛠️ Tech Stack

- **LLaMA 3.3 70B** — LLM for generating replies
- **Groq API** — Ultra-fast inference
- **RAG** — Past emails used as context for accurate, domain-specific replies
- **Streamlit** — Web UI
- **Python** — Core logic

## 📋 Features

- 30 past MFT/EDI support emails loaded as knowledge base
- Generates professional, context-aware draft replies
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

4. Run the app
```bash
   streamlit run app.py
```

## 💡 Use Case

MFT/EDI support teams handle repetitive email queries daily. This tool uses past resolved tickets as context to draft accurate replies — reducing response time significantly.

## 👤 Author

**Aditya Kumar Gupta**  
[LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/adii1401)