import cv2
from inputModule import inputModule

class webcamModule(inputModule):
    def __init__(self, webcam_idx=1, debug=False):
        super().__init__(debug)
        if debug:
            print('webcamModule.__init__: opening cv.VideoCapture with webcam_idx:{}'.format(webcam_idx))
        self.cam = cv2.VideoCapture(webcam_idx)
        if not self.cam.isOpened():
            print('webcamModule.__init__: Could not open webcam_idx {}!'.format(webcam_idx))
            exit()
            return -1
    def getFrame(self):
        ret, frame = self.cam.read()
        if self.debug:
            cv2.imshow('webcamModule frame', frame)
            cv2.waitKey(1)
        return frame
    def close(self):
        self.cam.release()
