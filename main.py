from engine import protect_data, reveal_data
from ai_client import ask_ai_safely

def run_privacy_shield():
    print("\n--- PRIVACY SHIELD AI (DAY 2) ---")
    
    # 1. User Input
    user_prompt = input("\nEnter your message for the AI: ")
    
    # 2. MASKING (Local)
    safe_text, vault = protect_data(user_prompt)
    print(f"\n[LOCAL] Masked version: {safe_text}")
    
    # 3. AI CALL (Cloud)
    print("[CLOUD] Asking Gemini safely...")
    ai_raw_response = ask_ai_safely(safe_text)
    
    # 4. REVEALING (Local)
    final_output = reveal_data(ai_raw_response, vault)
    
    print("\n" + "="*40)
    print(f"FINAL DECODED RESPONSE:\n{final_output}")
    print("="*40)

if __name__ == "__main__":
    run_privacy_shield()