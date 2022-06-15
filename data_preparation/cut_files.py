
import math
import os
from pathlib import Path

import ffmpeg

DATA_DIR = "../data/"

# Make 80/10/10 train/validation/test set
# Make folders for train, validation and test sets
# Cut the files and put them in the folders

def execute_cut():
    genres = [name for name in os.listdir(DATA_DIR)]
    for genre in genres:
        base_data_dir = f"../data/{genre}"
        uncut_dir = base_data_dir + "/uncut"
        train_dir = base_data_dir + "/cut/train"
        validation_dir = base_data_dir + "/cut/validation"
        test_dir = base_data_dir + "/cut/test"
        
        song_amount = len([name for name in os.listdir(uncut_dir)])
        train_amount = math.floor(song_amount / 100 * 80) # 80%
        validation_amount = math.floor(song_amount / 100 * 10) # 10%

        if os.path.exists(uncut_dir):
            # For each uncut (full) song
            for root, dirs, files in os.walk(uncut_dir):
                for index, file in enumerate(files):
                    filename_without_extension = ".".join(file.split(".")[:-1])
                    filepath = os.path.join(root, file)
                    absolute_filepath = os.path.abspath(filepath)

                    # Only convert videos that are longer than 91 seconds and shorter than 7min
                    result = ffmpeg.probe(absolute_filepath)
                    duration = float(result.get("format", {}).get("duration", "0.0"))
                    if duration < 91.0 or duration > 420.0:
                        continue
                    
                    target_output_dir = train_dir
                    if index + 1 > train_amount:
                        if index + 1 > train_amount + validation_amount:
                            target_output_dir = test_dir
                        else:
                            target_output_dir = validation_dir

                    # Cut into 30s pieces and convert to .wav, removing the 1st and last piece
                    for i in range(math.ceil(duration / 30) - 3):
                        output_dir = Path(os.path.join("", target_output_dir, f"{filename_without_extension}/"))

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
                            .global_args('-loglevel', 'error')
                            .global_args('-y')
                            .run()
                        )
                    print(f"CUT: {genre}/{file} into {math.ceil(duration / 30) - 3} pieces")

if __name__ == "__main__":
    execute_cut()
