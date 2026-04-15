import streamlit as st
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import Optional
import time

st.set_page_config(
    page_title="Assistant Santé Travail",
    page_icon="🩺",
    layout="centered"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True

@dataclass
class Intent:
    name: str
    keywords: list[str]
    response: str
    icon: str


INTENTS = [
    Intent(
        "rdv",
        ["rdv", "rendez-vous", "visite", "convocation"],
        """**Je peux vous aider à organiser un rendez-vous.**

👉 Contactez le service de santé au travail ou votre employeur.

Souhaitez-vous plus de détails ?""",
        "📅"
    ),
    Intent(
        "medecin",
        ["douleur", "mal", "blessure", "dos", "tête"],
        """**Je comprends votre situation.**

👉 Il est recommandé de consulter un médecin du travail.

Pouvez-vous préciser votre problème ?""",
        "🩺"
    ),
    Intent(
        "stress",
        ["stress", "fatigue", "burnout", "pression"],
        """**Le stress au travail est important à prendre en compte.**

👉 Des dispositifs d’accompagnement existent.

Souhaitez-vous être orienté ?""",
        "🧠"
    ),
    Intent(
        "poste",
        ["poste", "ergonomie", "chaise", "aménagement"],
        """**Un aménagement de poste peut être envisagé.**

👉 Ergonomie, matériel adapté, organisation.

Voulez-vous savoir comment faire la demande ?""",
        "🪑"
    ),
]

DEFAULT_RESPONSE = """Je suis là pour vous aider.

Vous pouvez :
- 📅 Prendre un rendez-vous  
- 🩺 Parler d’un problème de santé  
- 🧠 Gérer du stress  
- 🪑 Adapter votre poste  

Pouvez-vous préciser ?"""

WELCOME_MESSAGE = """Bienvenue 👋  

Je suis un assistant d’orientation en santé au travail.  

⚠️ *Je ne remplace pas un avis médical.*

Comment puis-je vous aider aujourd’hui ?"""

SIMILARITY_THRESHOLD = 0.6


def normalize(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str) -> list[str]:
    for char in ".,;:!?'\"()-":
        text = text.replace(char, " ")
    return [w for w in text.split() if len(w) > 2]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_intent(user_input: str) -> Optional[Intent]:
    normalized_input = normalize(user_input)

    for intent in INTENTS:
        for keyword in intent.keywords:
            if keyword in normalized_input:
                return intent

    input_words = tokenize(normalized_input)

    best_intent = None
    best_score = 0.0

    for intent in INTENTS:
        for input_word in input_words:
            for keyword in intent.keywords:
                score = similarity(input_word, keyword)
                if score > best_score:
                    best_score = score
                    best_intent = intent

    if best_score >= SIMILARITY_THRESHOLD:
        return best_intent

    return None


def generate_response(user_input: str) -> str:
    intent = detect_intent(user_input)

    # mini mémoire
    if "stress" in user_input.lower() and "manager" in user_input.lower():
        return """🧠 Vous évoquez un stress lié à votre environnement de travail.

👉 Cela peut relever des risques psychosociaux.

Je vous recommande :
- d’en parler au médecin du travail
- ou à un référent RH

Souhaitez-vous que je vous guide ?"""

    if intent:
        return f"{intent.icon} {intent.response}"

    return DEFAULT_RESPONSE



if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]



st.title("🩺 Assistant Santé Travail")
st.caption("Orientation et information santé au travail")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if len(st.session_state.messages) <= 3:
    st.markdown("### 💡 Actions rapides")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    if col1.button("📅 Rendez-vous"):
        user_input = "Je veux un rendez-vous"
    elif col2.button("🩺 Santé"):
        user_input = "J’ai une douleur"
    elif col3.button("🧠 Stress"):
        user_input = "Je suis stressé"
    elif col4.button("🪑 Poste"):
        user_input = "Problème de poste"
    else:
        user_input = None
else:
    user_input = None

text_input = st.chat_input("Décrivez votre situation...")

if text_input:
    user_input = text_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response = generate_response(user_input)

        placeholder = st.empty()
        full_text = ""

        for word in response.split():
            full_text += word + " "
            placeholder.markdown(full_text + "▌")
            time.sleep(0.01)

        placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()


st.markdown("---")
st.caption("💡 Démonstrateur technique — ne remplace pas un professionnel de santé")
