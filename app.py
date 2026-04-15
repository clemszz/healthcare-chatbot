import streamlit as st
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from mistralai.client import MistralClient

# ===== ENV =====
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    st.error("Clé API manquante")
    st.stop()

client = MistralClient(api_key=api_key)

# ===== CONFIG =====
st.set_page_config(page_title="Assistant Santé Travail", page_icon="🩺")

# ===== STYLE (FIX LISIBILITÉ) =====
st.markdown("""
<style>
.block-container {
    max-width: 800px;
}

/* Texte global */
html, body, [class*="css"] {
    color: #000000 !important;
}

/* Bulles */
.user-bubble {
    background-color: #DCF8C6;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}

.bot-bubble {
    background-color: #F1F0F0;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}

.name {
    font-size: 12px;
    color: grey;
}
</style>
""", unsafe_allow_html=True)

# ===== INTENTS =====
@dataclass
class Intent:
    name: str
    keywords: list[str]
    orientation: str

INTENTS = [
    Intent("rdv", ["rdv", "rendez-vous", "visite"],
           "Oriente vers la prise de rendez-vous avec la médecine du travail."),
    
    Intent("medecin", ["douleur", "mal", "blessure"],
           "Oriente vers un professionnel de santé ou médecin du travail."),
    
    Intent("stress", ["stress", "fatigue", "burnout"],
           "Oriente vers un accompagnement RH ou cellule de soutien."),
    
    Intent("poste", ["poste", "ergonomie", "aménagement"],
           "Oriente vers les équipes internes pour adaptation du poste."),
]

WELCOME = "Bonjour, comment puis-je vous aider ? 🙂"

# ===== NLP =====
def detect_intent(text):
    text = text.lower()
    for intent in INTENTS:
        for k in intent.keywords:
            if k in text:
                return intent
    return None

# ===== LLM =====
def generate_response(user_input):
    intent = detect_intent(user_input)

    system_prompt = """
Tu es un assistant en santé au travail en entreprise.

OBJECTIF :
- Orienter l’utilisateur vers les bonnes actions
- Donner des réponses concrètes et professionnelles

RÈGLES :
- Pas de diagnostic médical
- Toujours proposer une orientation claire (médecin, RH, pôle interne, etc.)
- Réponse courte et structurée
- Maximum 1 emoji léger (🙂)
- Ton professionnel
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    if intent:
        messages.append({
            "role": "system",
            "content": f"Contexte : {intent.orientation}"
        })

    messages.append({"role": "user", "content": user_input})

    response = client.chat(
        model="mistral-small",
        messages=messages
    )

    return response.choices[0].message.content

# ===== SESSION =====
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME}
    ]

# ===== UI =====
st.title("🩺 Assistant Santé Travail")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='name'>Vous</div><div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='name'>Assistant</div><div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# ===== INPUT =====
user_input = st.chat_input("Décrivez votre situation...")

# ===== PROCESS =====
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Analyse..."):
        reply = generate_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ===== FOOTER =====
st.markdown("---")
st.caption("Assistant interne - orientation uniquement")
