from modal import stub
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Deepgram API configuration
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MODEL_NAME = "alpha-stella-en-v2"
DEEPGRAM_URL = f"https://api.beta.deepgram.com/v1/speak?model={MODEL_NAME}&performance=some&encoding=linear16&sample_rate=24000"

def send_tts_request(text):
    """
    Sends a request to the Deepgram TTS API and returns the audio bytes.
    """
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice": MODEL_NAME
    }
    
    with requests.post(DEEPGRAM_URL, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()
        audio_bytes = response.content
        return audio_bytes

@stub.function()
def text_to_speech(text):
    """
    Serverless function that converts text to speech using Deepgram's TTS service
    and returns the audio bytes.
    """
    audio_bytes = send_tts_request(text)
    return audio_bytes

# Example usage, uncomment to test locally
# if __name__ == "__main__":
#     audio_bytes = text_to_speech("Hello, world!")
#     with open("output_audio.wav", "wb") as audio_file:
#         audio_file.write(audio_bytes)
#     print("Audio file has been saved.")
