
import os
import json
from pathlib import Path
import wave
import math

import numpy as np
import librosa
import scipy

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
                    if "aug.wav" in video_cut:
                        continue
                    audio_cut_path = Path(video_cuts_dir + video_cut).absolute()
                    try:
                        with wave.open(str(audio_cut_path), "rb") as wave_file:
                            frame_rate = wave_file.getframerate()
                        signal, sr = librosa.load(audio_cut_path, sr=frame_rate)
                        for segment in range(NUM_SEGMENTS):
                            num_samples_per_segment = int(frame_rate / NUM_SEGMENTS)
                            start_sample = num_samples_per_segment * segment # s=0 -> 0
                            finish_sample = start_sample + num_samples_per_segment # s=0 -> num_samples_per_segment
                            expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / HOP_LENGTH)
                            mfcc = get_mfcc(
                                signal=signal[start_sample:finish_sample],
                                sample_rate=sr,
                                n_mfcc=N_MFCC,
                                n_fft=N_FFT,
                                hop_length=HOP_LENGTH
                            )
                            mfcc = mfcc.T
                            if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                                datas[set_type]["mfcc"].append(mfcc.tolist())
                                datas[set_type]["labels"].append(index)
                    except wave.Error as e:
                        print(e)
                        continue

    for data_type in datas:
        with open(f"{DATA_DIR}extracted_mfccs_cus_{data_type}.json", "w") as f:
            f.write(json.dumps(datas[data_type]))


def get_mfcc(signal, sample_rate, n_mfcc, n_fft, hop_length):
    """
        signal: np.ndarray
            audio time series
        sample_rate: int
            sampling rate of `signal`
        n_mfcc: int
            number of MFCCs to return
        n_fft: int
            number of FFT components
        hop_length: int
            number of samples between successive frames
    """
    spectrogram = power_to_db(
        get_mel_spectrogram(
            signal=signal,
            sample_rate=sample_rate,
            n_fft=n_fft,
            hop_length=hop_length
        )
    )
    mfcc = scipy.fftpack.dct(
        spectrogram,
        axis=-2,
        type=2,
        norm="ortho"
    )[..., :n_mfcc, :]

    return mfcc

def power_to_db(spectrogram, reference_value=1.0, amin=1e-10, top_db=80.0):
    """Convert a power spectrogram (amplitude squared) to decibel (dB) units
    
    This computes the scaling ``10 * log10(spectrogram / reference_value)`` in a numerically
    stable way.
    
        spectrogram: np.ndarray
            input power
        reference_value: int
            the amplitude `abs(spectrogram)` is scaled relative to `reference_value`
        amin: float
            minimum threshold for `abs(spectrogram)` and ``reference_value``
        top_db: float
            threshold the output at `top_db` below the peak:
            `max(10 * log10(S)) - top_db`
    """

    magnitude = spectrogram

    log_spec = 10.0 * np.log10(np.maximum(amin, magnitude))
    log_spec -= 10.0 * np.log10(np.maximum(amin, reference_value))

    log_spec = np.maximum(log_spec, log_spec.max() - top_db)

    return log_spec


def get_mel_spectrogram(signal, sample_rate, n_fft, hop_length):
    """
        sample_rate: int
            sampling rate of the incoming signal
        n_fft: int
            number of FFT components
    """
    spectrogramm, n_fft = get_magnitude_spectrogram(
        signal,
        n_fft,
        hop_length
    )

    mel_basis = build_mel_filter(sample_rate=sample_rate, n_fft=n_fft)

    return np.einsum("...ft,mf->...mt", spectrogramm, mel_basis, optimize=True)


def get_magnitude_spectrogram(signal, n_fft, hop_length):
    """Helper function to retrieve a magnitude spectrogram.
    
        signal: np.ndarray
            audio time series
        n_fft: int
            number of FFT components
        hop_length: int
            number of samples between successive frames
    """
    spectrogram = np.abs(
        librosa.core.stft(
            y=signal,
            n_fft=n_fft,
            hop_length=hop_length,
            center=True,
            window="hann",
        ) ** 2
    )

    return spectrogram, n_fft


def build_mel_filter(sample_rate, n_fft):
    """
        n_fft: int
            number of FFT components
        sample_rate: int
            sampling rate of the incoming signal
    """
    n_mels = 128
    fmin = 0.0
    fmax = float(sample_rate) / 2
    htk = None

    # Initialize the weights
    weights = np.zeros((n_mels, int(1 + n_fft // 2)), dtype=np.float32)

    # Center freqs of each FFT bin
    fftfreqs = np.fft.rfftfreq(n=n_fft, d=1.0 / sample_rate)

    # 'Center freqs' of mel bands - uniformly spaced between limits
    mel_f = get_mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax, htk=htk)

    fdiff = np.diff(mel_f)
    ramps = np.subtract.outer(mel_f, fftfreqs)

    for i in range(n_mels):
        # lower and upper slopes for all bins
        lower = -ramps[i] / fdiff[i]
        upper = ramps[i + 2] / fdiff[i + 1]

        # .. then intersect them with each other and zero
        weights[i] = np.maximum(0, np.minimum(lower, upper))
    
    enorm = 2.0 / (mel_f[2 : n_mels + 2] - mel_f[:n_mels])
    weights *= enorm[:, np.newaxis]

    return weights


def get_mel_frequencies(n_mels, fmin, fmax, htk):
    min_mel = librosa.convert.hz_to_mel(fmin, htk=htk)
    max_mel = librosa.convert.hz_to_mel(fmax, htk=htk)

    mels = np.linspace(min_mel, max_mel, n_mels)

    return librosa.convert.mel_to_hz(mels, htk=htk)


if __name__ == "__main__":
    extract_mfcc()
