import streamlit as st
import requests
from gtts import gTTS

# Define the Streamlit app
st.title("YouTube Summarizer")

# Define the input form
form = st.form(key="input_form")

# Get the video ID from the URL
video_url = form.text_input("Enter a YouTube video URL")


# Define the FastAPI endpoint URL
endpoint_url = "http://localhost:8000/summarize"

# Define a function that sends a POST request to the endpoint
def summarize_video(video_url):
    data = {"video_url": video_url}
    response = requests.post(endpoint_url, json=data, timeout=None)
    summary = response.json()["summary"]
    return summary

# Submit button
submit_button = form.form_submit_button("Summarize Video")

# Handle form submissions
if submit_button:
    # Call the summarize_video function to get the summary
    summary = summarize_video(video_url)

    # Display the summary to the user
    st.subheader("Summary")
    st.write(summary)

    # Convert text summary into audio
    tts = gTTS(summary)
    print("converting text to audio")
    tts.save('hello.mp3')

    # Download audio transcript 
    with open('hello.mp3', 'rb') as f:
        st.download_button('Download mp3', f, file_name='hello.mp3')

