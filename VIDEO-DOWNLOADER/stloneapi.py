import os
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from pytube import YouTube

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YouTube Video Downloader')

        self.label_url = QLabel('Enter YouTube video URL:')
        self.entry_url = QLineEdit()
        self.button_download = QPushButton('Download')
        self.button_download.clicked.connect(self.download_video)

        layout = QVBoxLayout()
        layout.addWidget(self.label_url)
        layout.addWidget(self.entry_url)
        layout.addWidget(self.button_download)

        self.setLayout(layout)

    def download_video(self):
        video_url = self.entry_url.text()

        try:
            # Create a YouTube object
            yt = YouTube(video_url)

            # Get the highest resolution stream
            video_stream = yt.streams.get_highest_resolution()

            # Get the user's device type
            device_type = platform.system()

            # Get the default download folder based on the device type
            if device_type == "Windows":
                save_path = os.path.expanduser("~\\Downloads")
            elif device_type == "Linux":
                save_path = os.path.expanduser("~/Downloads")
            elif device_type == "Darwin":  # macOS
                save_path = os.path.expanduser("~/Downloads")
            elif device_type == "Android":
                # On Android, you may need to adjust this path based on your file system
                save_path = "/sdcard/Download"
            else:
                raise Exception(f"Unsupported device type: {device_type}")

            # Download the video to the specified path
            video_stream.download(output_path=save_path)

            QMessageBox.information(self, 'Download Complete', f'Video saved at: {os.path.join(save_path, yt.title + ".mp4")}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication([])
    window = YouTubeDownloaderApp()
    window.show()
    app.exec_()
