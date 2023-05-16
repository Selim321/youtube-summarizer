
from fastapi import FastAPI
from fastapi import Request, Body
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import unicodedata
from deepmultilingualpunctuation import PunctuationModel
from transformers import pipeline


# Define the FastAPI app
app = FastAPI()


# Define the endpoint that summarizes a YouTube video
@app.post("/summarize")
async def summarize(request:Request,video_url: str = Body(..., embed=True)):

    parsed_url = urlparse(video_url)
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
    print(final_summary)

    # Return the summary
    return {"summary": final_summary}

    