import os
from groq import Groq
from sample_emails import past_emails
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

context = "\n\n".join([
    f"Query: {e['query']}\nReply: {e['reply']}" 
    for e in past_emails
])

new_email = input("Enter new email query: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": f"Based on these past MFT support emails:\n{context}\n\nDraft a professional reply to:\n{new_email}"}]
)

print("\nDraft Reply:")
print(response.choices[0].message.content)