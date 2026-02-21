from groq import Groq

client = Groq(api_key="YOUR_API_KEY")

past_emails = """
Past Email 1:
Query: File transfer failed for partner ABC
Reply: We have identified the issue with partner ABC's AS2 connection. The certificate expired. We have renewed it and transfer is now working.

Past Email 2:
Query: Partner XYZ not receiving files
Reply: We checked the MFT logs and found SFTP port was blocked. Coordinated with network team and issue is resolved.
"""

new_email = "Hi team, my file transfer failed for partner XYZ. Can you check the status?"

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": f"Based on these past email replies:\n{past_emails}\n\nDraft a reply to this new email:\n{new_email}"}]
)

print(response.choices[0].message.content)
