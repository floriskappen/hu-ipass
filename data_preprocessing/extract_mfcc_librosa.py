
import os
import json
from pathlib import Path
import wave
import math

import librosa

DATA_DIR = "../data/"
NUM_SEGMENTS = 5

N_FFT = 2048
N_MFCC = 13
HOP_LENGTH = 512

def extract_mfcc():
    genres = [name for name in os.listdir(DATA_DIR)]
    
    # Dictionary to store data
    data = {
        "mapping": genres,
        "mfcc": [],
        "labels": []
    }

    for index, genre in enumerate(genres):
        genre_data_dir = DATA_DIR + genre + "/cut/"
        for video_id in os.listdir(genre_data_dir):
            video_cuts_dir = genre_data_dir + f"{video_id}/"
            for video_cut in os.listdir(video_cuts_dir):
                video_cut_path = Path(video_cuts_dir + video_cut).absolute()
                with wave.open(str(video_cut_path), "rb") as wave_file:
                    frame_rate = wave_file.getframerate()
                signal, sr = librosa.load(video_cut_path, sr=frame_rate)
                for segment in range(NUM_SEGMENTS):
                    num_samples_per_segment = int(frame_rate / NUM_SEGMENTS)
                    start_sample = num_samples_per_segment * segment # s=0 -> 0
                    finish_sample = start_sample + num_samples_per_segment # s=0 -> num_samples_per_segment
                    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / HOP_LENGTH)
                    mfcc = librosa.feature.mfcc(y=signal[start_sample:finish_sample],
                                                sr=sr,
                                                n_fft=2048,
                                                n_mfcc=13,
                                                hop_length=512)
                    mfcc = mfcc.T
                    if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                        data["mfcc"].append(mfcc.tolist())
                        data["labels"].append(index)

    with open("../extracted_mfccs.json", "w") as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    extract_mfcc()
