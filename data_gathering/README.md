# Data Gathering

This directory contains various scripts to gather the necessary data and transform it into 30s chunks

## Preconditions
No preconditions

## Explanation
**download_playlists.py**   
Downloads all audio files from the videos in the playlists specified in `config.py`.

**cut_files**
Loops through all downloaded audio files, converts them to 30s .wav files

## Execution order
1. download_playlists
2. cut_files
