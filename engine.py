import spacy

nlp = spacy.load("en_core_web_sm")

def protect_data(text):
    doc = nlp(text)
    mapping = {}
    masked = text
    counters = {}

    # 1. Gather all entities found by spaCy
    entities = list(doc.ents)
    
    # 2. Extract words into a list to check context clues
    words = [token.text.lower() for token in doc]
    
    # 3. Process and apply strict overrides
    for ent in sorted(entities, key=lambda e: e.start_char, reverse=True):
        label = ent.label_
        ent_text = ent.text
        
        # CONTEXT CLUE OVERRIDE: If spaCy labeled a name as a PRODUCT,
        # but the user typed "email for [Name]" or "message for [Name]", force it to PERSON
        if label == "PRODUCT":
            # Check if "for" or "to" appears right before this entity in the text
            lower_text = text.lower()
            entity_index = lower_text.find(ent_text.lower())
            surrounding_text = lower_text[max(0, entity_index-10):entity_index]
            
            if "for " in surrounding_text or "to " in surrounding_text or "dear " in surrounding_text:
                label = "PERSON"

        # Apply standard tracking tokens
        counters[label] = counters.get(label, 0)
        token = f"[[{label}_{counters[label]}]]"
        mapping[token] = ent_text
        
        # Swap the text locally
        masked = masked[:ent.start_char] + token + masked[ent.end_char:]
        counters[label] += 1

    return masked, mapping

def reveal_data(text, mapping):
    # Standard restoration logic
    for token, original_value in mapping.items():
        text = text.replace(token, original_value)
    return text