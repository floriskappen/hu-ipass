"""Helper function to do everything necessary to extract the MFCCs apart from actually extracting it itself.

The function needs an argument 'extraction_function' which is called to actually get the MFCCs."""

import os
import json
from pathlib import Path
import wave

import librosa

# Specify data dir
DATA_DIR = "../data/"

# Specify parameters to use
NUM_SEGMENTS = 5
N_FFT = 2048
N_MFCC = 13
HOP_LENGTH = 512

def extract_mfcc(extraction_function, mfcc_filename = "extracted_mfccs"):
    # Get all genres in the data dir
    genres = [name for name in os.listdir(DATA_DIR) if "." not in name]

    data_template = {
        "mapping": genres,
        "mfcc": [],
        "labels": []
    }

    # Prepare the data structure
    datas = {
        "train": data_template.copy(),
        "test": data_template.copy(),
        "validation": data_template.copy(),
    }


    for index, genre in enumerate(genres):
        set_dirs = {
            "train": DATA_DIR + genre + "/cut/train/",
            "test": DATA_DIR + genre + "/cut/test/",
            "validation": DATA_DIR + genre + "/cut/validation/",
        }
        for set_type, set_dir in set_dirs.items():
            for video_id in os.listdir(set_dir):
                video_cuts_dir = set_dir + f"{video_id}/"
                for video_cut in os.listdir(video_cuts_dir):
                    if "aug.wav" in video_cut:
                        continue
                    audio_cut_path = Path(video_cuts_dir + video_cut).absolute()

                    mfccs = extract_one_file_mfcc(extraction_function, audio_cut_path)

                    for mfcc in mfccs:
                        datas[set_type]["mfcc"].append(mfcc)
                        datas[set_type]["labels"].append(index)

    for data_type in datas:
        with open(f"{DATA_DIR}{mfcc_filename}_{data_type}.json", "w") as f:
            f.write(json.dumps(datas[data_type]))


def extract_one_file_mfcc(extraction_function, file_path):
    mfccs = []
    try:
        # Read the data
        with wave.open(str(file_path), "rb") as wave_file:
            frame_rate = wave_file.getframerate()
        signal, sr = librosa.load(file_path, sr=frame_rate)

        # Split it up into different segments
        for segment in range(NUM_SEGMENTS):
            num_samples_per_segment = int(frame_rate / NUM_SEGMENTS)
            start_sample = num_samples_per_segment * segment # s=0 -> 0
            finish_sample = start_sample + num_samples_per_segment # s=0 -> num_samples_per_segment

            # Call the extraction function passed as an argument with all the necessary parameters
            mfcc = extraction_function(
                signal=signal[start_sample:finish_sample],
                sample_rate=sr,
                n_mfcc=N_MFCC,
                n_fft=N_FFT,
                hop_length=HOP_LENGTH
            )
            mfccs.append(mfcc.tolist())
    except wave.Error as e:
        # Some files are corrupted so we catch them here. No need to do anything else.
        print(e)
    return mfccs
