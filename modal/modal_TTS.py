import modal
import requests
import time
import io
import os

stub = modal.Stub()

image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg")
    .pip_install("requests")
)

@stub.function(image=image, secrets=[modal.Secret.from_name("DEEPGRAM_API_KEY")])
def send_tts_request(text: str):
    DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
    
    MODEL_NAME = "alpha-stella-en-v2"
    DEEPGRAM_URL = f"https://api.beta.deepgram.com/v1/speak?model={MODEL_NAME}&performance=some&encoding=linear16&sample_rate=24000"
    
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice": MODEL_NAME
    }
    
    start_time = time.time()
    first_byte_time = None
    
    audio_buffer = io.BytesIO()
    
    with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                if first_byte_time is None:
                    first_byte_time = time.time()
                    ttfb = int((first_byte_time - start_time) * 1000)
                    print(f"Time to First Byte (TTFB): {ttfb}ms")
                audio_buffer.write(chunk)
    
    audio_buffer.seek(0)
    return audio_buffer