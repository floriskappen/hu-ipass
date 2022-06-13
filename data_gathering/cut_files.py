
import math
import os
from pathlib import Path

import ffmpeg

from config import TARGET_PLAYLIST_GENRES

def execute_cut():
    for genre in TARGET_PLAYLIST_GENRES:
        base_data_dir = f"../data/{genre}"
        uncut_dir = base_data_dir + "/uncut"
        cut_dir = base_data_dir + "/cut"

        if os.path.exists(uncut_dir):
            # For each uncut (full) song
            for root, dirs, files in os.walk(uncut_dir):
                for file in files:
                    filename_without_extension = ".".join(file.split(".")[:-1])
                    filepath = os.path.join(root, file)
                    absolute_filepath = os.path.abspath(filepath)

                    # Only convert videos that are longer than 30 sec
                    result = ffmpeg.probe(absolute_filepath)
                    duration = float(result.get("format", {}).get("duration", "0.0"))
                    if duration < 91.0:
                        continue

                    # Cut into 30s pieces and convert to .wav, removing the 1st and last piece
                    for i in range(math.ceil(duration / 30) - 3):
                        output_dir = Path(os.path.join("", cut_dir, f"{filename_without_extension}/"))
                        
                        # Create the directory if it does not yet exist
                        os.makedirs(output_dir, exist_ok=True)
                        
                        # Store new files in a folder in the cut dir with the video id as the folder name
                        output_filepath = Path(os.path.join(output_dir, f"{filename_without_extension}_{i}.wav"))

                        (
                            ffmpeg
                            .input(
                                absolute_filepath,
                                ss=float(30 * (i + 1)),
                                to=float(30 * (i + 2)) # Pieces of 30 seconds
                            )
                            .output(filename=output_filepath.absolute())
                            .overwrite_output()
                            .run_async()
                        )


if __name__ == "__main__":
    execute_cut()
