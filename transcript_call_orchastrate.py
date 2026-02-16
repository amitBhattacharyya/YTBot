import os
from persist_transcript import read_text_from_file
from persist_transcript import save_text_to_file
from call_transcript_api import get_transcript


# this will first check local storage for transcript if not found then call the transcript api
# And save the transcript in local storage for future use
def get_cached_transcript(video_id):
    base_location = os.environ.get("STORAGE_LOCATION")
    
    full_transcript = read_text_from_file(base_location + video_id + ".txt")
    
    if full_transcript:
        print("\n--- Transcript Retrieved from Local Storage! ---\n")
        return full_transcript
    
    full_transcript = call_transcript_api_monthly_100(video_id)
    save_text_to_file(full_transcript, base_location + video_id + ".txt")
    return full_transcript


    
# this call is monthly 100 free only , in side the  method there can be multiple keys maintained for rotaion
def call_transcript_api_monthly_100(video_id):
    full_transcript = ""    
    data = get_transcript(video_id)    
    transcript = data["transcript"]    
    for segment in transcript:
        full_transcript += segment['text'] + " "                    
    return full_transcript

    
       

