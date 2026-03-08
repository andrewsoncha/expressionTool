from fer.fer import FER
import cv2
from time import sleep
import keyboard

detector = FER()
cam = cv2.VideoCapture(1)

if not cam.isOpened():
    print('could not open camera!')
    return

while True:
    ret, frame = cam.read()
    cv2.imshow('me', frame)
    keyInput = cv2.waitKey(1)
    if keyInput=='q':
        break
    results = detector.detect_emotions(frame)
    if len(results) > 0:
        emotions = results[0]['emotions']
        print(emotions)
        print(max(emotions, key=emotions.get))
        maxEmotion = max(emotions, key=emotions.get)
        print(maxEmotion[0])
        keyboard.write(maxEmotion[0])
