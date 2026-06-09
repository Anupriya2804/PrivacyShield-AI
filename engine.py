import spacy

# --- SAFE LAZY-LOADING FOR CLOUD DEPLOYMENT ---
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If Streamlit Cloud can't find it locally, load it directly from the official wheel URL
    model_url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl"
    nlp = spacy.load(model_url)

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