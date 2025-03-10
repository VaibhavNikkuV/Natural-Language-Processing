import streamlit as st
import pandas as pd
import requests
from io import BytesIO

prediction_endpoint = "http://127.0.0.1:5000/predict"

st.title("Text Sentiment Predictor")

uploaded_file = st.file_uploader(
    "Choose a csv file for bulk prediction - upload the file and click on predict",
    type='csv'
)

#Text input for Sentiment analysis
user_input = st.text_input("Enter text and click on predict","")

if st.button("Predict"):
    if uploaded_file is not None:
        file = {"file": uploaded_file}
        response = requests.post(prediction_endpoint, files=file)
        response_bytes = BytesIO(response.content)
        response_df = pd.read_csv(response_bytes)

        st.download_button(
            label="Download Predictions",
            data=response_bytes,
            file_name="Predictions.csv",
            key="result_download_button",
        )

    else:
        response = requests.post(prediction_endpoint, data={"text": user_input})
        response = response.json()
        st.write(f"Predicted sentiment: {response['prediction']}")