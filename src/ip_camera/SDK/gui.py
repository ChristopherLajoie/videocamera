import sys
import cv2  # Might still be useful for image manipulation
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
from siyi_sdk.stream import SIYIRTSP

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.rtsp_streams = []  # Store the stream objects

        layout = QGridLayout()
        self.image_labels = [
            QLabel(self) for _ in range(4)  
        ]
        for i, label in enumerate(self.image_labels):
            layout.addWidget(label, i // 2, i % 2) 

        self.setLayout(layout)
        self.setWindowTitle("Multi-Stream RTSP Viewer")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(30)  # Update approximately every 30 milliseconds

    def start_streams(self, urls):
        for url in urls:
            rtsp_stream = SIYIRTSP(rtsp_url=url, debug=False)
            self.rtsp_streams.append(rtsp_stream)

    def closeEvent(self, event):
        # You might need to explicitly close SIYI streams here
        for stream in self.rtsp_streams:
            # Add appropriate close or stop method from the SDK if needed
            pass 
    
    def update_frames(self):
        for stream, label in zip(self.rtsp_streams, self.image_labels):
            frame = stream.getFrame()
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV uses BGR
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    stream_urls = ['rtsp://192.168.144.25:8554/main.264'] 
    window.start_streams(stream_urls)

    window.show()
    sys.exit(app.exec())
