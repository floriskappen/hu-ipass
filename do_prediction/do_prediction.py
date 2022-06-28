
import os
import math
from pathlib import Path
import sys

import numpy as np
import keras
import ffmpeg
from yt_dlp import YoutubeDL


DATA_DIR = "../data/"
MODEL_PATH = "../data/model_22-06-22_22-31-46.h5"
INPUT_URL_ID = "Y1_VsyLAGuk"
INPUT_LABEL = "electronic"

# Will be removed after prediction is done
TEMP_OUTPUT_DIR = "../data/temp.output/"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from data_preprocessing.extract_mfcc import extract_one_file_mfcc
from data_preprocessing.utils import get_mfcc

def do_prediction():
    input_file = TEMP_OUTPUT_DIR + download_file(INPUT_URL_ID, TEMP_OUTPUT_DIR)

    genres = [name for name in os.listdir(DATA_DIR) if "." not in name]

    model = keras.models.load_model(MODEL_PATH)
    absolute_filepath = os.path.abspath(input_file)

    result = ffmpeg.probe(absolute_filepath)
    duration = float(result.get("format", {}).get("duration", "0.0"))
    if duration < 91.0 or duration > 420.0:
        print("Audio file is too short")
        return

    filename_without_extension = input_file.split("/")[-1].split(".")[0]

    predictions = []

    output_dir = Path(os.path.join("", TEMP_OUTPUT_DIR, f"{filename_without_extension}/"))
    os.makedirs(output_dir, exist_ok=True)
    
    # Cut into 30s pieces and convert to .wav, removing the 1st and last piece
    for i in range(math.ceil(duration / 30) - 3):

        # Create the directory if it does not yet exist
        
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

        def helper_get_mfcc(**kwargs):
            mfccs = get_mfcc(**kwargs)
            return mfccs.T
        mfccs = extract_one_file_mfcc(helper_get_mfcc, str(output_filepath.absolute()))
        prediction = model.predict(mfccs)
        predicted_indexes = np.argmax(prediction, axis=1) # [3]
        predictions.extend(predicted_indexes.tolist())
        os.remove(output_filepath.absolute())
    os.remove(absolute_filepath)
    os.rmdir(output_dir)
    os.rmdir(TEMP_OUTPUT_DIR)

    def most_frequent(input_list):
        return max(set(input_list), key = input_list.count)
    predicted_index = most_frequent(predictions)
    predicted_genre = genres[predicted_index]
    print(f"Expected mapping: {INPUT_LABEL}, Predicted mapping: {predicted_genre}")



def download_file(youtube_id, output_dir):
    ydl = YoutubeDL({
        "outtmpl": f"{output_dir}/%(id)s.%(ext)s",
        "ignoreerrors": True,
        "format": "bestaudio/best",
    })
    ydl.download([f"https://www.youtube.com/watch?v={youtube_id}"])
    file_list = [name for name in os.listdir(TEMP_OUTPUT_DIR) if youtube_id in name]
    if len(file_list):
        return file_list[0]


if __name__ == "__main__":
    do_prediction()
