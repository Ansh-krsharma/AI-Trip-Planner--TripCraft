"""One-off diagnostic: lists every model your Groq API key can actually access.
Run from the tripcraft-ai folder (same folder as your .env):  python check_models.py
"""
import os

import requests
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GROQ_API_KEY")

if not key:
    print("GROQ_API_KEY not found -- check your .env file.")
else:
    resp = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {key}"},
    )
    print("status:", resp.status_code)
    if resp.status_code == 200:
        ids = [m["id"] for m in resp.json().get("data", [])]
        print(f"Your key can access {len(ids)} model(s):")
        for i in ids:
            print(" -", i)
    else:
        print(resp.text)
