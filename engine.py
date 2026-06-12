import spacy

nlp = spacy.load("en_core_web_sm")

IGNORE_WORDS = {"intern", "engineer", "manager", "developer", "analyst",
                "director", "ceo", "cto", "associate", "consultant",
                "microsoft", "google", "amazon", "apple", "meta", "openai"}

KNOWN_ORGS = {"microsoft", "google", "amazon", "apple", "meta", "openai",
              "netflix", "tesla", "twitter", "linkedin", "adobe", "oracle"}

def protect_data(text):
    doc = nlp(text)
    mapping = {}
    masked = text
    counters = {}

    covered = []
    cleaned_ents = []
    entities = list(doc.ents)

    # Pass 1: Handle spaCy's caught entities and patch structural mislabels
    for ent in entities:
        if ent.text.lower() in IGNORE_WORDS:
            continue
            
        label = ent.label_
        
        # If it's a known major corporation, lock it in as an organization
        if ent.text.lower() in KNOWN_ORGS:
            label = "ORG"
        # If spaCy misclassified a name as a product or art piece, correct it
        elif label in ["PRODUCT", "WORK_OF_ART", "ORG"]:
            # Default to PERSON if it's acting as a noun subject or direct object
            for token in doc:
                if token.text == ent.text and token.dep_ in ["nsubj", "nsubjpass", "dobj"]:
                    label = "PERSON"
                    break
                    
        cleaned_ents.append((ent.start_char, ent.end_char, ent.text, label))
        covered.append((ent.start_char, ent.end_char))

    # Pass 2: Fallback loop (Now safely checks index 0 for true Proper Nouns)
    for token in doc:
        if token.is_alpha and token.text[0].isupper():
            if token.text.lower() not in IGNORE_WORDS:
                # If it's explicitly identified structurally as a Proper Noun
                if token.pos_ == "PROPN":
                    # Double check it hasn't been processed in Pass 1
                    already = any(s <= token.idx < e for s, e in covered)
                    if not already:
                        # Treat it as a person token
                        label = "PERSON"
                        cleaned_ents.append((token.idx, token.idx + len(token.text), token.text, label))
                        covered.append((token.idx, token.idx + len(token.text)))

    # Sort in absolute reverse order to keep character indexes from shifting
    cleaned_ents.sort(key=lambda x: x[0], reverse=True)

    for start, end, ent_text, label in cleaned_ents:
        counters[label] = counters.get(label, 0)
        placeholder = f"[[{label}_{counters[label]}]]"
        mapping[placeholder] = ent_text
        masked = masked[:start] + placeholder + masked[end:]
        counters[label] += 1

    return masked, mapping


def reveal_data(text, mapping):
    for placeholder, original_value in mapping.items():
        text = text.replace(placeholder, original_value)
    return text