import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load your secret key
load_dotenv()
my_key = os.getenv("GOOGLE_API_KEY")

if not my_key:
    print("❌ ERROR: API Key not found! Check your .env file.")
else:
    # 2. Setup the Client (Standard v1 for 2026)
    client = genai.Client(
        api_key=my_key,
        http_options=types.HttpOptions(api_version='v1')
    )

    def ask_ai_safely(safe_text):
        try:
            # 3. Use the 2026 Standard Model: gemini-2.5-flash
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=safe_text
            )
            return response.text
        except Exception as e:
            # This helps us see the exact error if it fails again
            return f"❌ AI Error: {str(e)}"

# --- THE TEST ---
if __name__ == "__main__" and my_key:
    print("🚀 Connecting to Gemini 2.5 (Stable)...")
    test_msg = "Give a 1-sentence career tip for [[PERSON_0]] who wants to join [[ORG_1]]."
    answer = ask_ai_safely(test_msg)
    print(f"\nAI Response: {answer}")