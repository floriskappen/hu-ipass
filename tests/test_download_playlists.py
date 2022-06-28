
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data_gathering.download_playlists import execute_download

def test_download_playlists():
    execute_download({
        "test_genre": [
            "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        ]
    }, "data")

    files = os.listdir("data/test_genre/uncut")
    assert files[0] == "jNQXAC9IVRw.webm"

    os.remove("data/test_genre/uncut/jNQXAC9IVRw.webm")
    os.rmdir("data/test_genre/uncut")
    os.rmdir("data/test_genre")
