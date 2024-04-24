#include <gst/gst.h>
#include <gst/video/videooverlay.h>
#include <QApplication>
#include <QTimer>
#include <QWidget>


int main(int argc, char *argv[])
{
  QApplication app(argc, argv);
  app.connect(&app, SIGNAL(lastWindowClosed()), &app, SLOT(quit ()));
  
  
  if (!g_thread_supported ())
  g_thread_init (NULL);
  gst_init (&argc, &argv);

  // prepare the pipeline
  GstElement *pipeline = gst_pipeline_new (NULL);
  GstElement *src = gst_element_factory_make ("rtspsrc", "rtspsrc");
  g_object_set(G_OBJECT(src), "location", "rtsp://192.168.144.25:8554/main.264", NULL);
  g_object_set(G_OBJECT(src), "latency", 100, NULL); 

  GstElement *queue = gst_element_factory_make ("queue", NULL);
  GstElement *decode = gst_element_factory_make ("decodebin", NULL);

  GstElement *sink = gst_element_factory_make ("glimagesink", NULL);

  g_assert (src && queue && decode && sink);

  gst_bin_add_many (GST_BIN (pipeline), src, queue, decode, sink, NULL);
  gst_element_link_many (src, queue, decode, sink, NULL);
  // getting more information
  gst_debug_set_active(true);
  gst_debug_set_default_threshold(GST_LEVEL_WARNING);

  QWidget window;
  window.resize(320, 240);
  window.show();
  WId xwinid = window.winId();
  gst_video_overlay_set_window_handle (GST_VIDEO_OVERLAY (sink), xwinid);

  // run the pipeline

  GstStateChangeReturn sret = gst_element_set_state (pipeline,
  GST_STATE_PLAYING);
  if (sret == GST_STATE_CHANGE_FAILURE) {
  gst_element_set_state (pipeline, GST_STATE_NULL);
  gst_object_unref (pipeline);
  // Exit application
  QTimer::singleShot(0, QApplication::activeWindow(), SLOT(quit()));
  }
  }
