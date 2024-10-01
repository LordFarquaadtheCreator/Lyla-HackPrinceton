# pylint: disable=C0103
import asyncio
import shutil
import subprocess
import time
import requests
import os
from fastapi import FastAPI, WebSocket
from backend.agents.Paradigm_Agent.paradigm import agent_executor
from backend.agents.RAG.vectorize import vector_search
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
# from langchain.llms import OpenAI
from dotenv import load_dotenv
import uvicorn
 

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

file = ''

class LanguageModelProcessor:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", groq_api_key=os.getenv("GROQ_API_KEY"))
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125", openai_api_key=os.getenv("OPENAI_API_KEY"))
        
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load the system prompt from a file
        with open('system_prompt.txt', 'r') as file:
            system_prompt = file.read().strip()
        
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def process(self, text):
        self.memory.chat_memory.add_user_message(text)

        start_time = time.time()

        # Go get the response from the LLM
        response = self.conversation.invoke({"text": text})
        end_time = time.time()

        self.memory.chat_memory.add_ai_message(response['text'])  

        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']

class TextToSpeech:
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    MODEL_NAME = "aura-helios-en"  # Example model name, change as needed

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        return lib is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}&performance=some&encoding=linear16&sample_rate=24000&language=en,fr,hi,ja,ko"
        headers = {
            "Authorization": f"Token {self.DEEPGRAM_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

        player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
        player_process = subprocess.Popen(
            player_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        start_time = time.time()
        first_byte_time = None  
        try:
            with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        if first_byte_time is None:
                            first_byte_time = time.time()  
                            ttfb = int((first_byte_time - start_time) * 1000)
                            print(f"TTS Time to First Byte (TTFB): {ttfb}ms\n")
                    if player_process.stdin is not None:     
                        player_process.stdin.write(chunk)
                        player_process.stdin.flush()
                    else:
                        print("Error: player_process.stdin is None")
                        break

            if player_process.stdin is not None:
                player_process.stdin.close()
            player_process.wait()

        except Exception as e:
            print(f"An error occurred: {e}")

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)


from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.websocket("/ws/stt")
async def get_transcript(websocket: WebSocket):
    # Activate WebSocket
    await websocket.accept()

    # Initialize Deepgram
    config = DeepgramClientOptions(options={"keepalive": "true"})
    deepgram = DeepgramClient("YOUR_DEEPGRAM_API_KEY", config)
    dg_connection = deepgram.listen.asynclive.v("1")
    print("Listening...")

    transcript_collector = TranscriptCollector()
    transcription_complete = asyncio.Event()

    def handle_full_sentence(full_sentence):
        transcription_response = full_sentence
        print(f"Transcribed: {transcription_response}")

    async def on_message(result, **kwargs):
        sentence = result.channel.alternatives[0].transcript

        if not result.speech_final:
            transcript_collector.add_part(sentence)
        else:
            transcript_collector.add_part(sentence)
            full_sentence = transcript_collector.get_full_transcript().strip()

            if full_sentence:
                print(f"Human: {full_sentence}")
                handle_full_sentence(full_sentence)
                transcript_collector.reset()
                transcription_complete.set()  # Signal to stop transcription

    # Set the event handler for transcription
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    # Configure transcription options
    options = LiveOptions(
        model="nova-2",
        punctuate=True,
        language="ja",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        endpointing=300,
        smart_format=True,
    )

    await dg_connection.start(options)

    try:
        while True:
            # Take in streaming data from WebSocket instead of microphone
            data = await websocket.receive_bytes()

            # Directly send the received audio data to Deepgram
            await dg_connection.send(data)

            # Check if transcription is complete, if so break from the loop
            if transcription_complete.is_set():
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cleanup and close the connection
        await dg_connection.finish()
        
    return self.transcript_parts

import aiohttp
import asyncio

@app.websocket("/ws/tts")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Create a session to manage the connection to Deepgram's WebSocket API
    async with aiohttp.ClientSession() as session:

        # Open a WebSocket connection to Deepgram's API
        async with session.ws_connect(f"wss://api.deepgram.com/v1/listen?token={os.getenv('DEEPGRAM_API_KEY')}") as ws:

            # Loop to receive audio data from the client and send it to Deepgram
            while True:
                data = await websocket.receive_bytes()
                if not data:
                    break
                await ws.send_bytes(data)

                # Receive the transcription response from Deepgram
                deepgram_response = await ws.receive()
                if deepgram_response.type == aiohttp.WSMsgType.TEXT:
                    transcription = deepgram_response.data
                    llm_response = self.llm.process(transcription)
                    tts = TextToSpeech()
                    tts.speak(llm_response)

            # Close the WebSocket connection when done
            await ws.close()

@app.post("/upload_file")
def get_file(input_file: str) -> str:
    file += input_file
    
@app.post("/upload_text")
async def upload_text(text: str):
    from openai import OpenAI
    from fastapi.responses import StreamingResponse
    
    try:
        client = OpenAI()

        query = str(await agent_executor(text) + text)
        results = vector_search.similarity_search(query)

        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=str(results + file),
        )
    except:
        print("ruh roh raggy")

    def generate_audio_stream(response):
        for chunk in response.iter_content(chunk_size=4096):
            yield chunk

    # Note: The actual way to access the stream depends on the OpenAI API's response structure
    return StreamingResponse(generate_audio_stream(response), media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
