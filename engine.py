import spacy

# Loading the NLP model
nlp = spacy.load("en_core_web_sm")

def protect_data(text):
    """
    Takes raw text, finds sensitive entities, and masks them.
    Returns: (masked_text, secret_mapping_dictionary)
    """
    doc = nlp(text)
    secret_mapping = {}
    safe_text = text
    
    # We loop through the entities found by spaCy
    for i, ent in enumerate(doc.ents):
        # Create a placeholder like [[PERSON_0]]
        placeholder = f"[[{ent.label_}_{i}]]"
        
        # Save the real name in our secret 'vault'
        secret_mapping[placeholder] = ent.text
        
        # Replace the real name with the placeholder in the text
        safe_text = safe_text.replace(ent.text, placeholder)
        
    return safe_text, secret_mapping

def reveal_data(safe_text, secret_mapping):
    """
    Takes the AI's response and puts the real names back in.
    """
    original_text = safe_text
    for placeholder, original_value in secret_mapping.items():
        original_text = original_text.replace(placeholder, original_value)
    return original_text

# This part only runs if you run engine.py directly
if __name__ == "__main__":
    test_text = "Anupriya is a student in Jammu."
    safe, vault = protect_data(test_text)
    print(f"Locked: {safe}")
    print(f"Unlocked: {reveal_data(safe, vault)}")