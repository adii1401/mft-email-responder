# MFT Email Responder — AI Powered

An AI-powered email response system built for enterprise MFT/EDI workflows. 
Uses RAG (Retrieval Augmented Generation) to draft contextual replies 
based on 30 real-world MFT support email scenarios.

## What it does
- Takes incoming customer/partner email query as input
- Searches 30 past MFT/EDI email replies for similar scenarios
- Drafts a professional contextual reply automatically using LLaMA 3.3 70B

## Tech Stack
- Python
- Groq API (LLaMA 3.3 70B)
- RAG pattern for context-aware responses
- python-dotenv for secure API key management

## Files
- `email_responder.py` — original simple version
- `test_gemini.py` — full RAG version with 30 sample emails
- `sample_emails.py` — 30 MFT/EDI support email scenarios

## Setup
1. Clone this repository
2. Install dependencies: `pip install groq python-dotenv`
3. Create `.env` file and add: `GROQ_API_KEY=your_key_here`
4. Run: `python test_gemini.py`

## Use Case
Built for enterprise B2B integration teams handling MFT/EDI support 
queries from trading partners. POC for cloud mailbox automation.

## Author
Aditya Kumar Gupta  
AI Automation Engineer | MFT | EDI | B2B Integration  
[LinkedIn](https://linkedin.com/in/aditya-kumar-gupta-332453197)
