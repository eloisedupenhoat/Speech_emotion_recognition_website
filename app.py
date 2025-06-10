import streamlit as st # Used to build the webpage
import requests # Sends HTTP requests to the backend API for emotion prediction

# ---------------------- Page Setup ----------------------
# Sets the page title in the browser tab and centres the layout
st.set_page_config(page_title="Speech Emotion Recognition", layout="centered")

# ---------------------- Custom CSS for Styling ----------------------
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    .emotion-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Title ----------------------
st.title("🎙️ Speech Emotion Recognition") # Display the app title
st.markdown("Téléversez un fichier **.wav** pour détecter l’émotion exprimée dans la voix.") # Markdown instruction

# ---------------------- File Upload ----------------------
uploaded_file = st.file_uploader("Choisissez un fichier .wav", type=["wav"]) # File uploader that accepts .wav audio files only

# ---------------------- Prediction Button ----------------------
if uploaded_file is not None: # If a user uploads a file, it is played with a streamlit audio player
    st.audio(uploaded_file, format='audio/wav')

    if uploaded_file.type != "audio/wav": # If the audio file is different from .wav
        st.warning("⚠️ Veuillez téléverser un fichier au format .wav uniquement.") # Warn the user to only upload .wav files
    else: # Else, run this code
        if st.button("Faire une prédiction 🎯"): # Shows a prediction button named "Faire une prédiction" (all the rest only runs if this button is clicked)
            with st.spinner("⏳ Envoi à l'API..."): # Includes a loading spinner
                files = {'my_file': uploaded_file} # Prepares the file to be sent in the POST request
                api_url = "http://localhost:8001/predict" # The url of the prediction API

                try: # Tries to run this code
                    response = requests.post(api_url, files=files) # Sends the POST request to the API (to the prediciton URL with the uploaded audio file) and stores it in a response variable
                    response.raise_for_status() # Checks if there's an error

                    try: # Tries to run this code
                        result = response.json() # Stores the POST request response (a JSNON file) as a python dictionary
                        emotion = result.get("emotion", "inconnue") # Extracts the emotion key from the response dictionary

                        emotion_emoji = { # Map the various emotion results with a corresponding emoji
                            "angry": "😠",
                            "happy": "😊",
                            "sad": "😢",
                            "neutral": "😐",
                            "fearful": "😱",
                            "disgust": "🤢",
                            "surprised": "😲"
                        }
                        emoji = emotion_emoji.get(emotion.lower(), "") # Gets the corresponding emoji for the returned emotion
                        # CSS markdown to send a return message to the user
                        st.markdown(f"""
                            <div class="emotion-box">
                                L'émotion prédite est : {emotion} {emoji}
                            </div>
                        """, unsafe_allow_html=True)

                    except requests.exceptions.JSONDecodeError: # If something goes wrong instead of crashing, run this block
                        st.error("❌ Erreur : la réponse de l'API n'est pas au format JSON.")
                        st.text(f"Réponse brute : {response.text}")

                except requests.exceptions.RequestException as e: # If something goes wrong instead of crashing, run this block
                    st.error("❌ Erreur lors de l'appel à l'API.")
                    st.text(str(e))
