import cv2
from outputModule import outputModule

class windowModule(outputModule):
    def __init__(self, windowName='expressToolOutput'):
        self.windowName = windowName
        cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)

    def outputImg(self, img):
        if img is None:
            print('windowModule.show: the image is None!')
            return -1
        if img.shape == ():
            print('windowModule.show: the image is empty!')
            return -1
        cv2.imshow(self.windowName, img)
        keyInput = cv2.waitKey(1)
        if keyInput == 'q':
            return 1
        else:
            return 0
