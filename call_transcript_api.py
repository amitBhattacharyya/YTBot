import os
import requests
import json

# Configuration
API_KEY = os.environ.get("TRANSCRIPT_API_KEY")

BASE_URL = os.environ.get("TRANSCRIPT_API_BASE_URL")

def get_transcript(video_url, format="json", include_timestamp=False, send_metadata=True):
    """Fetch YouTube video transcript"""

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "video_url": video_url,
        "format": format,
        "include_timestamp": include_timestamp,
        "send_metadata": send_metadata
    }

    try:
        response = requests.get(
            f"{BASE_URL}/youtube/transcript",
            headers=headers,
            params=params
        )

        # Check for errors
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Handle different formats
        #if format == "json":
        #    transcript = data["transcript"]
        #    if include_timestamp:
        #        for segment in transcript:
        #            print(f"[{segment['start']}s] {segment['text']}")
        #    else:
        #        for segment in transcript:
        #            print(segment['text'])
        #else:
        #    # Text format
        #    print(data["transcript"])

        return data

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 402:
            error_data = e.response.json()
            print(f"Payment required: {error_data['detail']['message']}")
            print(f"Action: {error_data['detail']['action_url']}")
        elif e.response.status_code in (408, 429, 503):
            # Retryable errors - implement backoff
            retry_after = e.response.headers.get('Retry-After', '5')
            print(f"Retryable error ({e.response.status_code}). Retry after {retry_after} seconds")
        elif e.response.status_code == 404:
            print("Video not found or has no transcript available")
        else:
            print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Error: {e}")
