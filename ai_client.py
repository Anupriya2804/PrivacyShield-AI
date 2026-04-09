import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables
load_dotenv(override=True)

# Get the API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    def ask_ai_safely(prompt):
        return "Error: GOOGLE_API_KEY not found."
else:
    # Force the SDK to use the stable transport
    genai.configure(api_key=api_key)

    def ask_ai_safely(prompt):
        """
        Uses the exact versioned model name to avoid 404 errors.
        """
        try:
            # We use the full path 'models/gemini-1.5-flash' which is the current standard
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text
            else:
                return "AI returned an empty response. Check safety filters."
                
        except Exception as e:
            # Final fallback to a basic model string if the full path fails
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                return f"Final Connection Error: {str(e2)}"