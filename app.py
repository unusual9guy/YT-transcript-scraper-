import os
import requests 
import re
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialise_params(api_key, link_id):    
    params = {
        "api_key" : api_key,
        "engine" : "youtube_video_transcript",
        "v" : link_id,
        "type" : "asr"
    }
    return params

def get_response(params):
    search = requests.get("https://serpapi.com/search", params=params)
    return search.json()

def get_transcript(response):
    transcript = ""
    for result in response.get("transcript", []):
        snippet = result.get("snippet", "")
        transcript = transcript + snippet + " "
    return transcript.strip()

def get_vID(yt_url):
    # Updated regex to handle standard and shortened (youtu.be) URLs
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    vId = re.search(pattern, yt_url)
    return vId.group(1) if vId else None

# --- STREAMLIT UI ---
def main():
    st.set_page_config(page_title="YouTube Transcriber", page_icon="📺")
    
    st.title("📺 YouTube Video Transcriber")
    st.markdown("Enter a YouTube URL below to extract the transcript using SerpAPI.")

    # Sidebar for API Key (optional if already in .env)
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input("Enter SerpAPI Key", type="password")

    yt_url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

    if st.button("Get Transcript"):
        if not api_key:
            st.error("Please provide a SerpAPI key (either in .env or the sidebar).")
        elif not yt_url:
            st.warning("Please enter a valid YouTube URL.")
        else:
            vId = get_vID(yt_url)
            
            if not vId:
                st.error("Could not extract Video ID. Please check the URL format.")
            else:
                with st.spinner("Fetching transcript..."):
                    params = initialise_params(api_key=api_key, link_id=vId)
                    response = get_response(params)
                    
                    if "error" in response:
                        st.error(f"API Error: {response.get('error')}")
                    else:
                        transcript = get_transcript(response)
                        
                        if transcript:
                            st.subheader("Transcript Result")
                            st.text_area("Full Text", transcript, height=300)
                            
                            # Download button
                            st.download_button(
                                label="Download Transcript as Text",
                                data=transcript,
                                file_name=f"transcript_{vId}.txt",
                                mime="text/plain"
                            )
                        else:
                            st.info("No transcript found for this video. It might have transcripts disabled or be a very short video.")

if __name__ == "__main__":
    main()