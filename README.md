# PrivacyShield AI

My friend once picked up my phone and scrolled through my ChatGPT history.

In that one moment I realized that everything was there. Things I'd asked 
about. People I'd mentioned. Places. Problems. All of it, sitting in 
some company's server, readable by anyone who gets close enough.

That scared me. So I built this.

---

## What it does

Every time you use ChatGPT, Gemini, or any cloud AI - your words leave 
your device. Names, locations, companies, health issues, personal 
situations - all of it reaches a server you don't control.

PrivacyShield sits between you and the AI. Before your message leaves 
your computer, it finds every piece of personal information and replaces 
it with a code. The AI sees the code. Never the real thing. When the 
answer comes back, your app swaps the codes back to real namesn - locally, 
on your machine.

The AI answered your question. But it never knew who you were talking about.

---

## How it actually works

You type this:
Anupriya who works at Google wants to apply at Microsoft

Your computer reads it locally and masks it:
[[PERSON_0]] who works at [[ORG_0]] wants to apply at [[ORG_1]]

This safe version goes to the AI. AI replies:
[[PERSON_0]] should apply through [[ORG_1]]'s careers page

This app decodes it back:

The AI helped. The AI never knew who Anupriya was.

---

## Who needs this

Everyone who has ever typed something personal into an AI and immediately 
thought — *wait, should I have done that?*

Lawyers who can't share client details. Doctors who can't type patient 
names. Students sharing sensitive situations. Anyone who values the 
difference between getting help and giving away their life.

---

## Tech Stack

| | |
|--|--|
| PII Detection | spaCy (runs 100% locally) |
| AI Backend | Groq API — llama-3.3-70b |
| Interface | Streamlit |
| Privacy Layer | Custom masking engine |

The important part — spaCy runs on your machine. Nothing sensitive 
touches any server.

---

## Run it yourself

```bash
git clone https://github.com/Anupriya2804/PrivacyShield-AI.git
cd PrivacyShield-AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create a `.env` file: 
GROQ_API_KEY=your_key_here

Get your free Groq key at [console.groq.com](https://console.groq.com)

Then run:

```bash
streamlit run app.py
```

---

## What's next

- Support for more languages
- Custom entity types — financial data, medical terms
- Browser extension so it works everywhere, not just this app
- Offline mode — fully local AI so nothing leaves your device ever

---

## Built by

Anupriya — CS undergrad, Ex-intern DRDO, building things that actually matter

[GitHub](https://github.com/Anupriya2804) · [LinkedIn](https://linkedin.com/in/anupriya-sihag)
