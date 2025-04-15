import os
import requests
import pyaudio
import wave
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app1 = FastAPI()
# Allow all origins (or specify your React app's URL if you want to restrict it)
app1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can replace "*" with "http://localhost:3000" for stricter CORS policy
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)



# Create directories if they don't exist
os.makedirs("mic_to_audio", exist_ok=True)

def record_audio(filename="mic_to_audio/recorded_audio.wav", duration=5, rate=44100, channels=1, chunk=1024):
    """Records audio from the microphone and saves it as a WAV file."""
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16, 
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    print("🎤 Recording...")
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    print("✅ Recording finished.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
    
    return filename

@app1.get("/send-audio")
def send_audio():
    """Records audio and sends it to the Flask API."""
    file_path = record_audio()
    url = "http://127.0.0.1:5000/convert"  # Flask server endpoint
    
    with open(file_path, "rb") as audio_file:
        files = {"audio": audio_file}
        response = requests.post(url, files=files)
    
    print(f"🔄 Server Response: {response.json()}")  # Debugging line
    return {"response": response.json()}
