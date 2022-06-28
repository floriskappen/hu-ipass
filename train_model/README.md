# Data Preprocessing

This directory contains a script to train the model

## Preconditions
Data needs to be ready and a model needs to be trained. See the `data_preprocessing/` directory.


## Explanation
`train_model` loads all the prepared datasets and trains an LSTM model. It also logs the progress and does a prediction at the end. The model gets saved in the data directory with a timestamp