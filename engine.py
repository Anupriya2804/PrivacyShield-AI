import spacy

nlp = spacy.load("en_core_web_sm")

IGNORE_WORDS = {"intern", "engineer", "manager", "developer", "analyst",
                "director", "ceo", "cto", "associate", "consultant"}

def protect_data(text):
    doc = nlp(text)
    mapping = {}
    masked = text
    counters = {}

    # Step 1: Find proper noun subjects that spaCy might mislabel
    forced_person_texts = []
    for token in doc:
        if token.pos_ == "PROPN" and token.dep_ in ["nsubj", "nsubjpass", "flat"]:
            if token.text.lower() not in ["microsoft", "google", "amazon", "apple", "meta"]:
                forced_person_texts.append(token.text)

    # Step 2: Process entities
    entities = list(doc.ents)
    for ent in sorted(entities, key=lambda e: e.start_char, reverse=True):
        label = ent.label_
        ent_text = ent.text

        # Force PERSON if spaCy mislabelled a human name as PRODUCT or WORK_OF_ART
        if label in ["PRODUCT", "WORK_OF_ART"] and ent_text in forced_person_texts:
            label = "PERSON"

        # Skip job titles
        if ent_text.lower() in IGNORE_WORDS:
            continue

        counters[label] = counters.get(label, 0)
        placeholder = f"[[{label}_{counters[label]}]]"
        mapping[placeholder] = ent_text
        masked = masked[:ent.start_char] + placeholder + masked[ent.end_char:]
        counters[label] += 1

    return masked, mapping


def reveal_data(text, mapping):
    for placeholder, original_value in mapping.items():
        text = text.replace(placeholder, original_value)
    return text