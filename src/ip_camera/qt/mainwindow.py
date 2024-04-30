import sys
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')  # Specify the Gtk version
from gi.repository import Gst, Gtk, GLib
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from mainwindow_ui import Ui_Form
import platform

# Initialize GStreamer
Gst.init(None)
Gtk.init()


class VideoPlayer(QMainWindow, Ui_Form):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setupUi(self)

        self.pipeline = None
        self.video_window = None  # This will hold the window handle

        self.pushButton.clicked.connect(self.start_pipeline)
        self.pushButton_2.clicked.connect(self.stop_pipeline)

    def start_pipeline(self):
        if not self.pipeline:
            # Create a DrawingArea for gtksink
            drawing_area = Gtk.DrawingArea()
            drawing_area.set_size_request(640, 480)  # Set size if needed

            GLib.timeout_add(500, drawing_area.realize)
            #drawing_area.realize()  # Ensure the widget is realized

            # Create the pipeline with an initial gtksink
            self.pipeline = Gst.parse_launch(
                f'rtspsrc location=rtsp://192.168.144.25:8554/main.264 latency=100 ! '
                f'queue ! decodebin ! videoconvert ! gtksink name=sink sync=false'
            )
                
             # Get the gtksink element 
            sink = self.pipeline.get_by_name("sink")

            # Connect to the 'realize' signal of the embedded widget
            widget = sink.get_property("widget")
            widget.connect("realize", self.on_widget_realized)


            # Start the pipeline
            self.pipeline.set_state(Gst.State.PLAYING)

            self.status_label.setText("Pipeline Running")

    def on_widget_realized(self, widget):
        self.video_window = widget.get_window().get_xid()
        
        # Find the placeholder widget
        video_placeholder = self.findChild(QWidget, "video_widget")  

        # Create a QWindow from the window ID
        video_window = QWindow.fromWinId(self.video_window)

        # Create the window container and embed the QWindow
        container = QWidget.createWindowContainer(video_window, parent=video_placeholder)

        # Add the container to the video placeholder's layout
        layout = QVBoxLayout(video_placeholder)
        layout.addWidget(container)

    def stop_pipeline(self):
        if self.pipeline:
            # Stop the pipeline
            self.pipeline.set_state(Gst.State.NULL)
            self.pipeline = None

            self.status_label.setText("Pipeline Stopped")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())