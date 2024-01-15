from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
import platform

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        video_url = request.json.get('video_url')

        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()

        device_type = platform.system()
        if device_type == "Windows":
            save_path = os.path.expanduser("~\\Downloads")
        elif device_type == "Linux":
            save_path = os.path.expanduser("~/Downloads")
        elif device_type == "Darwin":  # macOS
            save_path = os.path.expanduser("~/Downloads")
        elif device_type == "Android":
            save_path = "/sdcard/Download"
        else:
            raise Exception(f"Unsupported device type: {device_type}")

        video_stream.download(output_path=save_path)

        result_message = f"Download complete. Video saved at: {os.path.join(save_path, yt.title + '.mp4')}"
        return jsonify(result_message=result_message)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
