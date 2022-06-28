"""This program uses yt_dlp (youtube_dl fork) to download videos from a bunch of playlists.

It neatly saves them in folders categorized by genre.
"""

from yt_dlp import YoutubeDL

from config import TARGET_PLAYLIST_GENRES

def execute_download():
    for genre in TARGET_PLAYLIST_GENRES:
        # Use YoutubeDL to download the file and save it in the correct location
        ydl = YoutubeDL({
            "outtmpl": f"../data/{genre}/uncut/%(id)s.%(ext)s",
            "ignoreerrors": True,

            # Only download the audio
            "format": "bestaudio/best",
        })
        ydl.download(TARGET_PLAYLIST_GENRES[genre])

if __name__ == "__main__":
    execute_download()

