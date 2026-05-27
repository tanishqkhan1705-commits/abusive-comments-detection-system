# api.py
# This file fetches comments from YouTube and Reddit

import re

from googleapiclient.discovery import build

# ── PUT YOUR API KEYS HERE ────────────────────────────────────────────────────
YOUTUBE_API_KEY      = "AIzaSyCjQbJhX62wVK800LXnzT012XJuBgU25IM"       # from Google Cloud Console

# ─────────────────────────────────────────────────────────────────────────────


def get_youtube_comments(url):
    """
    Give it a YouTube video URL.
    Returns: list of comments, each comment is a dict with 'author' and 'text'
    """
    # Step 1: Pull the video ID out of the URL
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    video_id = match.group(1)

    # Step 2: Call the YouTube API
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50,
        textFormat="plainText"
    ).execute()

    # Step 3: Extract the comments
    comments = []
    for item in response.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet.get("authorDisplayName", "Unknown"),
            "text":   snippet.get("textDisplay", "")
        })
    return comments