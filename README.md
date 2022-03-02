# Webカメラ制御プログラム

フレームキャプチャと同時並行でwebカメラによる動画撮影を実行することを目的としたpythonプログラム

## 導入
```
$ git clone https://github.com/SK-eee-ku/webcam_with_packetcapture.git
```

## 使い方
現在，プレビューと録画ができる．
```
from video_capture import Video_cam

camera = Video_cam()

camera.preveiw() # カメラ映像のプレビュー，qキーで終了

#  10秒間の動画を録画
#  webcam_with_packetcapture/video_data/temp_00.mp4で保存される
camera.capture_and_save(
    "temp",
    time_capture=10,
)
```

## 出力ファイル
録画すると，サブディレクトリの"video_data"に動画データとエポック時のデータが保存される．エポック時は秒単位．
