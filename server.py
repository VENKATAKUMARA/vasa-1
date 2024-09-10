import asyncio
import websockets
import whisper
from gtts import gTTS
import os

# Initialize Whisper model
model = whisper.load_model("base")

async def process_audio(websocket, path):
    audio_path = 'received_audio.mp3'
    
    # Receive the audio file from the client
    with open(audio_path, 'wb') as f:
        while True:
            chunk = await websocket.recv()
            if chunk == b'END_OF_FILE':
                break
            f.write(chunk)
    
    # Process the audio file and print the transcribed text
    await translate_audio(audio_path, websocket)

async def translate_audio(audio_path, websocket):
    # Convert audio to text using Whisper
    result = model.transcribe(audio_path)
    text = result['text']
    
    # Print the transcribed text before translation
    print(f"Transcribed Text: {text}")
    
    # Translate text to Hindi using gTTS
    translated_audio_path = 'translated_audio.mp3'
    tts = gTTS(text=text, lang='hi')  # 'hi' for Hindi
    tts.save(translated_audio_path)
    
    # Send the translated audio back to the client
    await send_translated_audio(translated_audio_path, websocket)

async def send_translated_audio(translated_audio_path, websocket):
    with open(translated_audio_path, 'rb') as f:
        while True:
            chunk = f.read(1024*1024)  # 1 MB chunks
            if not chunk:
                break
            await websocket.send(chunk)
        await websocket.send(b'END_OF_FILE')

async def main():
    async with websockets.serve(process_audio, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run server indefinitely

if __name__ == "__main__":
    asyncio.run(main())
