import os
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from scripts.speech_to_text import speech_to_text
from scripts.text_to_sign import convert_to_sign_grammar
from scripts.sign_mapping import match_sentence_to_video


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# Define the folder where your videos are stored
VIDEO_FOLDER = os.path.join(
    os.getcwd(), "data", "sign_videos"
)  # Path to the videos folder
FINAL_PATH = os.path.join(
    os.getcwd(), "final_path", "matched_path.txt"
)  # Path to the matched_path.txt file


os.makedirs("audio_to_text", exist_ok=True)
os.makedirs("text_to_sign", exist_ok=True)
os.makedirs("final_path", exist_ok=True)


def convert_audio_to_wav(audio_path):
    """Convert any audio format to WAV."""
    try:
        # Using pydub to load the audio file and export it as WAV
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(audio_path.split(".")[-1], "wav")
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        raise ValueError(f"Error converting audio to WAV: {e}")


@app.route("/convert", methods=["POST"])
def convert():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_path = "mic_to_audio/react_temp_audio.wav"
    # audio_path = "mic_to_audio/temp_audio.wav"
    audio_file.save(audio_path)

    print(f"✅ Audio file saved at: {audio_path}")

    # Convert the audio to WAV if it's not already in that format
    if not audio_path.endswith(".wav"):
        try:
            audio_path = convert_audio_to_wav(audio_path)
            print(f"✅ Audio converted to WAV: {audio_path}")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # # Step 1: Convert speech to text
    text = speech_to_text(audio_path)

    # Save the transcribed text in a file
    text_filename = f"audio_to_text/transcription.txt"
    with open(text_filename, "w") as f:
        f.write(text)

    print(f"📝 Recognized Text: {text}")

    # Step 2: Convert text to sign language grammar
    sign_sentence = convert_to_sign_grammar(text)

    # Save the transcribed sign text in a file
    sign_text_filename = f"text_to_sign/sign_transcription.txt"
    with open(sign_text_filename, "w") as f:
        f.write(sign_sentence)

    # Step 3: Map to sign videos
    video_paths = match_sentence_to_video(sign_sentence)

    # Save the transcribed sign text in a file
    path_filename = f"final_path/matched_path.txt"
    with open(path_filename, "w") as f:
        f.write("\n".join(video_paths))

    print(f"📝 Recognized Text: {text}")
    print(f"📝 Recognized Text: {sign_sentence}")
    print(f"📝 Recognized Text: {video_paths}")

    return jsonify(
        {"text": text, "sign_sentence": sign_sentence, "videos": video_paths}
    )


# Serve video files
# @app.route('/videos', methods=['GET'])
# def serve_video():
#     try:
#         # Read the matched_path.txt file and get the first video path
#         with open(FINAL_PATH, 'r') as file:
#             video_paths = file.readlines()

#         # Extract the first video path (ignoring the index number)
#         video_path = video_paths[0].strip().split()[0]  # Get the actual video path
#         print(f"Serving video: {video_path}")

#         # Send the video from the VIDEO_FOLDER
#         return send_from_directory(VIDEO_FOLDER, f"{video_path}.mp4")

#     except Exception as e:
#         return jsonify({"error": str(e)}), 404


@app.route("/paths", methods=["GET"])
def give_paths():
    try:
        # Read the matched_path.txt file to get the list of video paths
        with open(FINAL_PATH, "r") as file:
            video_paths = file.readlines()

        # Clean up paths (strip newline characters and add .mp4 extension)
        video_paths = [path.strip() + ".mp4" for path in video_paths]

        # Return video paths in JSON format
        return jsonify({"video_paths": video_paths})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/videos/<filename>", methods=["GET"])
def stream_video(filename):
    video_path = os.path.join(VIDEO_FOLDER, filename)

    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    def generate_video():
        with open(video_path, "rb") as f:
            while chunk := f.read(1024 * 8):  # Read 8KB at a time
                yield chunk

    return Response(generate_video(), content_type="video/mp4")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
