import streamlit as st
import requests
from gtts import gTTS
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import unicodedata
from deepmultilingualpunctuation import PunctuationModel
from transformers import pipeline


def summarize_video(url):
  
  if "watch" in url:
    pass
  else:
    url = url.replace("youtu.be/", "www.youtube.com/watch?v=")

  parsed_url = urlparse(url)
  video_id = parse_qs(parsed_url.query)['v'][0]

  # Get the transcript 
  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  # Combining all the lists into on unique list
  text = []
  for i in range(0, len(transcript)):
      text.append(transcript[i]["text"])

  # Join list items into one paragraph
  video_transcript = " ".join(text)
  print("Text transcript created")

  print(video_transcript)

  # Text normalization 
  my_string = unicodedata.normalize('NFKD', video_transcript)
  print("Text normalized")


  # Add punctuation 
  model = PunctuationModel()
  result = model.restore_punctuation(video_transcript)
  print("Punctuation restored")

  # SUMMARIZATION 

  # instantiate the summarization pipeline
  summarization_pipeline = pipeline(
      "summarization", 
      model="t5-base", # you can choose a different model, depending on your requirements
      tokenizer="t5-base" # you can choose a different tokenizer, depending on your requirements
  )

  # define the input text to summarize
  input_text = result

  # split the input text into smaller chunks
  chunk_size = 5000
  chunks = [input_text[i:i+chunk_size] for i in range(0, len(input_text), chunk_size)]

  # summarize each chunk separately
  summaries = []
  for chunk in chunks:
      summary = summarization_pipeline(chunk, max_length=200, min_length=30, do_sample=False)
      summaries.append(summary[0]['summary_text'])

  # combine the summaries of all chunks into a single summary
  final_summary = " ".join(summaries)

  # print the generated summary
  return final_summary

# Define the Streamlit app
st.title("YouTube Summarizer")

# Define the input form
form = st.form(key="input_form")

# Get the video ID from the URL
video_url = form.text_input("Enter a YouTube video URL")

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




    