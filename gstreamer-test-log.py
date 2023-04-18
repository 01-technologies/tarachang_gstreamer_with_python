import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

# GStreamerを初期化
Gst.init(None)

# デバッグロギングを有効にし、ログレベルを設定
# GST_LEVEL_INFO, GST_LEVEL_ERROR, GST_LEVEL_WARNING, GST_LEVEL_DEBUG
Gst.debug_set_active(True)
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

# パイプライン文字列
pipeline_str = (
    "avfvideosrc ! "
    "video/x-raw, format=YUY2, width=640, height=480, framerate=30/1 ! "
    "queue ! videoconvert ! vp8enc ! rtpvp8pay ! "
    "udpsink host=dev.janus.jizaipad.jp port=5004"
)

# パイプラインを作成
pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)

# GLibのメインループを実行
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    loop.quit()

# パイプラインをNULL状態に設定してクリーンアップ
pipeline.set_state(Gst.State.NULL)
