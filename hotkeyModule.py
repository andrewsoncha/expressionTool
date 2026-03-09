from pyautogui import keyDown, keyUp
from outputModule import outputModule

class hotkeyModule(outputModule):
    def __init__(self, emotionHotkeys=None):
        self.emotionHotkeys = {}
        if emotionHotkeys is not None:
            self.emotionHotkeys = emotionHotkeys

    def updateHotkeys(self, newHotkeyDict):
        self.emotionHotkeys = newHotkeyDict

    def outputHotkey(self, emotion):
        if emotion not in self.emotionHotkeys:
            print('hotkeyModule.outputHotkey: no hotkey for emotion {}!'.format(emotion))
        else:
            hotkeyStr = self.emotionHotkeys[emotion]
            print('pressing hotkeyStr:', hotkeyStr)
            keyDown(hotkeyStr)
            keyUp(hotkeyStr)
