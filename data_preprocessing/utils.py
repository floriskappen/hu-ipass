import scipy
import librosa
import numpy as np

def get_mfcc(signal, sample_rate, n_mfcc, n_fft, hop_length):
    """Get the MFFCs of an audio signal
    
    Algorithm steps derived from: https://en.wikipedia.org/wiki/Mel-frequency_cepstrum

    Implementation derived from python_speech_features, librosa

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

    # Take the fourier transform of the signal and map it onto the mel scale
    fft_spectrogram = get_mel_spectrogram(
        signal=signal,
        sample_rate=sample_rate,
        n_fft=n_fft,
        hop_length=hop_length
    )

    # Take the logs of the powers at each of the mel frequencies
    mel_spectrogram = power_to_db(fft_spectrogram)

    # Take the discrete cosine transform (dct) of the list
    mfcc = scipy.fftpack.dct(
        mel_spectrogram,
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
    # Get the magnitude spectrogram
    spectrogramm, n_fft = get_magnitude_spectrogram(
        signal,
        n_fft,
        hop_length
    )

    # Get the basis of the mel filter
    mel_basis = build_mel_filter(sample_rate=sample_rate, n_fft=n_fft)

    # Multiply the spectrogram and the mel_basis filter to filter the spectrogram
    return np.einsum("...ft,mf->...mt", spectrogramm, mel_basis, optimize=True)


def get_magnitude_spectrogram(signal, n_fft, hop_length):
    """Helper function to retrieve a magnitude spectrogram using librosa's short-time Fourier transform (STFT) function.
    
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

    # Initialize the weights
    weights = np.zeros((n_mels, int(1 + n_fft // 2)), dtype=np.float32)

    # Center freqs of each FFT bin
    fftfreqs = np.fft.rfftfreq(n=n_fft, d=1.0 / sample_rate)

    # 'Center freqs' of mel bands - uniformly spaced between limits
    mel_f = get_mel_frequencies(n_mels + 2, fmin=fmin, fmax=fmax)

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


def get_mel_frequencies(n_mels, fmin, fmax) -> np.ndarray:
    """Compute an array of acoustic frequencies tuned to the mel scale.
    
        n_mels: int
            Number of mel binds
        fmin: float
            Minimum frequency (Hz)
        fmax: float
            Maximum frequency (Hz)
    """

    # 'Center freqs' of mel bands - uniformly spaced between limits
    min_mel = librosa.convert.hz_to_mel(fmin, htk=None)
    max_mel = librosa.convert.hz_to_mel(fmax, htk=None)

    mels = np.linspace(min_mel, max_mel, n_mels)

    return librosa.convert.mel_to_hz(mels, htk=None)
