import os
import subprocess
import sys

try:
    import spacy

    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    import spacy
    nlp = spacy.load("en_core_web_sm")

import streamlit as st
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

st.set_page_config(page_title="PrivacyShield AI", layout="wide")

st.title("🛡️ PrivacyShield AI")
st.write("Secure your personal data before sending prompts to cloud-based LLMs.")

with st.sidebar:
    st.title("System Overview")
    st.write("""
    This tool uses local Natural Language Processing (NLP) to identify 
    and mask sensitive entities (names, locations, organizations) 
    before they reach the API.
    """)
    st.divider()
    st.caption("Engine: spaCy (en_core_web_sm)")
    st.caption("LLM: Google Gemini 2.5")

prompt = st.text_area("Enter your prompt below (e.g., 'My name is Anupriya and I live in Jammu'):", height=150)

if st.button("Run Secure Query"):
    if not prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
        # 1. Mask the data locally
        masked_text, mapping = protect_data(prompt)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1. Local Masking (Private)")
            st.info(f"**Sent to AI:**\n\n{masked_text}")
            with st.expander("View Mapping Keys"):
                st.json(mapping)
        
        with st.spinner("Querying AI safely..."):
            # 2. Send masked text to Gemini
            ai_response = ask_ai_safely(masked_text)
            
            # 3. Unmask the response locally
            final_output = reveal_data(ai_response, mapping)
        
        with col2:
            st.subheader("2. Final Response (De-identified)")
            st.success(final_output)

st.divider()
st.caption("Built as a 3rd-year CSE Project - Privacy-First AI Middleware.")