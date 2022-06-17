
import os
import math
from pathlib import Path

import numpy as np
import keras
import ffmpeg


MODEL_PATH = "../data/model_17-06-22 15-47-36.h5"
INPUT_FILE = "../data/country/uncut/1rbJ0eoRVt0.webm"
INPUT_LABEL = "country"

def do_prediction():
    model = keras.models.load_model(MODEL_PATH)
    absolute_filepath = os.path.abspath(INPUT_FILE)

    result = ffmpeg.probe(absolute_filepath)
    duration = float(result.get("format", {}).get("duration", "0.0"))
    if duration < 91.0 or duration > 420.0:
        print("AaaaaaAAAAAAA too short :(((")
        return
    
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

if __name__ == "__main__":
    do_prediction()
