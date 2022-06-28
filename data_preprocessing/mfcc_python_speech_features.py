
import python_speech_features

from extract_mfcc import extract_mfcc

def extraction_function_python_speech_features(signal, sample_rate, n_mfcc, n_fft, hop_length):
    # Use python speech features' function
    mfcc = python_speech_features.mfcc(
        signal=signal,
        samplerate=sample_rate,
        nfft=n_fft,
        numcep=n_mfcc,
        winstep=hop_length / sample_rate
    )
    return mfcc

if __name__ == "__main__":
    extract_mfcc(
        extraction_function=extraction_function_python_speech_features,
        mfcc_filename="extracted_mfccs_psf"
    )
