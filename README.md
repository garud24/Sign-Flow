# Sign-Flow

# 🤟 Sign Flow: Real-Time Sign Language to Speech Interface

*Bridging gestures to voice — and voice to gestures — with AI-powered ASL interpretation.*

---

## 📌 Overview

**Sign Flow** is a real-time, bidirectional ASL interpretation system that enables:

- ✋ Translating **ASL gestures** into **text and speech**
- 🎤 Converting **spoken audio** into **corresponding ASL video segments**

It’s built using deep learning, computer vision, speech recognition, and real-time video rendering — delivering inclusive communication in both directions.

---

## 🚀 Features

### 🎥 Sign-to-Text + Speech

- Live **ASL gesture recognition** using webcam input
- **CNN model** trained on ASL alphabet dataset with 95%+ accuracy
- **MediaPipe Hands** for landmark-based cropping
- **Prediction buffering** for consistency
- **GPT & TTS integration** to form and speak full sentences

### 🔁 Audio-to-ASL Video

- Input a **spoken phrase** via microphone or file
- Extracted **keywords** trigger matching **ASL gesture videos**
- Dynamically stream matching video clips from `data/sign_videos/` to the frontend

---

## 🛠️ Tech Stack

| Layer        | Technologies                                       |
|--------------|----------------------------------------------------|
| Frontend     | React, Tailwind CSS, MediaPipe Hands, CameraUtils |
| Backend      | Python, FastAPI, PyTorch, TorchVision, SpeechRecognition |
| ML Model     | ResNet18 CNN (custom-trained on ASL dataset)       |
| Audio        | SpeechRecognition, PyDub, MoviePy, ffmpeg          |
| Video        | HTML5 video rendering from static ASL video clips  |
| Extras       | GPT for NLP-based text enhancement + sentence prediction |

---

## 📂 Folder Structure
```
sign-flow/
│
├── backend/                             # FastAPI backend for ASL recognition
│   ├── inference/
│   │   ├── model.py                     # PyTorch model loading + prediction
│   │   ├── hand_detector.py            # MediaPipe hand cropping logic
│   ├── models/
│   │   └── asl_cnn_model.pt            # Trained ASL CNN model
│   ├── main.py                          # FastAPI app (predict endpoint)
│   ├── requirements.txt
│
├── audio_to_sign/                      # Audio to ASL Video module
|   |── data/
│   |     ├── sign_videos/                   # ASL gesture videos (e.g., hello.mp4, thankyou.mp4)
│   |     └── samples/ 
│   ├── mic_to_audio/
│   │   ├── recorded_audio.wav
│   │   ├── temp_audio.wav
│   │   └── react_temp_audio.wav
│   ├── final_path/
│   │   └── matched_path.txt
│   ├── text_to_sign/
│   │   ├── sign_transcription.txt
│   ├── scripts/
│   │   ├── speech_to_text.py           # Converts audio → text
│   │   ├── sign_mapping.py             # Maps text → video paths
│   │   └── text_to_sign.py             # Core logic: sentence → sign video sequence
│   ├── fastapi_send_audio.py           # Optional: Audio upload + video stream API
│   ├── app.py                          # Stream ASL videos for input sentence
│   └── requirements.txt
│
├── asl-app/                            # React frontend
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── logo512.png (etc.)
│   ├── src/
│   │   ├── App.js
│   │   ├── AudioRecorder.js            # Audio recorder component
│   │   ├── VideoPlayer.js              # ASL video stream player
│   │   ├── video_to_text.js            # Hand gesture → prediction React component
│   │   ├── index.js
│   │   └── styles/
│   │       ├── App.css
│   │       ├── AudioRecorder.css
│   │       └── VideoPlayer.css
│   └── package.json
│
└── README.md

```


## ⚙️ Setup Instructions

### 🔹 Backend (FastAPI + PyTorch + Audio)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```


### 🔹 Frontend (React + Tailwind)

cd frontend
npm install
npm run dev



### 🧪 Examples
### 🖐️ ASL Gesture Input

{
  "prediction": {
    "prediction": "H",
    "confidence": 97.35
  }
}


### 🔊 Audio-to-ASL Input
### Input: "Thank you very much"
### → Plays: data/sign_videos/thank.mp4 + you.mp4


### 📊 Dataset
- ASL Alphabet Dataset (Kaggle)

- Custom image captures using webcam

- how2Sign videos for common words stored in data/sign_videos/

### 🔮 Future Enhancements
- ✋ Full-word gesture detection from landmarks

- 🧠 Transformer model for sequential sign recognition

- 🎤 Live microphone transcription to video

- ☁️ Cloud deployment (e.g., HuggingFace, Vercel, or Streamlit)

# 🧑‍💻 Author
- Himanshu & Sourav
- Computer Science Graduate | UNC Charlotte
- [GitHub](https://github.com/garud24) • [LinkedIn](https://www.linkedin.com/in/himanshu-garud/)

