import asyncio
import modal
from deepgram import DeepgramClient
import os

stub = modal.Stub()

@stub.function(secrets=[modal.Secret.from_name("DEEPGRAM_API_KEY")])
async def transcribe_audio(audio_path: str):
    DEEPGRAM_API_KEY = os.environ["DEEPGRAM_API_KEY"]
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    transcript_collector = TranscriptCollector()

    # Function to process transcription results
    def process_result(result):
        for word in result['results']['channels'][0]['alternatives'][0]['words']:
            transcript_collector.add_part(word['word'])

    try:
        # Open the audio file in read-binary mode
        with open(audio_path, 'rb') as audio:
            source = {"buffer": audio, "mimetype": "audio/wav"}
            response = await deepgram.transcription.pre_recorded(source, {'punctuate': True})
            process_result(response)
        
        full_transcript = transcript_collector.get_full_transcript()
        print(f"Full transcript: {full_transcript}")
        return full_transcript
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)
