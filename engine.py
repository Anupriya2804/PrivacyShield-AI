import spacy

nlp = spacy.load("en_core_web_sm")

def protect_data(text):
    doc = nlp(text)
    mapping = {}
    masked = text
    counters = {}

    for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
        label = ent.label_
        counters[label] = counters.get(label, 0)
        token = f"[[{label}_{counters[label]}]]"
        mapping[token] = ent.text
        masked = masked[:ent.start_char] + token + masked[ent.end_char:]
        counters[label] += 1

    return masked, mapping

def reveal_data(text, mapping):
    for token, original in mapping.items():
        text = text.replace(token, original)
    return text