
import os
import soundfile

import audiomentations
import librosa

# Specify the directory in which the data lives
DATA_DIR = "../data/"

# Compose the augmentation class
augment = audiomentations.Compose([
    audiomentations.PitchShift(min_semitones=-3, max_semitones=3, p=1),
    audiomentations.Gain(min_gain_in_db=8, max_gain_in_db=8, p=1)
])


if __name__ == "__main__":
    # Get all genres in the data directory
    genres = [name for name in os.listdir(DATA_DIR)]

    for genre in genres:
        base_data_dir = f"../data/{genre}"
        train_dir = base_data_dir + "/cut/train"

        if os.path.exists(train_dir):
            for r, dirs, f in os.walk(train_dir):
                for directory in dirs:
                    for root, d, files in os.walk(os.path.join(train_dir, directory)):
                        # Loop through all the files in the training directory
                        for file in files:
                            # Skip augmented files as they have a lower sample rate. This issue should be solved in a later version
                            if "aug.wav" in file:
                                continue

                            filename_without_extension = ".".join(file.split(".")[:-1])
                            filepath = os.path.join(root, file)
                            absolute_filepath = os.path.abspath(filepath)
                            signal, sample_rate = librosa.load(absolute_filepath)

                            # Augment the signal
                            augmented_signal = augment(signal, sample_rate)
                            # Save the file
                            soundfile.write(
                                os.path.join(root, f"{filename_without_extension}_aug.wav"),
                                augmented_signal,
                                sample_rate
                            )
                        print(f"AUGMENT: {len(files)} files for {genre}/{directory}")
