
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

# Load .env file
project_folder = Path(__file__).resolve().parent
load_dotenv(project_folder / ".env", override=True)

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found.")
    raise SystemExit(1)

print("Gemini API key found.")
print("Connecting to Google Gemini...")

try:
    # Create Gemini client with 30-second timeout
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000
        )
    )

    # Send test request
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with: Hello! Assignment Buddy is connected successfully."
    )

    print("\nSUCCESS! Gemini connection works.")
    print("AI response:")
    print(response.text)

except Exception as error:
    print("\nConnection failed.")
    print("Error type:", type(error).__name__)
    print("Details:", str(error))
