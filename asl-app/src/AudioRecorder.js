import React, { useState, useRef } from "react";
import "./AudioRecorder.css";

import Recorder from "recorder-js";

const AudioRecorder = () => {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const recorderRef = useRef(null);
  const audioContextRef = useRef(null);

  const startRecording = async () => {
    try {
      // Set up the audio context and recorder
      const audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      audioContextRef.current = audioContext;

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new Recorder(audioContext);
      recorderRef.current = recorder;

      recorder.init(stream);
      recorder.start();
      setRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = async () => {
    if (recorderRef.current) {
      const { blob } = await recorderRef.current.stop();
      setAudioBlob(blob);
      setRecording(false);
    }
  };

  const sendAudioToFlask = async () => {
    if (!audioBlob) return alert("No audio recorded!");

    const formData = new FormData();
    formData.append("audio", audioBlob, "audio.wav");

    try {
      const response = await fetch("http://127.0.0.1:5000/convert", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      console.log("Server Response:", result);
    } catch (error) {
      console.error("Error sending audio:", error);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-lg w-80 text-center">
      <h2 className="text-lg font-semibold mb-2">🎤 Audio Recorder</h2>
      <button
        onClick={recording ? stopRecording : startRecording}
        className={`record-button ${recording ? "bg-red" : "bg-blue"}`}
      >
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {audioBlob && (
        <div className="mt-4">
          <audio controls src={URL.createObjectURL(audioBlob)}></audio>
          <button onClick={sendAudioToFlask} className="send-button">
            Send to Backend
          </button>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
