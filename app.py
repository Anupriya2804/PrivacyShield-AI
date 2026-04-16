import streamlit as st
import spacy
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

# --- PAGE CONFIG ---
st.set_page_config(page_title="PrivacyShield", page_icon="🛡️", layout="centered")

# --- CLEAN AESTHETIC CSS ---
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Elegant Title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #1E293B;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-title {
        font-size: 18px;
        color: #64748B;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Input Box */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 15px !important;
        font-size: 16px !important;
    }

    /* The Button */
    .stButton>button {
        width: 100%;
        border-radius: 8px !important;
        background-color: #4F46E5 !important;
        color: white !important;
        border: none !important;
        padding: 12px !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #4338CA !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Output Cards */
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    
    .label {
        font-size: 12px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI CONTENT ---
st.markdown('<p class="main-title">PrivacyShield</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Secure local masking for private AI interactions</p>', unsafe_allow_html=True)

# Main Input
user_input = st.text_area("", placeholder="Paste your sensitive prompt here...", height=150)

# Center the button a bit
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run_btn = st.button("Process Securely")

if run_btn:
    if not user_input.strip():
        st.toast("Please enter a prompt first.")
    else:
        # Step 1: Local Masking
        masked_text, mapping = protect_data(user_input)
        
        # Step 2: API Call
        with st.spinner("Analyzing..."):
            system_hint = "Respond naturally. Keep placeholders like [[ORG_0]] exactly as they are.\n\n"
            ai_raw = ask_ai_safely(system_hint + masked_text)
            
            # Step 3: Local Unmasking
            final_output = reveal_data(ai_raw, mapping)

        # --- DISPLAY RESULTS ---
        st.markdown("---")
        
        # Row for Masked Text
        st.markdown('<p class="label">Local Anonymization (What the AI sees)</p>', unsafe_allow_html=True)
        st.code(masked_text, language=None)
        
        # Card for Final Result
        st.markdown('<p class="label">Reconstructed Response (Local only)</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card">{final_output}</div>', unsafe_allow_html=True)

# Hide Sidebar by default
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)