import streamlit as st
import requests

'''
# SPEECH EMOTION RECOGNITION
'''

uploaded_file = st.file_uploader("Choose a .wav file")
if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')

    if st.button('Make prediction'):
        with st.spinner("Envoi à l'API..."):
            st.snow()
            st.balloons()
            files = {'file': uploaded_file}
            api_url = "http://localhost:8000/predict"  # A corriger avec la bonne API
            response = requests.post(api_url, files=files)

result = response.json()
emotion = result.get("emotion", "inconnue")

# streamlit run app.py --> Pour regarder ce que ça donne
# https://docs.streamlit.io/
# https://streamlit.lewagon.ai/
