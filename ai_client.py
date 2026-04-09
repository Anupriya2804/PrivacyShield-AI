import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    def ask_ai_safely(prompt):
        return "Error: GOOGLE_API_KEY not found."
else:
    client = genai.Client(api_key=api_key)

    def ask_ai_safely(prompt):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            if response and response.text:
                return response.text
            else:
                return "AI returned an empty response. Check safety filters."
        except Exception as e:
            return f"Connection Error: {str(e)}"