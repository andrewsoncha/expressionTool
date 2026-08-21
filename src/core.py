from fer.fer import FER
import cv2
import time
import keyboard

possibleEmotions = ['happy', 'sad', 'neutral', 'surprise', 'angry', 'fearful', 'disgust']

class Core():
    def __init__(self, input_module, output_module, renderer=None, renderImg = True, sendImgPath = False, debug=False):
        self.input_module = input_module
        self.renderer = renderer
        self.output_module = output_module
        self.debug = debug
        self.detector = FER()
        self.renderImg = renderImg
        self.sendImgPath = sendImgPath
        if debug:
            print('Core.__init__: detector loaded!')

    def oneLoop(self):
        frame = self.input_module.getFrame()
        output_code = 0
        if frame is None:
            return 0
        if frame.size == 0:
            return 0
        if self.debug:
            cv2.imshow('input image', frame)
            cv2.waitKey(1)
        results = self.detector.detect_emotions(frame)
        if len(results) > 0:
            emotions = results[0]['emotions']
            maxEmotion = max(emotions, key=emotions.get)
            if self.debug:
                print('DEBUG: Emotion Values: ', emotions)
                print('DEBUG: Max Emotion: ', maxEmotion)
            if self.renderImg: # Render the avatar images (ex: Window mode or web Module)
                resultImg = self.renderer.renderEmotionImg(maxEmotion)
                output_code = self.output_module.outputImg(resultImg)
            elif self.sendImgPath: # Send the file path to the avatar image (ex: OBS ImageSource Output)
                imgPath = self.renderer.getEmotionImagePath(maxEmotion)
                if imgPath is not None:
                    output_code = self.output_module.outputImgPath(imgPath)
            else: # Press Hotkey instead of Rendering Image (ex: Hotkey Output)
                output_code = self.output_module.outputHotkey(maxEmotion)
            if output_code == 1: # User hit the halt key
                return 1;
        return 0

    def run(self):
        status = 0
        if self.debug == True:
            frameN = 0
            prevTime = time.time()
        while status==0:
            status = self.oneLoop()
            if self.debug == True:
                frameN += 1
                if time.time() - prevTime > 1:
                    print('DEBUG: fps = ', frameN)
                    prevTime = time.time()
                    frameN = 0
        self.input_module.close()

