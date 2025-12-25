import streamlit as st
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = """You are a helpful assistant.
Summarize the following YouTube transcript clearly and concisely:

"""
import youtube_transcript_api
print(youtube_transcript_api.__file__)


def generate_gemini_content(transcript_text):
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        PROMPT + transcript_text,
        generation_config={
            "max_output_tokens": 1024,
            "temperature": 0.3
        }
    )
    return response.text


def extract_transcript_details(video_url):
    video_id = video_url.split("v=")[-1].split("&")[0]
    print(video_id)
    transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    transcript_text = " ".join([entry['text'] for entry in transcript_data])
    return transcript_text


# ---------------- STREAMLIT UI ----------------

st.title("🎥 YouTube Transcript Summarizer (Gemini)")

youtube_url = st.text_input("Enter YouTube Video URL")

if youtube_url:
    video_id = youtube_url.split("v=")[-1].split("&")[0]
    print(video_id)
    st.image(
        f"https://img.youtube.com/vi/{video_id}/0.jpg",
        caption="Video Thumbnail",
        use_container_width=True
    )

if st.button("Generate Summary"):
    with st.spinner("Fetching transcript & summarizing..."):
        transcript_text = extract_transcript_details(youtube_url)

        summary = generate_gemini_content(transcript_text)

        st.subheader("📄 Generated Summary")
        st.write(summary)