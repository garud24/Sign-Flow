import React, { useState, useEffect } from "react";
import VideoPlayer from "./VideoPlayer";
import AudioRecorder from "./AudioRecorder";
import VideoTotext from "./video_to_text.js";
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import "./App.css"; // Import the CSS file

function App() {
  const [videoId, setVideoId] = useState(null);

  // useEffect(() => {
  //   const fetchVideoPaths = async () => {
  //     try {
  //       const response = await fetch("http://127.0.0.1:5000/paths");
  //       const data = await response.json();
  //       console.log(data); // Log the data to see it

  //       // Set the first video path as the default videoId
  //       if (data.video_paths && data.video_paths.length > 0) {
  //         setVideoId(data.video_paths[0]); // Set the video ID to the first path
  //       }
  //     } catch (error) {
  //       console.error("Error fetching video paths:", error);
  //     }
  //   };

  //   fetchVideoPaths(); // Call the function on component mount
  // }, []); // Empty dependency array ensures it runs once when the component mounts

  const fetchVideoPaths = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/paths");
      const data = await response.json();
      console.log(data); // Log the data to see it

      // Set the first video path as the default videoId
      if (data.video_paths && data.video_paths.length > 0) {
        setVideoId(data.video_paths[0]); // Set the video ID to the first path
      }
    } catch (error) {
      console.error("Error fetching video paths:", error);
    }
  };

  useEffect(() => {
    // Log videoId after it has been updated
    if (videoId) {
      console.log("Updated videoId:", videoId);
    }
  }, [videoId]); // This useEffect runs when videoId is updated

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>SIGN FLOW</h1>
          <nav>
            <ul style={{ listStyle: 'none', display: 'flex', gap: '1rem' }}>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/video-to-text">Video to Text</Link></li>
              <li><Link to="/text-to-video">Text to Video</Link></li>
            </ul>
          </nav>
        </header>

        <main className="app-main">
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <AudioRecorder />
                  {videoId ? (
                    <VideoPlayer videoId={videoId} />
                  ) : (
                    <p>Loading video...</p>
                  )}
                  <div>
                    <button onClick={fetchVideoPaths} className="send-button">
                      Get ASL
                    </button>
                  </div>
                </>
              }
            />
            <Route path="/video-to-text" element={<VideoTotext />} />
            
          </Routes>
        </main>

        <footer className="app-footer">
          <p>Enjoy your viewing experience!</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
