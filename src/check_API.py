import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

MODEL_NAME = "grok-4.3"


def get_client() -> OpenAI | None:
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
        timeout=30.0,
    )


if __name__ == "__main__":
    client = get_client()
    if client is None:
        print("ERROR: XAI_API_KEY not found in .env.")
        raise SystemExit(1)

    print("xAI API key found.")
    print("Connecting to Grok...")

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with: Hello! Assignment Buddy is connected to Grok successfully.",
                }
            ],
        )
        print("\nSUCCESS! Grok connection works.")
        print("AI response:")
        print(response.choices[0].message.content)
    except Exception as error:
        print("\nConnection failed.")
        print("Error type:", type(error).__name__)
        print("Details:", str(error))