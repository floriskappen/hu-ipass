
from extract_mfcc import extract_mfcc
import utils

def extraction_function_custom(signal, sample_rate, n_mfcc, n_fft, hop_length):
    mfcc = utils.get_mfcc(
        signal=signal,
        sample_rate=sample_rate,
        n_fft=n_fft,
        n_mfcc=n_mfcc,
        hop_length=hop_length
    )
    return mfcc.T

if __name__ == "__main__":
    extract_mfcc(
        extraction_function=extraction_function_custom,
        mfcc_filename="extracted_mfccs_custom"
    )
