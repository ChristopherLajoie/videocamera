import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst
from gi.repository import Gtk, Gst

Gst.init(None)

def create_pipeline(ip_numbers):
    pipelines = []
    for ip_number in ip_numbers:
        pipeline = f"rtspsrc location=rtsp://192.168.144.{ip_number}:8554/main.264 latency=100 ! queue ! decodebin ! videoconvert ! gtksink sync=false name=video_sink"
        pipelines.append(pipeline)
    
    #pipelines.append("videotestsrc ! videoconvert ! gtksink sync=false name=video_sink")
    #pipelines.append("videotestsrc ! videoconvert ! gtksink sync=false name=video_sink")
    return pipelines

class IPInputWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="IP Input")
        self.set_default_size(400, 200)
        self.ip_entries = []
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        for i in range(4):
            ip_entry = Gtk.Entry()
            self.box.pack_start(ip_entry, True, True, 0)
            self.ip_entries.append(ip_entry)

        self.start_button = Gtk.Button.new_with_label("Start")
        self.start_button.connect("clicked", self.on_start_clicked)
        self.box.pack_start(self.start_button, True, True, 0)

    def on_start_clicked(self, button):
        ip_numbers = [ip_entry.get_text() for ip_entry in self.ip_entries if ip_entry.get_text() != '']
        pipeline_string = create_pipeline(ip_numbers)
        main_window = MainWindow(pipeline_string)
        main_window.show_all()
        self.hide()

class MainWindow(Gtk.Window):
    def __init__(self, pipeline_string):
        Gtk.Window.__init__(self, title="Video Window")
        self.set_default_size(600, 400)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)

        self.boxes = []
        for _ in range(len(pipeline_string)):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.main_box.pack_start(box, True, True, 0)
            self.boxes.append(box)

        self.pipelines = [Gst.parse_launch(pipeline) for pipeline in pipeline_string]

        video_sinks = [pipeline.get_by_name("video_sink") for pipeline in self.pipelines]
        video_widgets = [video_sink.get_property("widget") for video_sink in video_sinks]
        parent_containers = [video_widget.get_parent() for video_widget in video_widgets]

        for parent_container, video_widget in zip(parent_containers, video_widgets):
            if parent_container:
                parent_container.remove(video_widget)

        for box, video_widget in zip(self.boxes, video_widgets):
            box.pack_start(video_widget, True, True, 0)

        for pipeline in self.pipelines:
            pipeline.set_state(Gst.State.PLAYING)

        for box, pipeline in zip(self.boxes, self.pipelines):
            stop_button = Gtk.Button.new_with_label("Stop")
            stop_button.connect("clicked", lambda button: self.on_stop_clicked(button, pipeline))
            box.pack_start(stop_button, False, False, 0)

        self.connect("destroy", self.on_destroy)

    def on_stop_clicked(self, pipeline, button):
        pipeline.set_state(Gst.State.NULL)
        #Gtk.main_quit()

    def on_destroy(self, window):
        for pipeline in self.pipelines:
            pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()


ip_input_window = IPInputWindow()
ip_input_window.connect("delete-event", Gtk.main_quit)
ip_input_window.show_all()

Gtk.main()
