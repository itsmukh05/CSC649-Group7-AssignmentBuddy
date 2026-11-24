from pathlib import Path
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from project root (parent of src/) or current directory
current_dir = Path(__file__).resolve().parent
load_dotenv(current_dir.parent / ".env", override=True)
load_dotenv(current_dir / ".env", override=True)

api_key = os.getenv("GEMINI_API_KEY", "").strip()

if not api_key:
    print("ERROR: Gemini API key not found. Check that .env is in the root folder.")
    raise SystemExit(1)

print("Gemini API key found.")
print("Connecting to Google Gemini...")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=30000),
)

models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash-lite"]
last_error = None

for model_name in models_to_try:
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents="Reply with: Hello! Assignment Buddy is connected successfully.",
            )
            print(f"\nSUCCESS! Connected using {model_name}.")
            print("AI response:")
            print(response.text)
            client.close()
            raise SystemExit(0)
        except Exception as error:
            last_error = error
            err_str = str(error)
            if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                print(f"{model_name} busy (attempt {attempt + 1}/3), retrying...")
                time.sleep(2.0 * (attempt + 1))
                continue
            break

client.close()
print("\nConnection failed.")
print("Error type:", type(last_error).__name__)
print("Details:", str(last_error))