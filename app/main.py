import os
import requests
from pydub import AudioSegment
import speech_recognition as sr
from helpers.twitter import post_tweet

recognizer = sr.Recognizer()
last_radio_url = ""

try:
    # Fetch the latest team radio data
    res = requests.get("https://api.openf1.org/v1/team_radio?session_key=latest")
    res.raise_for_status()
    data = res.json()

    # Get the last radio transmission
    last_radio = data[-1] if data else None

    if last_radio and last_radio_url != last_radio.get("recording_url"):
        driver_number = last_radio.get("driver_number")

        try:
            # Fetch driver information using driver_number
            res2 = requests.get(f"https://api.openf1.org/v1/drivers?driver_number={driver_number}&session_key=latest")
            res2.raise_for_status()
            driver = res2.json()

            if "recording_url" in last_radio:
                last_radio_url = last_radio["recording_url"]

                try:
                    # Download the MP3 file
                    mp3_response = requests.get(last_radio_url)
                    mp3_response.raise_for_status()

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
                    text = f'{driver[0]["last_name"]} ({driver[0]["team_name"]}) team radio: {audio_transcript}.'
                    
                    post_tweet(text)

                except requests.RequestException as e:
                    print(f"Error downloading or processing the MP3 file: {e}")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand the audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                finally:
                    # Remove the files if they exist
                    if os.path.exists(mp3_filename):
                        os.remove(mp3_filename)
                    if os.path.exists(wav_filename):
                        os.remove(wav_filename)
                    
                    last_radio_url = last_radio.get("recording_url")

            else:
                print("No recordings found.")

        except requests.RequestException as e:
            print(f"Error fetching driver information: {e}")

    else:
        print("No new data found or no data available.")

except requests.RequestException as e:
    print(f"Error fetching team radio data: {e}")
