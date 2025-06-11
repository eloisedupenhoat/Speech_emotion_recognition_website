import streamlit as st
import requests
import pandas as pd
import base64

# ---------------------- Page Setup ----------------------
st.set_page_config(page_title="Speech Emotion Recognition", layout="centered")

# ---------------------- Global Styling ----------------------
def set_background(image_path, opacity=0.5):
    # Read the image file and encode it to base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # Construct the CSS style with the correct data URL based on the image format
    css = f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{encoded_string}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-blend-mode: normal; /* Adjust blend mode if needed */
        opacity: {opacity}; /* Adjust opacity level */
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Path to your background image (change this to your actual image path)
background_image_path = 'static/bg.jpg'

# Set background with desired opacity (e.g., 0.5)
set_background(background_image_path, opacity=1)

st.markdown("""
    <style>
    /* Boost all font sizes */
    html, body, .stApp {
        font-size: 38px !important;
        line-height: 1.6;
    }

    /* Title styling */
    h1 {
        font-size: 70px !important;
        font-weight: 900;
        text-shadow: 2px 2px 4px #000;
        text-align: center;
        margin-bottom: 40px;
    }

    /* Form labels and text */
    label, .stMarkdown, .css-1v0mbdj, .css-10trblm {
        font-size: 36px !important;
        text-shadow: 1px 1px 3px #000;
    }

    /* Buttons */
    .stButton > button {
        font-size: 40px !important;
        padding: 1.2em 2.5em;
        border-radius: 12px;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        box-shadow: 2px 2px 8px #00000055;
    }

    .stButton > button:hover {
        background-color: #0056b3;
    }

    /* Emotion result box */
    .emotion-box {
        font-size: 44px;
        margin-top: 50px;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000;
    }

    /* Adjust uploader text */
    .uploadedFileName, .css-1cpxqw2 {
        font-size: 32px !important;
    }

    /* Bar chart text */
    .css-1aumxhk {
        font-size: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Title ----------------------
st.title("🎙️ Speech Emotion Recognition")
st.markdown("Téléversez un fichier **.wav** pour détecter l’émotion exprimée dans la voix.")

# ---------------------- File Upload ----------------------
uploaded_file = st.file_uploader("Choisissez un fichier .wav", type=["wav"])

# ---------------------- Prediction Button ----------------------
if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if uploaded_file.type != "audio/wav":
        st.warning("⚠️ Veuillez téléverser un fichier au format .wav uniquement.")
    else:
        if st.button("Faire une prédiction 🎯"):
            with st.spinner("⏳ Envoi à l'API..."):
                files = {'my_file': uploaded_file}
                api_url = st.secrets["API_URL"] + "/predict/"

                try:
                    response = requests.post(api_url, files=files)
                    response.raise_for_status()

                    try:
                        result = response.json()
                        predicted_emotion = result.get("emotion", "inconnue")
                        probabilities = result.get("probabilities", {})

                        emotion_emoji = {
                            "angry": "😠",
                            "happy": "😊",
                            "sad": "😢",
                            "neutral": "😐",
                            "fearful": "😱",
                            "disgust": "🤢",
                            "surprised": "😲"
                        }
                        emoji = emotion_emoji.get(predicted_emotion.lower(), "")

                        # Predicted emotion
                        st.markdown(
                            f"<div class='emotion-box'>L'émotion prédite est : {predicted_emotion.upper()} {emoji}</div>",
                            unsafe_allow_html=True
                        )

                        # Probabilities
                        if probabilities:
                            st.markdown("### 📊 Probabilités pour chaque émotion")
                            prob_df = pd.DataFrame({
                                "Émotion": list(probabilities.keys()),
                                "Probabilité": list(probabilities.values())
                            })
                            st.bar_chart(prob_df.set_index("Émotion"))

                    except requests.exceptions.JSONDecodeError:
                        st.error("❌ Erreur : la réponse de l'API n'est pas au format JSON.")
                        st.text(f"Réponse brute : {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error("❌ Erreur lors de l'appel à l'API.")
                    st.text(str(e))
