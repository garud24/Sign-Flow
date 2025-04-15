import speech_recognition as sr

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)  # You can replace with Whisper or another API
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Speech service is unavailable."

if __name__ == "__main__":
    text = speech_to_text("input.wav")  # Example audio file
    print("Recognized Text:", text)
