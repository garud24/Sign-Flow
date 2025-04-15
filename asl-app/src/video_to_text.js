import React, { useEffect, useRef, useState, useCallback } from "react";
import { Hands } from "@mediapipe/hands/hands";
import { Camera } from "@mediapipe/camera_utils/camera_utils";

export default function VideoToText() {
  const videoRef = useRef(null);
  const [prediction, setPrediction] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [parsedData,setParsedata] = useState(null)

  const CONSISTENCY_THRESHOLD = 3;
  const recentPredictions = useRef([]);
  const lastPredictionTime = useRef(0);

  const sendToBackend = async (imageBlob) => {
    const formData = new FormData();
    formData.append("file", imageBlob, "frame.jpg");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict/", {
        method: "POST",
        body: formData,
      });

      const rawText = await response.text(); // must read before .json()
      console.log("🧪 Raw response:", rawText);

      if (!response.ok) throw new Error("Failed to fetch prediction");

      const data = JSON.parse(rawText); // parse manually since we already read it
      console.log("📩 Prediction received:", data);
      setParsedata(data);

      // Consistency buffer
      recentPredictions.current.push(data.prediction);
      if (recentPredictions.current.length > CONSISTENCY_THRESHOLD) {
        recentPredictions.current.shift();
      }

      const allSame = recentPredictions.current.every(
        (p) => p === recentPredictions.current[0]
      );

      if (
        allSame &&
        recentPredictions.current.length === CONSISTENCY_THRESHOLD &&
        data.prediction !== "nothing"
      ) {
        setPrediction(data);
      }
    } catch (err) {
      console.error("❌ Prediction error:", err);
      setPrediction(null);
      recentPredictions.current = [];
    }
  };

  const cropAndSend = useCallback(async (results) => {
    const now = Date.now();
    if (now - lastPredictionTime.current < 500) return;
    lastPredictionTime.current = now;

    if (!results.multiHandLandmarks || !results.multiHandLandmarks.length) return;

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    const landmarks = results.multiHandLandmarks[0];
    const width = videoRef.current.videoWidth;
    const height = videoRef.current.videoHeight;

    const xs = landmarks.map((pt) => pt.x * width);
    const ys = landmarks.map((pt) => pt.y * height);

    const xMin = Math.max(Math.min(...xs) - 60, 0);
    const yMin = Math.max(Math.min(...ys) - 60, 0);
    const xMax = Math.min(Math.max(...xs) + 60, width);
    const yMax = Math.min(Math.max(...ys) + 60, height);

    const cropW = xMax - xMin;
    const cropH = yMax - yMin;

    canvas.width = cropW;
    canvas.height = cropH;
    ctx.drawImage(videoRef.current, xMin, yMin, cropW, cropH, 0, 0, cropW, cropH);

    const resizedCanvas = document.createElement("canvas");
    resizedCanvas.width = 224;
    resizedCanvas.height = 224;
    const resizedCtx = resizedCanvas.getContext("2d");
    resizedCtx.drawImage(canvas, 0, 0, 224, 224);

    resizedCanvas.toBlob((blob) => {
      setPreviewUrl(URL.createObjectURL(blob));
      sendToBackend(blob);
    }, "image/jpeg", 0.9);
  }, []);

  useEffect(() => {
    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7,
    });

    hands.onResults(cropAndSend);

    if (videoRef.current) {
      const camera = new Camera(videoRef.current, {
        onFrame: async () => {
          await hands.send({ image: videoRef.current });
        },
        width: 640,
        height: 480,
      });

      camera.start();
    }
  }, [cropAndSend]);

  return (
    <div className="flex flex-col items-center p-6 gap-4">
      <h1 className="text-2xl font-bold">🤖 ASL Letter Recognizer</h1>

      <video
        ref={videoRef}
        className="rounded-xl shadow-md border"
        autoPlay
        muted
        playsInline
        width="640"
        height="480"
      />
      {parsedData ? (
  <pre className="bg-gray-100 p-2 rounded text-sm w-full max-w-md overflow-x-auto">
    <strong>Prediction:</strong>{JSON.stringify(parsedData.prediction?.prediction, null, 2)}
  </pre>
) : (
  <p>No Data</p>
)}

      {prediction?.prediction && (
        <div className="text-xl mt-4 p-4 bg-white rounded shadow text-center">
          <p>
            <strong>Prediction:</strong> {prediction.prediction}
          </p>
          <p>
            <strong>Confidence:</strong> {Number(prediction.confidence).toFixed(2)}%
          </p>
        </div>
      )}

      {!prediction && (
        <p className="text-gray-500 mt-2">🕵️ Waiting for consistent gesture...</p>
      )}

      {previewUrl && (
        <div className="mt-4">
          <img
            src={previewUrl}
            alt="Cropped preview"
            className="w-48 rounded border"
          />
        </div>
      )}
    </div>
  );
}
