import os
import requests 
from dotenv import load_dotenv
import re

load_dotenv()

def initialise_params(api_key, link_id):    
    # Parameters for the YT Scraper api 
    params = {
        "api_key" : api_key,
        "engine" : "youtube_video_transcript",
        "v" : link_id,
        "type" : "asr"
    }

    return params

def get_response(params):
    # Caliing the actual API 
    search = requests.get("https://serpapi.com/search", params=params)
    # Converting the search request into json 
    response = search.json()
    return response

def get_transcript(response):
    # Looping through the response to get only the transcript from the response
    transcript = ""
    for result in response.get("transcript", []):
        snippet = result.get("snippet", [])
        transcript = transcript + snippet + " "
        # print(f"{snippet}")
        # print("--" * 10)
    return transcript

def get_vID(yt_url):
    # Regex pattern to extract the video ID needed for serpAPI
    pattern = r'(?:https?:\/\/)?(?:www\.|m\.)?(?:youtu\.be\/|youtube\.com\/watch\?v=)([\w-]{11})'
    vId = re.search(pattern, yt_url)

    if vId:
        return vId.group(1)
    else:
        return None



def main():
    yt_url =  input("Enter the YT link you want to transcribe:")
    vId = get_vID(yt_url=yt_url)

    if not vId:
        print("No vId found")

    else:
        api_key = os.getenv("SERPAPI_API_KEY")
        params = initialise_params(api_key=api_key,link_id=vId)
        
        # Getting response from the api call 
        response = get_response(params=params)

        # Getting only the transcript
        transcript = get_transcript(response=response)
        print(f"The transcript for the video link '{yt_url}' is : {transcript}")   

    

if __name__ == "__main__":
    main()