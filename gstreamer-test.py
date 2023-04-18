import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib

# GStreamerを初期化
Gst.init(None)

# パイプライン文字列
pipeline_str = (
    "avfvideosrc ! "
    "video/x-raw, format=YUY2, width=640, height=480, framerate=30/1 ! "
    "queue ! videoconvert ! vp8enc ! rtpvp8pay ! "
    "udpsink host=dev.janus.jizaipad.jp port=5004"
)

# パイプラインを作成
pipeline = Gst.parse_launch(pipeline_str)

# パイプラインを再生状態に設定
pipeline.set_state(Gst.State.PLAYING)

# GLibのメインループを実行
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    # CTRL+Cが押されたら、ループを停止
    loop.quit()

# パイプラインをNULL状態に設定してクリーンアップ
pipeline.set_state(Gst.State.NULL)
