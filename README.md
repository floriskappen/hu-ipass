# Genre Classification
IPASS assignment by Floris Kappen

This repo contains all the parts necessary for the training pipeline aswell as executing the pipeline.


## Setup

1. Start by running `pip install -r requirements.txt`
2. Make sure FFMPEG is installed. This is necessary for the data_gathering scripts. It needs to be in your system path.


## Running steps
This repo contains a bunch of directories, each containing their own script(s). Each directory has its' own README with more information

The order in which the scripts in the directories should be executed is the following:
1. `data_gathering/`: Downloads the data
2. `data_preparation/`: Filters and cuts the full songs into 30s pieces
3. `data_augmentation/`: Expands the training set by augmenting the data using various techniques
4. `data_preprocessing/`: Generates MFCCs for each set and saves them as JSON
5. `train_model`: Trains a LSTM model with the generated MFCCs
6. `do_prediction`: Does a prediction with an audio file of your choice


## The algorithm
If you are just here for the implementation of the algorithm, please check `data_preprocessing/utils.py` which contains all the code for that.

## Tests
The `tests/` folder contains (multiple) tests for the different components. These can be run by running `pytest` in the root directory (this one)


## data/ folder
The `data/` folder at the root of this repository will be filled with the collected data. The structure is as follows:
- `data/`
    - `${genre}/`
        - `uncut/`: Contains the audio files ripped straight from youtube
        - `cut/`
            - `train/`: Contains the training set
                - `${song_id}`: Contains 30s segments of the song aswell as augmented variants later on
            - `validation/`: Contains the validation set
                - `${song_id}`: Contains 30s segments of the song
            - `test/`: Contains the test set
                - `${song_id}`: Contains 30s segments of the song
