import streamlit as st
import requests

# ---------------------- Page Setup ----------------------
st.set_page_config(page_title="Speech Emotion Recognition", layout="centered")

# ---------------------- Custom CSS ----------------------
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(
            rgba(255, 255, 255, 0.85),
            rgba(255, 255, 255, 0.85)
        ), url("https://www.xrtoday.com/wp-content/uploads/2022/01/What_Speech_Recognition_Technology_VR.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Segoe UI', sans-serif;
    }

    .stMarkdown p {
        font-size: 3rem !important;
        line-height: 3.8rem;
        text-align: center;
        max-width: 100%;
    }

    .stFileUploader {
        font-size: 2.8rem;
        padding: 3rem;
        margin-top: 2rem;
        margin-bottom: 3rem;
        max-width: none !important;
        width: 100% !important;
    }

    div[data-testid="stFileUploaderDropzone"] {
        min-width: 100% !important;
        padding: 3rem !important;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border: 3px dashed #aaa;
        border-radius: 1rem;
        font-size: 2.4rem;
        max-width: none !important;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 18px;
        padding: 2.6rem 5rem;
        font-size: 3.2rem;
        margin-top: 3rem;
        font-weight: 700;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.25);
    }

    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }

    .emotion-box {
        background-color: #d4edda;
        border-left: 12px solid #28a745;
        padding: 3rem;
        border-radius: 16px;
        font-weight: bold;
        font-size: 3.2rem;
        margin-top: 50px;
        text-align: center;
        box-shadow: 0px 6px 16px rgba(0,0,0,0.15);
        max-width: 100%;
    }

    audio {
        height: 120px;
        width: 100%;
        margin-top: 40px;
        margin-bottom: 50px;
        transform: scale(1.4);
    }

    section.main > div {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 5vw;
        padding-right: 5vw;
    }

    .element-container:has(.stFileUploader) {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Centered Title + Subtitle ----------------------
st.markdown("""
    <div style='
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 45vh;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    '>
        <h1 style='font-size:5.5rem; margin-bottom: 2rem;'>
            🎙️ <strong>Speech Emotion Recognition</strong>
        </h1>
        <p style='font-size: 3rem; line-height: 3.6rem; max-width: 90vw;'>
            Téléversez un fichier <strong>.wav</strong> pour détecter l’émotion exprimée dans la voix.
        </p>
    </div>
""", unsafe_allow_html=True)

# ---------------------- File Upload ----------------------
uploaded_file = st.file_uploader("Choisissez un fichier .wav", type=["wav"])

# ---------------------- Prediction Logic ----------------------
if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if uploaded_file.type != "audio/wav":
        st.warning("⚠️ Veuillez téléverser un fichier au format .wav uniquement.")
    else:
        if st.button("Faire une prédiction 🎯"):
            with st.spinner("⏳ Envoi à l'API..."):
                files = {'my_file': uploaded_file}
                api_url = "http://localhost:8001/predict"

                try:
                    response = requests.post(api_url, files=files)
                    response.raise_for_status()

                    try:
                        result = response.json()
                        emotion = result.get("emotion", "inconnue")

                        emotion_emoji = {
                            "angry": "😠",
                            "happy": "😊",
                            "sad": "😢",
                            "neutral": "😐",
                            "fearful": "😱",
                            "disgust": "🤢",
                            "surprised": "😲"
                        }
                        emoji = emotion_emoji.get(emotion.lower(), "")

                        st.markdown(f"""
                            <div class="emotion-box">
                                L'émotion prédite est : {emotion} {emoji}
                            </div>
                        """, unsafe_allow_html=True)

                    except requests.exceptions.JSONDecodeError:
                        st.error("❌ Erreur : la réponse de l'API n'est pas au format JSON.")
                        st.text(f"Réponse brute : {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error("❌ Erreur lors de l'appel à l'API.")
                    st.text(str(e))
