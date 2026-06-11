from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from engine import protect_data, reveal_data
from groq import Groq

load_dotenv()

app = FastAPI(title="PrivacyShield AI API")

# Initialize Groq Client safely using the cloud environment variable
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "healthy", "layer": "local-ner-v4.0", "engine": "Groq Cloud"}

@app.post("/run-secure-query")
def run_query(request: QueryRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    # 1. Local Anonymization (via your engine.py)
    masked_text, mapping = protect_data(request.prompt)
    
    # 2. Safe API Call to Groq
    try:
        system_hint = "Instructions: Respond to the following prompt. Keep all placeholders like [[PERSON_0]] or [[ORG_0]] exactly as they are in your response.\n\n"
        
        completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Fast, reliable model on Groq
            messages=[{"role": "user", "content": system_hint + masked_text}]
        )
        groq_response = completion.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API Error: {str(e)}")
    
    # 3. Local Reconstruction
    final_output = reveal_data(groq_response, mapping)
    
    return {
        "original_prompt": request.prompt,
        "masked_text_sent_to_cloud": masked_text,
        "reconstructed_final_response": final_output
    }