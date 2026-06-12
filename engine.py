import spacy

nlp = spacy.load("en_core_web_sm")

def protect_data(text):
    doc = nlp(text)
    mapping = {}
    masked = text
    counters = {}

    # 1. Track entities and individual tokens
    entities = list(doc.ents)
    
    # 2. Build a map of words that are definitely proper nouns/names based on sentence structure
    forced_person_texts = []
    for token in doc:
        # If it's a Proper Noun and it is acting as a subject or a person-like token
        if token.pos_ == "PROPN" and token.dep_ in ["nsubj", "nsubjpass", "flat"]:
            # Make sure it's not a known corporate word like Microsoft or Google
            if token.text.lower() not in ["microsoft", "google", "amazon", "apple", "meta"]:
                forced_person_texts.append(token.text)

    # 3. Process entities with strict structural rules
    for ent in sorted(entities, key=lambda e: e.start_char, reverse=True):
        label = ent.label_
        ent_text = ent.text
        
        # RULE: If the model thinks a human name is an ORG or a PRODUCT,
        # but our structural pass flagged it as a Proper Noun Subject, force it to PERSON
        if ent_text in forced_person_texts or label in ["PRODUCT", "ORG"]:
            # Protect known actual organizations
            if ent_text.lower() not in ["microsoft", "google", "amazon", "apple", "meta"]:
                label = "PERSON"

        # Apply standard tracking tokens
        counters[label] = counters.get(label, 0)
        token = f"[[{label}_{counters[label]}]]"
        mapping[token] = ent_text
        
        # Swap the text out locally
        masked = masked[:ent.start_char] + token + masked[ent.end_char:]
        counters[label] += 1

    return masked, mapping

def reveal_data(text, mapping):
    for token, original_value in mapping.items():
        text = text.replace(token, original_value)
    return text