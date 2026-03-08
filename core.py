from fer.fer import FER
import cv2
from time import sleep
import keyboard

possibleEmotions = ['happy', 'sad', 'neutral', 'surprised', 'angry', 'fearful', 'disgust']

class Core():
    def __init__(self, input_module, renderer, output_module, debug=False):
        self.input_module = input_module
        self.renderer = renderer
        self.output_module = output_module
        self.debug = debug
        self.detector = FER()
        if debug:
            print('Core.__init__: detector loaded!')

    def oneLoop(self):
        frame = self.input_module.getFrame()
        if frame is None:
            return 0
        if frame.size == 0:
            return 0
        if self.debug:
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        results = self.detector.detect_emotions(frame)
        if len(results) > 0:
            emotions = results[0]['emotions']
            maxEmotion = max(emotions, key=emotions.get)
            if self.debug:
                print(emotions)
                print(maxEmotion)
            resultImg = self.renderer.renderEmotionImg(maxEmotion)
            output_code = self.output_module.outputImg(resultImg)
            if output_code == 1: # User hit the halt key
                return 1;
        return 0

    def run(self):
        status = 0
        while status==0:
            status = self.oneLoop()
        input_module.close()

