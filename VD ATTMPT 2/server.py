from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube
import os
import platform

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS


def get_default_download_path():
  device_type = platform.system()

  if device_type == "Windows":
    return os.path.expanduser("~\\Downloads")
  elif device_type == "Linux":
    return os.path.expanduser("~/Downloads")
  elif device_type == "Darwin":  # macOS
    return os.path.expanduser("~/Downloads")
  elif device_type == "Android":
    return "/sdcard/Download"
  else:
    raise Exception(f"Unsupported device type: {device_type}")


@app.route('/api/download', methods=['POST'])
def download_video():
  try:
    video_url = request.json['video_url']
    yt = YouTube(video_url)
    video_stream = yt.streams.get_highest_resolution()

    save_path = get_default_download_path()
    video_stream.download(output_path=save_path)

    return jsonify({
        'result_message':
        f"Download complete. Video saved at: {os.path.join(save_path, yt.title + '.mp4')}"
    }), 200
  except Exception as e:
    return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
