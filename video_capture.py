import os
import re
import math
import time

import cv2
import numpy as np

ROOT_DIR = os.path.dirname(__file__)
VIDEO_DATA_DIR = os.path.join(ROOT_DIR, "video_data")
os.makedirs(VIDEO_DATA_DIR, exist_ok=True)


def fname_creator(fname_prefix):
    fnames_exist = [f.split(".")[0] for f in os.listdir(
        VIDEO_DATA_DIR) if fname_prefix in f]

    if len(fnames_exist) == 0:
        return "{}_00_video.mp4".format(fname_prefix)
    else:
        fnames_exist_number = [int(re.sub(r'\D', "", f)) for f in fnames_exist]
        max_number = max(fnames_exist_number)
        return "{}_{:02}_video.mp4".format(fname_prefix, max_number + 1)


class Video_cam():

    def __init__(self, cam_num=0):
        self._cam = cv2.VideoCapture(cam_num)
        self.width = int(self._cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if math.isnan(self._cam.get(cv2.CAP_PROP_FPS)):
            self.fps = 30
            self._cam.set(cv2.CAP_PROP_FPS, 30)
        else:
            self.fps = int(self._cam.get(cv2.CAP_PROP_FPS))

    def __del__(self):
        self._cam.release()

    def preveiw(self):
        '''
        カメラの画角を確認するための関数
        qキーで終了
        '''
        while True:
            ret, frame = self._cam.read()
            cv2.imshow("camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def capture_and_save(
        self,
        video_name_prefix="sample",
        time_capture=None,
        num_capture_frames=None,
    ):
        '''
        動画の撮影，保存の関数．
        動画の名前は接頭辞を指定することで，ファイル名が被らない番号を降ってから保存する．
        '''

        video_name = fname_creator(video_name_prefix)

        if time_capture is None and num_capture_frames is None:
            num_capture_frames = 60 * self.fps
        elif num_capture_frames is None:
            num_capture_frames = int(time_capture * self.fps)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_writer = cv2.VideoWriter(
            os.path.join(VIDEO_DATA_DIR, video_name),
            fourcc,
            self.fps,
            (self.width, self.height))

        epoch_time = np.zeros(num_capture_frames, dtype=np.float64)

        for i in range(num_capture_frames):
            ret, frame = self._cam.read()
            video_writer.write(frame)
            epoch_time[i] = time.time()

        np.save(os.path.join(VIDEO_DATA_DIR,
                "{}_epoch".format(video_name.split(".")[0])), epoch_time)


if __name__ == '__main__':
    temp = fname_creator("temp")
    print(temp)
