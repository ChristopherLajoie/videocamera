#include <QApplication>
#include <QQmlApplicationEngine>
#include <QQuickWindow>
#include <QQuickItem>
#include <QRunnable>
#include <gst/gst.h>
#include <cstdlib> 

class SetPlaying : public QRunnable
{
public:
  SetPlaying(GstElement *);
  ~SetPlaying();

  void run ();

private:
  GstElement * pipeline_;
};

SetPlaying::SetPlaying (GstElement * pipeline)
{
  this->pipeline_ = pipeline ? static_cast<GstElement *> (gst_object_ref (pipeline)) : NULL;
}

SetPlaying::~SetPlaying ()
{
  if (this->pipeline_)
    gst_object_unref (this->pipeline_);
}

void
SetPlaying::run ()
{
  if (this->pipeline_)
    gst_element_set_state (this->pipeline_, GST_STATE_PLAYING);
}

int main(int argc, char *argv[])
{
  int ret;

  setenv("GST_DEBUG", "qmlglsink:4", 1); // Set environment variable
  gst_init (&argc, &argv);

  gst_debug_set_default_threshold(GST_LEVEL_INFO);  // Set debug level
  gst_debug_add_log_function(gst_debug_log_default, NULL, NULL); // Add default log function

  {
    QGuiApplication app(argc, argv);

    // Modified Pipeline Creation
    GstElement *pipeline = gst_pipeline_new (NULL);
    GstElement *src = gst_element_factory_make ("rtspsrc", "rtspsrc");
    g_object_set(G_OBJECT(src), "location", "rtsp://192.168.144.25:8554/main.264", NULL);
    g_object_set(G_OBJECT(src), "latency", 100, NULL); 
    
    GstElement *queue = gst_element_factory_make ("queue", NULL);
    GstElement *decode = gst_element_factory_make ("decodebin", NULL);

    GstElement *glupload = gst_element_factory_make ("glupload", NULL);
    GstElement *sink = gst_element_factory_make ("qmlglsink", NULL);

    g_assert (src && queue && decode && glupload && sink);

    gst_bin_add_many (GST_BIN (pipeline), src, queue, decode, glupload, sink, NULL);
    gst_element_link_many (src, queue, decode, glupload, sink, NULL);

    //GstElement *pipeline = gst_parse_launch("rtspsrc location=rtsp://192.168.144.25:8554/main.264 latency=100 ! queue ! decodebin ! qmlglsink", NULL);

    // Assuming 'videoItem' is still the name of the QML element
    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    QQuickItem *videoItem;
    QQuickWindow *rootObject;

    /* find and set the videoItem on the sink */
    rootObject = static_cast<QQuickWindow *> (engine.rootObjects().first());
    videoItem = rootObject->findChild<QQuickItem *> ("videoItem");
    g_assert (videoItem);

    rootObject->scheduleRenderJob (new SetPlaying (pipeline),
        QQuickWindow::BeforeSynchronizingStage);

    ret = app.exec();

    gst_element_set_state (pipeline, GST_STATE_NULL);
    gst_object_unref (pipeline);
  }

  gst_deinit ();

  return ret;
}