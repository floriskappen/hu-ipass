
from email.mime import audio
import os
import soundfile

import audiomentations
import librosa


DATA_DIR = "../data/"

augment = audiomentations.Compose([
    audiomentations.PitchShift(min_semitones=-3, max_semitones=3, p=1),
    audiomentations.Gain(min_gain_in_db=8, max_gain_in_db=8, p=1)
])


if __name__ == "__main__":
    genres = [name for name in os.listdir(DATA_DIR)]
    for genre in genres:
        base_data_dir = f"../data/{genre}"
        train_dir = base_data_dir + "/cut/train"

        if os.path.exists(train_dir):
            for r, dirs, f in os.walk(train_dir):
                for directory in dirs:
                    for root, d, files in os.walk(os.path.join(train_dir, directory)):
                        for file in files:
                            filename_without_extension = ".".join(file.split(".")[:-1])
                            filepath = os.path.join(root, file)
                            absolute_filepath = os.path.abspath(filepath)
                            signal, sample_rate = librosa.load(absolute_filepath)
                            augmented_signal = augment(signal, sample_rate)
                            soundfile.write(
                                os.path.join(root, f"{filename_without_extension}_aug.wav"),
                                augmented_signal,
                                sample_rate
                            )
                        print(f"AUGMENT: {len(files)} files for {genre}/{directory}")
