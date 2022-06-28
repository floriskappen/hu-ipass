"""This program uses yt_dlp (youtube_dl fork) to download videos from a bunch of playlists.

It neatly saves them in folders categorized by genre.
"""

from yt_dlp import YoutubeDL


def execute_download(custom_target_playlist_genres = None, data_dir = "../data"):
    if custom_target_playlist_genres:
        target_playlist_genres = custom_target_playlist_genres
    else:
        from config import TARGET_PLAYLIST_GENRES
        target_playlist_genres = TARGET_PLAYLIST_GENRES

    for genre in target_playlist_genres:
        # Use YoutubeDL to download the file and save it in the correct location
        ydl = YoutubeDL({
            "outtmpl": f"{data_dir}/{genre}/uncut/%(id)s.%(ext)s",
            "ignoreerrors": True,

            # Only download the audio
            "format": "bestaudio/best",
        })
        ydl.download(target_playlist_genres[genre])

if __name__ == "__main__":
    execute_download()

