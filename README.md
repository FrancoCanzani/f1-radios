# Team Radio to Twitter Bot

This project fetches the latest Formula 1 team radio recordings, converts the audio to text using Google's Speech Recognition API, and posts the transcribed message to Twitter.

## Features

- Fetches the latest team radio data from the OpenF1 API.
- Downloads the latest team radio recording.
- Converts the audio from MP3 to WAV format.
- Uses Google's Speech Recognition API to transcribe the audio.
- Posts the transcribed message to Twitter with driver and team information.

## Requirements

- Python 3.6+
- [pydub](https://github.com/jiaaro/pydub)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [requests](https://pypi.org/project/requests/)
- [tweepy](https://www.tweepy.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/team-radio-to-twitter.git
   cd team-radio-to-twitter
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root of the project and add your Twitter API credentials:
   ```plaintext
   CONSUMER_KEY=your_consumer_key
   CONSUMER_SECRET=your_consumer_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py`: Contains the main logic for fetching, processing, and posting the team radio data.
- `helpers/twitter.py`: Contains the helper function `post_tweet` for posting tweets using Tweepy.
- `audio_files/`: Directory where audio files are temporarily stored.
