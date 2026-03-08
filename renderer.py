import cv2

POSSIBLE_EMOTIONS = ['happy', 'sad', 'neutral', 'surprised', 'angry', 'fearful', 'disgust']

class Renderer():
    def __init__(self, imgPaths=None, speakingMode=False, bounceMode=False):
        self.emotionImgPaths = {}
        self.emotionImgs = {}
        for emotion in POSSIBLE_EMOTIONS:
            self.emotionImgPaths[emotion] = None
            self.emotionImgs[emotion] = None
        self.speakingMode = speakingMode # TODO: Add functionality where the avatar image is grayscaled when the user is not speaking but is colorized when the user is
        self.bounceMode = bounceMode # TODO: Add functionality where the avatar image bounces when the user starts speaking
        for emotion in POSSIBLE_EMOTIONS:
            print('emotion:', emotion)
            if imgPaths[emotion] is None:
                emotionImgPath = input('Please input the image file path for {}:'.format(emotion))
                self.addEmotionImage(emotion, emotionImgPath)
            else:
                self.addEmotionImage(emotion, imgPaths[emotion])

    def addEmotionImage(self, emotionType, imgPath):
        self.emotionImgPaths[emotionType] = imgPath
        emotionImg = cv2.imread(imgPath)
        if emotionImg is None:
            print('Could not read image {} for emotion {}!'.format(imgPath, emotionType))
            return
        self.emotionImgs[emotionType] = emotionImg
        cv2.imshow(emotionType, emotionImg)
        cv2.waitKey(1)

    def renderEmotionImg(self, emotionType):
        if emotionType not in POSSIBLE_EMOTIONS:
            print('emotion of type {} is not in the list of possible emotions!'.format(emotionType))
            return None
        renderedImg = emotionImgs[emotionType]

        if speakingMode:
            # TODO: Add functionality where the avatar image is grayscaled when the user is not speaking but is colorized when the user is
            pass
        if bouncingMode:
            # TODO: Add functionality where the avatar image bounces when the user starts speaking
            pass
        return renderedImg
        
