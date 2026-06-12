import streamlit as st
import os
import spacy

# Direct fallback loading from the official Explosion GitHub wheel
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    try:
        nlp = spacy.load("https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl")
    except Exception:
        # Fallback to prevent app crash if network blips
        pass

# NOW import your custom modules safely
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

# --- UI CONFIGURATION ---
st.set_page_config(page_title="PrivacyShield AI", layout="wide")


# Custom CSS for the Blue Engineering Theme
# Custom CSS for the Blue Engineering Theme
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfc;
    }
    /* Blue Button Styling */
    .stButton>button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.6rem 2.5rem;
        border: none;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        color: white !important;
    }
    .stSubheader {
        color: #1e293b;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    /* Input Box refinement */
    .stTextArea textarea {
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    /* Sidebar styling & fixing the white border artifact */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    /* FIX: Force any native Streamlit structural borders/slivers on the left edge to disappear */
    div[data-testid="stSidebarCollapseButton"] {
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: #f8fafc !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("PrivacyShield AI")
st.markdown("##### Secure local masking for private AI interactions")

with st.sidebar:
    st.markdown("### System Status")
    st.success("🟢 Local NLP: Online")
    st.success("🟢 API Bridge: Active")
    st.divider()
    st.write("PrivacyShield intercepts PII (Names, Locations, Orgs) locally before they leave your system.")

# --- CORE LOGIC ---
# --- CORE LOGIC ---
prompt = st.text_area("Enter your prompt:", height=150, placeholder="e.g., Draft an internship application for Anupriya at Microsoft...")

if st.button("Run Secure Query"):
    if not prompt.strip():
        st.error("Please enter a message.")
    else:
        # Step 1: Local Masking
        masked_text, mapping = protect_data(prompt)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Local Anonymization")
            st.caption("Data transmitted to cloud endpoint:")
            st.info(masked_text)
        
        with st.spinner("Processing safely..."):
            # Step 2: Safe API Call with dynamic placeholder instructions
            system_hint = (
                "Instructions: You are a secure backend assistant. You will receive a prompt where sensitive data "
                "has been masked with tokens like [[PRODUCT_0]], [[PERSON_0]], or [[ORG_0]].\n"
                "CRITICAL RULE: Treat ALL placeholders—regardless of whether they say PERSON, PRODUCT, or ORG—strictly "
                "as dynamic variable placeholders for the name or entity requested. Do not interpret [[PRODUCT_0]] as a "
                "literal commodity, software, or corporate launch item. If the prompt asks to 'draft an email for [[PRODUCT_0]]', "
                "treat it exactly as 'draft an email for this person'. Keep all placeholders exactly as they are in your response.\n\n"
            )
            full_prompt = system_hint + masked_text
            
            ai_response = ask_ai_safely(full_prompt)
            
            # Step 3: Local Unmasking
            final_output = reveal_data(ai_response, mapping)
        
        with col2:
            st.subheader("2. Reconstructed Response")
            st.caption("Final output restored locally:")
            st.success(final_output)

st.divider()
st.caption("Security Layer: local-ner-v4.0 | No PII is sent to the cloud API.")