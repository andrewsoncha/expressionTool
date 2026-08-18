import cv2
from src.outputModule import outputModule
import obsws_python as obs
from obsws_python.error  import OBSSDKRequestError
import time

class obsOutputModule(outputModule):
    def __init__(self, obs_host: str='localhost', obs_port: int=4455, obs_pw: str='', scene_name: str='', input_name: str='expressionTool'):
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_pw = obs_pw
        print('INFO obsOutputModule: obs_host {}    obs_port {}   obs_pw {}'.format(self.obs_host, self.obs_port, self.obs_pw))

        if self.obs_pw == '':
            self.cl = obs.ReqClient(host=self.obs_host, port=self.obs_port)
        else:
            self.cl = obs.ReqClient(host=self.obs_host, port=self.obs_port, password=self.obs_pw)

        if self.cl is None:
            print('ERROR obsModule.py: Unable to connect to OBS Websocket server(host: {},  port: {})!'.format(self.obs_host, self.obs_port))
            return

        if scene_name == '':
            response = self.cl.send('GetCurrentProgramScene', raw=True)
            if 'sceneName' not in response:
                print('ERROR obsModule.py: Unable to get current program scene from OBS webserver!')
                return
            self.scene_name = response['sceneName']
            print('INFO obsModule.py: Scene Name: {}'.format(self.scene_name))
        else:
            self.scene_name = scene_name
        self.inputName = input_name

        try:
            response = self.cl.send('CreateInput', data = {
                'sceneName': self.scene_name,
                'inputName': self.inputName,
                'inputKind': 'image_source',
                'inputSettings': {
                    'file':'' 
                }
            })
        except OBSSDKRequestError as e:
            print('INFO obsModule.py:  OBSSDKRequest error. Likely means that the source already exists. Please ignore.')
            print('e: ', e)

    def outputImgPath(self, imagePath: str) -> int:
        print('outputImgPath({})'.format(imagePath))
        try:
            response = self.cl.send('SetInputSettings', data = {
                'sceneName': self.scene_name,
                'inputName': self.inputName,
                'inputSettings': {
                    'file': imagePath
                }
            })
            return 0
        except  OBSSDKRequestError as e:
            print('ERROR obsModule.py: OBSSDKRequestError')
            print('e: ', e)
            return 1


