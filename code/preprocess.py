"""
preprocess.py

This script is used to download and preprocess our datasets.

Process:
    1. Convert raw dataset into pandas dataframe
    2. Convert youtube clips into mp3 files
    3. Convert mp3 files into NumPy array (.npy) spectrograms

    Currently, I'm only preprocessing AVspeech. I have not gotten around to AudioSet yet.
"""

#  STEP 1
#  Convert raw dataset into pandas dataframe

import pandas as pd
from pathlib import Path

# Establish main dataset directory
parent = Path(r"C:\Users\james\OneDrive - University of Rhode Island\Desktop\Audio Denoising\datasets")
raw_av_path = parent / 'AVspeech' / 'raw'

# Load the raw AVspeech train/test datasets into pandas dataframes
av_train_csv = raw_av_path / 'train' / 'avspeech_train.csv'
av_train_raw = pd.read_csv(av_train_csv)

av_test_csv = raw_av_path / 'test' / 'avspeech_test.csv'
av_test_raw = pd.read_csv(av_test_csv)



# STEP 2
# Convert youtube clips into mp3 files

"""

THIS IS WHERE WE LEFT OFF.

WE NEED TO:
    1. CHECK THAT THIS FUNCTION WORKS
    2. CONFIGURE THE "Audio Denosiing" FILE TO GitHub AND PUSH ITS CONTENTS TO PRESERVE FILE HIERARCHIES

"""



import os, sys
import yt_dlp

def download_clips(df, output_dir, max_files):
    """
    Converts YouTube dataset clips into mp3 audio files.
    
    Args:
        df (pd.DataFrame): The DataFrame containing our YouTube clips
        output_dir (Path): Directory to save the MP3 files
        max_files (int): Maximum number of clips to download
    """

    # Check if the output directory exists
    if not os.path.exists(output_dir):
        print('Error in download_clips function: output_dir does not exist')
        sys.exit()  # Terminate the program to prevent damage
        
    filesDownloaded = 0  # Tracks the number of files downloaded
    
    # Iterate through the DataFrame
    for _, row in df.iterrows():
        if filesDownloaded >= max_files:
            break
        
        # Extract necessary data
        video_id = row['id']
        start_time = row['start']
        end_time = row['stop']
        
        # Construct the YouTube URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Define output file path
        output_path = output_dir / f"{video_id}_{start_time}_{end_time}.mp3"
        
        # Skip if the file already exists
        if output_path.exists():
            print(f"File already exists: {output_path}")
            continue
        
        # Use yt-dlp to download the clip
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': str(output_path.with_suffix('.%(ext)s')),
                'download_sections': [{
                    'section': {
                        'start_time': start_time,
                        'end_time': end_time
                    }
                }]
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            print(f"Downloaded: {output_path}")
            filesDownloaded += 1
        
        except Exception as e:
            print(f"Failed to download {video_url} ({start_time}-{end_time}): {e}")
    
    print(f"Download complete: {filesDownloaded}/{max_files} files saved.")

# Example Usage
parent = Path(r"C:/Users/james/OneDrive - University of Rhode Island/Desktop/Audio Denoising")
raw_av_path = parent / 'datasets' / 'AVspeech' / 'raw' / 'train'
output_path = parent / 'processed_audio'

av_train_raw = pd.read_csv(raw_av_path / 'avspeech_train.csv')
download_clips(av_train_raw, output_path, max_files=10)