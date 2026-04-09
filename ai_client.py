import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    def ask_ai_safely(prompt): return "Key Missing"
else:
    # THIS IS THE CRITICAL FIX: Force the version to v1
    genai.configure(api_key=api_key, transport='rest') 

    def ask_ai_safely(prompt):
        # We use 'gemini-1.5-flash' as it is the most modern stable model
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Deployment Error: {str(e)}"