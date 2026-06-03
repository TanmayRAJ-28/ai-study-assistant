"""check_groq_models.py

Attempts to list available Groq models using available clients.

Usage: python check_groq_models.py
"""
import os
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")


def try_langchain_groq():
    try:
        # Attempt to use langchain_groq client if available
        from langchain_groq import GroqClient

        client = GroqClient(api_key=API_KEY) if API_KEY else GroqClient()
        if hasattr(client, "list_models"):
            models = client.list_models()
            return models
        # try alternative attribute
        if hasattr(client, "models"):
            return client.models
    except Exception:
        return None


def try_http_list():
    # Best-effort HTTP request to Groq models endpoint. If the
    # project's langchain-groq client is not available, this will
    # attempt the public API. If the endpoint differs in your
    # account, update the URL accordingly.
    try:
        import requests

        url = "https://api.groq.com/v1/models"
        headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"HTTP {resp.status_code}", "text": resp.text}
    except Exception:
        return None


def main():
    print("Checking for Groq models...\n")

    if not API_KEY:
        print("GROQ_API_KEY is not set in your environment (.env). Please set it and retry.")
        return

    print("1) Trying langchain_groq client...")
    res = try_langchain_groq()
    if res:
        print("Found models via langchain_groq client:\n")
        print(json.dumps(res, indent=2))
        return

    print("2) Falling back to HTTP request to Groq API...")
    res = try_http_list()
    if res:
        print("HTTP response:\n")
        print(json.dumps(res, indent=2) if not isinstance(res, str) else res)
        return

    print("Unable to list models. Ensure you have network access, a valid GROQ_API_KEY, and either the langchain-groq client or the requests package installed.")


if __name__ == "__main__":
    main()
