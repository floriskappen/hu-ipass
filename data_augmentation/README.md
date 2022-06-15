# Data augmentation

Data augmentation is a technique used to increase the number of samples a machine learning model sees during training.

This directory includes a script to augment the data we have collected so far. But remember, data augmentation is less effective than collecting new data!

## Preconditions
- Run the script in `data_gathering/` to download the uncut data
- Run the script in `data_preparation/` to prepare the data for augmentation

## Relevant augmentation techniques
Waveform augmentation:
- Time stretching
- Pitch scaling
- Noise addition
- Impulse response addition (adding reverb) : meh
- Low/high/pass-band filters : meh
- Random gain (to make our model amplitude-agnostic)

Spectogram augmentation:
- Time masking
- Frequency masking
- Time stretching
- Pitch scaling

## Credits

Most of my information regarding data augmentation for audio comes from Valerio Velardo and his [series on Audio Data Augmentation](https://www.youtube.com/playlist?list=PL-wATfeyAMNoR4aqS-Fv0GRmS6bx5RtTW)
