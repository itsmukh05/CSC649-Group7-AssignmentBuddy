import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MODEL_NAME = "gemini-2.5-flash"


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=30000),
    )


if __name__ == "__main__":
    client = get_client()
    if client is None:
        print("ERROR: Gemini API key not found.")
        raise SystemExit(1)

    print("Gemini API key found.")
    print("Connecting to Google Gemini...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents="Reply with: Hello! Assignment Buddy is connected successfully.",
        )
        print("\nSUCCESS! Gemini connection works.")
        print("AI response:")
        print(response.text)
    except Exception as error:
        print("\nConnection failed.")
        print("Error type:", type(error).__name__)
        print("Details:", str(error))