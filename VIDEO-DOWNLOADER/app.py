# app.py

from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
import platform
import logging

app = Flask(__name__)

def download_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()

        device_type = platform.system()
        save_path = get_download_path(device_type)

        video_stream.download(output_path=save_path)

        file_name = sanitize_filename(yt.title)
        file_path = os.path.join(save_path, file_name + '.mp4')

        return f"Download complete. Video saved at: {file_path}"
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def get_download_path(device_type):
    if device_type == "Windows":
        return os.path.expanduser("~\\Downloads")
    elif device_type == "Linux" or device_type == "Darwin":  # Darwin represents macOS
        return os.path.expanduser("~/Downloads")
    elif device_type == "Android":
        # On Android, you may need to adjust this path based on your file system
        return "/sdcard/Download"
    elif device_type == "iOS":
        # On iOS, you may need to adjust this path based on your file system
        return "~/Downloads"
    else:
        raise Exception(f"Unsupported device type: {device_type}")

def sanitize_filename(title):
    return "".join(c for c in title if c.isalnum() or c in (' ', '.', '_'))

@app.route("/api/download", methods=["POST"])
def api_download():
    try:
        data = request.get_json()
        video_url = data.get("video_url")
        result_message = download_youtube_video(video_url)
        return jsonify({"result_message": result_message})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
