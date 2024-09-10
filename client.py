import asyncio
import websockets

async def send_audio(uri, audio_file, chunk_size=1024*1024):
    async with websockets.connect(uri) as websocket:
        # Read and send the audio file in chunks
        with open(audio_file, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                await websocket.send(chunk)
        
        # Indicate end of file transmission
        await websocket.send(b'END_OF_FILE')

        # Receive server confirmation
        response = await websocket.recv()
        print("Server response:", response)

        # Receive translated audio file
        await receive_translated_audio(websocket)

async def receive_translated_audio(websocket):
    # Path to save the received translated audio
    translated_audio_path = 'received_translated_audio.mp3'
    
    with open(translated_audio_path, 'wb') as f:
        while True:
            chunk = await websocket.recv()
            if chunk == b'END_OF_FILE':
                break
            f.write(chunk)
    
    print(f"Translated audio received and saved at: {translated_audio_path}")

# Example usage
audio_file = "path_to_your_audio_file.mp3"  # Replace with your audio file path
uri = "ws://localhost:8765"

# Send the audio file to the server and receive the translated audio
asyncio.run(send_audio(uri, audio_file))
