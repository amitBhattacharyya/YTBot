from googleapiclient.discovery import build
import os
import sys

# ---- Configuration ----
# Read API key from environment variable `YOUTUBE_API_KEY` (no hardcoded default)
API_KEY = os.getenv("YOUTUBE_API_KEY")
MAX_RESULTS = 5                   # number of videos to return
# ---- Function to perform the search and return the API response ----
def search_youtube(search_query, api_key=None, max_results=MAX_RESULTS, region_code="US"):
    """Perform a YouTube search and return the raw API response.

    Args:
        search_query (str): Query string to search for (required).
        api_key (str, optional): YouTube Data API key. If omitted, the
            function will use the `YOUTUBE_API_KEY` environment variable.
        max_results (int): Number of results to return.
        region_code (str): ISO 3166-1 alpha-2 country code to bias results.

    Returns:
        dict: Raw API response from YouTube Data API v3.
    """
    if not search_query:
        raise ValueError("search_query is required and cannot be empty")

    api_key = api_key or API_KEY
    if not api_key:
        raise ValueError("API key not provided. Set YOUTUBE_API_KEY env var or pass api_key argument")

    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",          # only return videos (omit for channels/playlists)
        maxResults=max_results,
        order="relevance",
        regionCode=region_code
    )
    response = request.execute()
    return response

# ---- Print results (commented out for future reference) ----
# for item in response.get("items", []):
#     video_id = item["id"]["videoId"]
#     title = item["snippet"]["title"]
#     channel = item["snippet"]["channelTitle"]
#     url = f"https://www.youtube.com/watch?v={video_id}"
#     print(f"Title: {title}\nChannel: {channel}\nURL: {url}\n")

if __name__ == "__main__":
    # Example usage: provide the search query as command-line args:
    #   python sampleYtConnection.py acer nitro review
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        response = search_youtube(query)
        # Response is available in `response`; printing is intentionally
        # commented out above for future reference.
    else:
        print("Please provide a search query as command-line arguments.")
