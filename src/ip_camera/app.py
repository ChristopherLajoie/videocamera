import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

class VideoWorker(QThread):  # Thread for GStreamer pipeline
    frameAvailable = pyqtSignal(Gst.Sample) 

    def __init__(self, pipeline_str):
        super().__init__()
        self.pipeline = Gst.parse_launch(pipeline_str)

    def run(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        bus = self.pipeline.get_bus()
        msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ANY)

        if msg.type == Gst.MessageType.EOS:
            # Handle end-of-stream
            pass
        elif msg.type == Gst.MessageType.ERROR:
            # Handle errors
            pass  
        elif msg.type == Gst.MessageType.ELEMENT:
            if msg.structure.get_name() == "GstSample": 
                self.frameAvailable.emit(msg.get_structure().get_sample())

class VideoWidget(QWidget):
    def __init__(self, worker):
        super().__init__()

        self.image_label = QLabel()  
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

        worker.frameAvailable.connect(self.update_frame)

    def update_frame(self, sample):
        buf = sample.get_buffer()
        result, mapinfo = buf.map(Gst.MapFlags.READ)

        if result:
            # Assuming an RGB format"
            image = QImage(mapinfo.data, mapinfo.size[0], mapinfo.size[1], QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(image))

        buf.unmap(mapinfo)

class MyQtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My RTSP Player")

        # UI elements
        self.video_widget = VideoWidget(video_worker)
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

        # Layout (Using QHBoxLayout for buttons)
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.reset_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_widget)
        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

        # Signal connections 
        self.play_button.clicked.connect(self.start_video)  
        self.stop_button.clicked.connect(self.stop_video)
        self.reset_button.clicked.connect(self.reset_video)

    def start_video(self):
        if self.video_widget.worker:
            self.video_widget.worker.pipeline.set_state(Gst.State.PLAYING)

    def stop_video(self):
        if self.video_widget.worker:
            self.video_widget.worker.pipeline.set_state(Gst.State.PAUSED)

    def reset_video(self):
        if self.video_widget.worker:
            self.video_widget.worker.pipeline.set_state(Gst.State.NULL)  # Stop
            self.video_widget.worker.pipeline.set_state(Gst.State.PLAYING)  # Restart

if __name__ == "__main__":
    Gst.init(None)

    pipeline_str = "rtspsrc location=rtsp://192.168.144.25:8554/main.264 latency=100 ! queue ! decodebin ! xvimagesink"
    video_worker = VideoWorker(pipeline_str)

    app = QApplication([])
    window = MyQtApp()
    window.video_widget.worker = video_worker  # Connect worker to widget
    window.show()

    video_worker.start()  # Start the GStreamer thread
    app.exec_()