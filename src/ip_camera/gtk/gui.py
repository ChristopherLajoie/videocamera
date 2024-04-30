import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst

Gst.init(None)  
Gtk.init(None)

def stop_pipeline(button):
    pipeline.set_state(Gst.State.NULL)

# Gtk
win = Gtk.Window(title="Video Window")
win.connect("destroy", Gtk.main_quit)
win.set_default_size(600, 400)

box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
win.add(box)

# Gst
pipeline = None  

def create_pipeline():
    global pipeline
    if pipeline:
        stop_pipeline(None)  # Stop the existing pipeline before creating a new one
    pipeline = Gst.parse_launch("rtspsrc location=rtsp://192.168.144.25:8554/main.264 latency=100 ! queue ! decodebin ! videoconvert ! gtksink sync=false name=video_sink")

    video_sink = pipeline.get_by_name("video_sink")
    video_widget = video_sink.get_property("widget")

    parent_container = video_widget.get_parent()

    if parent_container:
        parent_container.remove(video_widget)

    box.pack_start(video_widget, True, True, 0)

    pipeline.set_state(Gst.State.PLAYING)
    
create_pipeline()  

stop_button = Gtk.Button.new_with_label("Stop")
stop_button.connect("clicked", stop_pipeline)
box.pack_start(stop_button, False, False, 0)


win.show_all()
Gtk.main()
