import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def create_pipeline(ip_number):
    pipeline = f"rtspsrc location=rtsp://192.168.144.{ip_number}:8554/main.264 latency=100 ! queue ! decodebin ! videoconvert ! gtksink sync=false name=video_sink"
    return pipeline

class IPInputWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="IP Input")
        self.set_default_size(200, 100)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.ip_entry = Gtk.Entry()
        self.ip_entry.set_text("Enter IP Number")
        self.box.pack_start(self.ip_entry, True, True, 0)

        self.start_button = Gtk.Button.new_with_label("Start")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.box.pack_start(self.start_button, True, True, 0)

    def on_start_clicked(self, button):
        ip_number = self.ip_entry.get_text()
        pipeline_string = create_pipeline(ip_number)
        main_window = MainWindow(pipeline_string)
        main_window.show_all()
        self.hide()

class MainWindow(Gtk.Window):
    def __init__(self, pipeline_string):
        Gtk.Window.__init__(self, title="Video Window")
        self.set_default_size(600, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(box)

        self.pipeline = Gst.parse_launch(pipeline_string)

        video_sink = self.pipeline.get_by_name("video_sink")
        video_widget = video_sink.get_property("widget")

        parent_container = video_widget.get_parent()

        if parent_container:
            parent_container.remove(video_widget)

        box.pack_start(video_widget, True, True, 0)

        self.pipeline.set_state(Gst.State.PLAYING)

        self.stop_button = Gtk.Button.new_with_label("Stop")
        self.stop_button.connect("clicked", self.on_stop_clicked)
        box.pack_start(self.stop_button, False, False, 0)

        self.connect("destroy", self.on_destroy)

    def on_stop_clicked(self, button):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_destroy(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

# Gst
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

# Create IP input window
ip_input_window = IPInputWindow()
ip_input_window.connect("delete-event", Gtk.main_quit)
ip_input_window.show_all()

Gtk.main()
