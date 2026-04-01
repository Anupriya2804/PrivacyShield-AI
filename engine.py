import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def anonymize_text(text):
    doc = nlp(text)
    mapping = {}
    anonymized_text = text
    
    # Let's find Entities (Names, Orgs, Locations)
    for ent in doc.ents:
        if ent.label_ in ["PERSON", "ORG", "GPE"]: # GPE is locations
            placeholder = f"[[{ent.label_}_{len(mapping)}]]"
            mapping[placeholder] = ent.text
            anonymized_text = anonymized_text.replace(ent.text, placeholder)
            
    return anonymized_text, mapping

# TEST IT
test_input = "Anupriya is working at Microsoft in Jammu."
safe_text, secret_key = anonymize_text(test_input)

print("--- ORIGINAL ---")
print(test_input)
print("\n--- SAFE FOR AI ---")
print(safe_text)
print("\n--- THE SECRET MAPPING ---")
print(secret_key)