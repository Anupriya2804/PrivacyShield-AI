import spacy
import re

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

    # Collect all char ranges already covered by spaCy entities
    covered = []
    entities = list(doc.ents)

    # Fix mislabelled entities + skip job titles
    cleaned_ents = []
    for ent in entities:
        if ent.text.lower() in IGNORE_WORDS:
            continue
        label = ent.label_
        if label in ["PRODUCT", "WORK_OF_ART"]:
            # Check if it's a proper noun subject — likely a person
            for token in doc:
                if token.text == ent.text and token.dep_ in ["nsubj", "nsubjpass"]:
                    label = "PERSON"
                    break
        cleaned_ents.append((ent.start_char, ent.end_char, ent.text, label))
        covered.append((ent.start_char, ent.end_char))

    # Fallback: catch capitalized words spaCy missed
    # (likely names — single capitalized token not at sentence start)
    for token in doc:
        if token.is_alpha and token.text[0].isupper():
            if token.i != 0:  # not the first word of sentence
                if token.text.lower() not in IGNORE_WORDS:
                    if token.pos_ == "PROPN":
                        # Check if already covered by an entity
                        already = any(s <= token.idx < e for s, e in covered)
                        if not already:
                            label = "PERSON"
                            cleaned_ents.append((token.idx, token.idx + len(token.text), token.text, label))
                            covered.append((token.idx, token.idx + len(token.text)))

    # Sort in reverse so char replacements don't shift positions
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