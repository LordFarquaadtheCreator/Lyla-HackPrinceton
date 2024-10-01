from fastapi import FastAPI, Request
from modal import asgi_app, Mount
import modal
import text_processer
import TTS
import STT

app = FastAPI()

@app.post("/transcribe")
async def api_transcribe(request: Request):
    audio_bytes = await request.body()
    transcription = await STT.transcribe_audio.remote(audio_bytes)
    return {"transcription": transcription}

@app.post("/process")
async def api_process(request: Request):
    body = await request.json()
    text = body["text"]
    response = await text_processer.process_text.remote(text)
    return {"response": response}

@app.post("/speak")
async def api_speak(request: Request):
    body = await request.json()
    text = body["text"]
    audio_url = await TTS.text_to_speech.remote(text)
    return {"audio_url": audio_url}

modal_app = asgi_app(app)
