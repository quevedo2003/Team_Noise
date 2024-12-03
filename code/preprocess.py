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
parent = Path(r"C:\Users\james\Desktop\Audio Denoising\datasets")
raw_av_path = parent / 'AVspeech' / 'raw'

# Load the raw AVspeech train/test datasets into pandas dataframes
av_train_csv = raw_av_path / 'train' / 'avspeech_train.csv'
av_train_raw = pd.read_csv(av_train_csv)

av_test_csv = raw_av_path / 'test' / 'avspeech_test.csv'
av_test_raw = pd.read_csv(av_test_csv)

# print(av_train_raw.head(), '\n', av_test_raw.head())


# STEP 2
# Convert youtube clips into mp3 files



import os, sys, subprocess
import yt_dlp
  
#   Converts YouTube dataset clips into mp3 audio files.
#   
#   Args:
#       df (pd.DataFrame): The DataFrame containing our YouTube clips
#       output_dir (Path): Directory to save the MP3 files
#       max_files (int): Maximum number of clips to download

def download_clips(df, output_dir, max_files):

    # Check if the output directory exists
    if not os.path.exists(output_dir):
        print('Error in download_clips function: output_dir does not exist')
        sys.exit()  # Terminate the program to prevent damage
        
    filesDownloaded = 0  # Tracks the number of files downloaded
    failedAttempts = 0

    # Iterate through the DataFrame
    for _, row in df.iterrows():
        if filesDownloaded >= max_files:  # Ensure the loop stops once the max_files limit is reached
            break

        # Extract necessary data
        video_id = row['id']
        start_time = row['start']
        end_time = row['stop']
        
        # Construct the YouTube URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Define output file path
        output_path = output_dir / f"{video_id}.mp3"
        
        # Define parameters for mp3 downloads
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'outtmpl': str(output_path.with_suffix('.%(ext)s')),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'download_sections': {
                'audio': [f"{start_time}-{end_time}"]  # Trim start to stop timestamp
            },
            }

        # Check if the YouTube video is valid

            # BUG: the code is always claiming 'extraction successful! even if the link is invalid

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url=video_url, download=False)
                # might need to store logic to run downloader
                print('Extraction successful!')
        except:
            print('Extraction failed.')
            failedAttempts += 1

        # Download audio clip

            # BUG: the code is always failing download, even if link is valid.
        
        try:
            subprocess.run([
                'ffmpeg', '-ss', str(start_time), '-to', str(end_time),
                '-i', video_url, '-q:a', '0', '-map', 'a',
                '-y', output_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print('Download succesful!')
            filesDownloaded += 1
        except subprocess.CalledProcessError:
            print('Download failed.')
            failedAttempts += 1
        
        print (f'{filesDownloaded}/{max_files} downloaded. {failedAttempts} failed.')

    print(f"\nDownload complete: {filesDownloaded}/{max_files} files saved. {failedAttempts} invalid files skipped.\n")


# Example Usage
av_train_mp3_path = parent / 'AVspeech' / 'cleaned' / 'train' / 'mp3'
download_clips(av_train_raw, av_train_mp3_path, 3)
