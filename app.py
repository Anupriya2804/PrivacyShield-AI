import streamlit as st
import spacy
import os
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

# This will now work because Streamlit pre-installs it from requirements.txt
nlp = spacy.load("en_core_web_sm")

# --- UI CONFIGURATION ---
st.set_page_config(page_title="PrivacyShield AI", layout="wide", page_icon="🛡️")

st.title("🛡️ PrivacyShield AI")
st.write("Secure your personal data before sending prompts to cloud-based LLMs.")

with st.sidebar:
    st.title("System Overview")
    st.write("Local NLP masking ensures PII never leaves your system.")
    st.divider()
    st.caption("3rd Year CSE Project")

# --- CORE LOGIC ---
prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Run Secure Query"):
    if not prompt.strip():
        st.error("Please enter a message.")
    else:
        # Step 1: Local Masking
        masked_text, mapping = protect_data(prompt)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Masked Query")
            st.info(masked_text)
        
        with st.spinner("AI is thinking..."):
            # Step 2: Safe API Call
            ai_response = ask_ai_safely(masked_text)
            # Step 3: Local Unmasking
            final_output = reveal_data(ai_response, mapping)
        
        with col2:
            st.subheader("2. Final Response")
            st.success(final_output)