
import os
import json
from pathlib import Path
import math
import wave

import librosa
import python_speech_features

DATA_DIR = "../data/"
NUM_SEGMENTS = 5

N_FFT = 2048
N_MFCC = 13
HOP_LENGTH = 512

def extract_mfcc():
    genres = [name for name in os.listdir(DATA_DIR) if "." not in name]

    data_template = {
        "mapping": genres,
        "mfcc": [],
        "labels": []
    }
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
            # Dictionary to store data
            data = {
                "mapping": genres,
                "mfcc": [],
                "labels": []
            }

            for video_id in os.listdir(set_dir):
                video_cuts_dir = set_dir + f"{video_id}/"
                for video_cut in os.listdir(video_cuts_dir):
                    audio_cut_path = Path(video_cuts_dir + video_cut).absolute()
                    try:
                        with wave.open(str(audio_cut_path), "rb") as wave_file:
                            frame_rate = wave_file.getframerate()
                        signal, sample_rate = librosa.load(audio_cut_path, sr=frame_rate)
                        for segment in range(NUM_SEGMENTS):
                            num_samples_per_segment = int(sample_rate / NUM_SEGMENTS)
                            start_sample = num_samples_per_segment * segment # s=0 -> 0
                            finish_sample = start_sample + num_samples_per_segment # s=0 -> num_samples_per_segment
                            expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / HOP_LENGTH)
                            mfcc = python_speech_features.mfcc(
                                signal=signal[start_sample:finish_sample],
                                samplerate=sample_rate,
                                nfft=N_FFT,
                                numcep=N_MFCC,
                                winstep=HOP_LENGTH / sample_rate
                            )
                            datas[set_type]["mfcc"].append(mfcc.tolist())
                            datas[set_type]["labels"].append(index)
                    except wave.Error as e:
                        print(e)
                        continue

    for data_type in datas:
        with open(f"{DATA_DIR}extracted_mfccs_sf_{data_type}.json", "w") as f:
            f.write(json.dumps(datas[data_type]))

if __name__ == "__main__":
    extract_mfcc()
