import os
import requests
from pydub import AudioSegment
import speech_recognition as sr
from helpers.twitter import post_tweet

recognizer = sr.Recognizer()

# Fetch the latest team radio data
res = requests.get("https://api.openf1.org/v1/team_radio?session_key=latest")
data = res.json()

# Get the last radio transmission
last_radio = data[-1] if data else None

# Check if there is a valid last radio transmission
if last_radio:
    driver_number = last_radio.get("driver_number")

    # Fetch driver information using driver_number
    res2 = requests.get(f"https://api.openf1.org/v1/drivers?driver_number={driver_number}&session_key=latest")
    driver = res2.json()


    # Check if there are any recordings
    if "recording_url" in last_radio:
        last_radio_url = last_radio["recording_url"]

        # Download the MP3 file
        mp3_response = requests.get(last_radio_url)

        # Set the path to the app/audio_files folder
        app_folder = os.path.join(os.path.dirname(__file__), 'audio_files')
        os.makedirs(app_folder, exist_ok=True)

        mp3_filename = os.path.join(app_folder, "last_recording.mp3")
        wav_filename = os.path.join(app_folder, "last_recording.wav")

        # Save the MP3 file
        with open(mp3_filename, "wb") as file:
            file.write(mp3_response.content)
        
        # Convert MP3 to WAV
        audio = AudioSegment.from_mp3(mp3_filename)
        audio.export(wav_filename, format="wav")

        # Recognize the audio
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            
        audio_transcript = recognizer.recognize_google(audio_data)
        text = f"{driver[0]["last_name"]} ({driver[0]["team_name"]}) team radio: {audio_transcript}."
        
        post_tweet(text)
        
        # Remove the files if they exist
        if os.path.exists(mp3_filename):
            os.remove(mp3_filename)
        if os.path.exists(wav_filename):
            os.remove(wav_filename)

    else:
        print("No recordings found.")

else:
    print("No data found.")
