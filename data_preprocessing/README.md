# Data Preprocessing

This directory contains various scripts to preprocess the gathered data

## Preconditions
Data needs to be ready, see the `data_gathering/` directory.


## Explanation
**extract_mfcc**    
Helper function to do everything necessary to extract the MFCCs apart from actually extracting it itself.   
The function needs an argument 'extraction_function' which is called to actually get the MFCCs.

**utils**   
Contains the actual functions necessary to extract the MFCCs from an audio file. Contains __detailed documentation__

## MFCC Extraction
What is MFCC?

MFCCs are features that can be extracted from audio, often used in the speech processing or genre recognition fields. It stands for Mel Frequency Cepstral Co-efficients

1. Take the (short-time) Fourier transform of (a windowed excerpt of) a signal.

A Fourier transform (FT) is a mathematical transform that decomposes functions depending on space or time into functions depending on spatial frequency or temporal frequency. For this part of the MFCC extraction I use librosa.

2. Map the powers of the spectrum obtained above onto the mel scale

Studies have shown that humans do not perceive frequencies on a linear scale. We are better at detecting differences in lower frequencies than higher frequencies. For example, we can easily tell the difference between 500 and 1000 Hz, but we will hardly be able to tell a difference between 10,000 and 10,500 Hz, even though the distance between the two pairs are the same.

In 1937, Stevens, Volkmann, and Newmann proposed a unit of pitch such that equal distances in pitch sounded equally distant to the listener. This is called the mel scale. We perform a mathematical operation on frequencies to convert them to the mel scale.


