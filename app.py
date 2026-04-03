import streamlit as st
from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

st.set_page_config(page_title="PrivacyShield AI", layout="wide")

st.title("PrivacyShield AI")
st.write("Secure your personal data before sending prompts to cloud-based LLMs.")

with st.sidebar:
    st.title("System Overview")
    st.write("""
    This tool uses local Natural Language Processing (NLP) to identify 
    and mask sensitive entities (names, locations, organizations) 
    before they reach the API.
    """)


prompt = st.text_area("Enter your prompt below:", height=150)

if st.button("Run Secure Query"):
    if not prompt.strip():
        st.error("Please enter a valid prompt.")
    else:
       
        masked_text, mapping = protect_data(prompt)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Masked Query")
            st.info(masked_text)
        
        with st.spinner("Processing..."):
            ai_response = ask_ai_safely(masked_text)
       
        final_output = reveal_data(ai_response, mapping)
        
        with col2:
            st.subheader("Final Response")
            st.success(final_output)

st.divider()
st.caption("Data is processed locally using spaCy before transmission.")