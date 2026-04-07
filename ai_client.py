import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables
load_dotenv(override=True)

# Get the API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    def ask_ai_safely(prompt):
        return "Error: GOOGLE_API_KEY not found. Check Streamlit Secrets."
else:
    genai.configure(api_key=api_key)

    def ask_ai_safely(prompt):
        # List of every possible model name that might work
        model_names = [
            'gemini-1.5-flash', 
            'gemini-pro', 
            'models/gemini-1.5-flash',
            'models/gemini-pro'
        ]
        
        last_err = ""
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception as e:
                last_err = str(e)
                continue
        
        return f"AI Error (All models failed): {last_err}"