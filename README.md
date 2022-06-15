# Genre Classification
IPASS assignment by Floris Kappen

This repo contains all the parts necessary for the training pipeline aswell as executing the pipeline.


## Setup

1. Start by running `pip install -r requirements.txt`
2. Make sure FFMPEG is installed. This is necessary for the data_gathering scripts. It needs to be in your path.


## Running steps
This repo contains a bunch of directories, each containing their own script(s). Each directory has its' own README with more information

The order in which the scripts in the directories should be executed is the following:
1. `data_gathering/`: Downloads the data
3. `data_preparation/`: Filters and cuts the full songs into 30s pieces
2. `data_augmentation/`: Expands the training set by augmenting the data using various techniques
4. `data_preprocessing/`: Generates MFCCs for each set and saves them as JSON

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
