
import librosa

from extract_mfcc import extract_mfcc

def extraction_function_librosa(signal, sample_rate, n_mfcc, n_fft, hop_length):
    # Use librosa's MFCC function
    mfcc =  librosa.feature.mfcc(
        y=signal,
        sr=sample_rate,
        n_fft=n_fft,
        n_mfcc=n_mfcc,
        hop_length=hop_length
    )

    return mfcc.T

if __name__ == "__main__":
    extract_mfcc(
        extraction_function=extraction_function_librosa,
        mfcc_filename="extracted_mfccs_lib"
    )
