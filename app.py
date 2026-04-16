import streamlit as st
import spacy
import os
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

# --- UI CONFIGURATION ---
st.set_page_config(page_title="PrivacyShield AI", layout="wide", page_icon="🛡️")

# Custom CSS for a clean, modern "Engineering" look
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    .stButton>button {
        background-color: #059669;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #047857;
        color: white;
        border: none;
    }
    .stSubheader {
        color: #1f2937;
        font-weight: 700;
    }
    .stTextArea textarea {
        border: 1px solid #e5e7eb !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ PrivacyShield AI")
st.markdown("##### Secure local masking for private AI interactions")

with st.sidebar:
    st.title("System Status")
    st.success("🟢 Local NLP: Online")
    st.success("🟢 API Bridge: Active")
    st.divider()
    st.write("PrivacyShield intercepts PII (Names, Locations, Orgs) locally before they leave your system.")

# --- CORE LOGIC ---
prompt = st.text_area("Enter your prompt:", height=150, placeholder="e.g., Send an email to Anupriya at Microsoft about the upcoming project...")

if st.button("Run Secure Query"):
    if not prompt.strip():
        st.error("Please enter a message.")
    else:
        # Step 1: Local Masking
        masked_text, mapping = protect_data(prompt)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Local Anonymization")
            st.caption("What is transmitted to the cloud:")
            st.info(masked_text)
        
        with st.spinner("Processing safely..."):
            # Step 2: Safe API Call with Context Instruction
            system_hint = "Instructions: Respond to the following prompt. Keep all placeholders like [[PERSON_0]] or [[ORG_0]] exactly as they are in your response.\n\n"
            full_prompt = system_hint + masked_text
            
            ai_response = ask_ai_safely(full_prompt)
            
            # Step 3: Local Unmasking
            final_output = reveal_data(ai_response, mapping)
        
        with col2:
            st.subheader("2. Reconstructed Response")
            st.caption("Final output restored on your machine:")
            st.success(final_output)

st.divider()
st.caption("Security Layer: local-ner-v3.7 | Data processed locally using spaCy.")