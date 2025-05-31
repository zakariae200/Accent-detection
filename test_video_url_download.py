import yt_dlp
import os
from pathlib import Path

def download_video(url, output_path='downloads', filename=None):
    """
    Downloads a video from the given URL using yt-dlp.

    Parameters:
    - url (str): The URL of the video to download.
    - output_path (str): The directory where the video will be saved.
    - filename (str, optional): Custom filename for the downloaded video (without extension).
    
    Returns:
    - str: Path to the downloaded video file
    """
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Set up output template based on whether a custom filename is provided
    if filename:
        output_template = os.path.join(output_path, f"{filename}.%(ext)s")
    else:
        output_template = os.path.join(output_path, '%(title)s.%(ext)s')

    # Set up yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio quality
        'outtmpl': output_template,  # Output filename template
        'merge_output_format': 'mp4',  # Merge video and audio into mp4 format
        'quiet': False,  # Set to True to suppress output
        'noplaylist': True,  # Download only the single video, not a playlist
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"Starting download for: {url}")
            ydl.download([url])
            print("Download completed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

