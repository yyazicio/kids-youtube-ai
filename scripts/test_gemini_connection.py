import os

from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Missing GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
chat = client.chats.create(model="gemini-3.8-flash")
response = chat.send_message("Reply with exactly: OK")

print(response.text)
