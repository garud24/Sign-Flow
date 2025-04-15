import React, { useRef, useEffect, useState } from "react";

const VideoPlayer = ({ videoId }) => {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (videoRef.current) {
      // Pause the current video if needed
      videoRef.current.pause();

      // Set the new video source
      videoRef.current.src = `http://127.0.0.1:5000/videos/${videoId}`;
      //videoRef.current.src = `http://127.0.0.1:5000/videos/1-xK5UtDSmE_3-2-rgb_front.mp4`;

      // Load the new video
      videoRef.current.load();

      // Optionally trigger play, but this may not work until the user interacts
      if (isPlaying) {
        videoRef.current.play();
      }
    }
  }, [videoId, isPlaying]); // Reset video when videoId changes

  // Handle click to start the video (user interaction)
  const handlePlayClick = () => {
    if (videoRef.current) {
      setIsPlaying(true); // Allow video to play
      videoRef.current.play(); // Play video after user interaction
    }
  };

  return (
    <div className="video-player">
      <video
        ref={videoRef}
        width="320"
        height="240"
        controls
        autoPlay
        onClick={handlePlayClick} // Handle play when clicked
      >
        <source
          src={`http://127.0.0.1:5000/videos/${videoId}`}
          type="video/mp4"
        />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default VideoPlayer;
