import json
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ObsConfigInfo:
    obs_host: str = 'localhost'
    obs_port: int = 4455
    obs_pw: str = '' # The password will not be saved in the config file
    obs_input_source: str = 'expressionTool Input Source' # The name of the OBS source that will be fed to this tool
    obs_output_source: str = 'expressionTool Output Source' # The name of the OBS source that this tool will output to
    def __init__(self):
        self.obs_host = 'localhost'
        self.obs_port = 4455
        self.obs_pw = ''
        self.obs_input_source = 'expressionTool Input Source'
        self.obs_output_source = 'expressionTool Output Source'

@dataclass
class WebcamInfo:
    webcam_idx: int = 1

@dataclass
class AvatarImageInfo:
    imagePaths: dict[str, str] = field(default_factory=dict)
    def __init__(self):
        base_path = Path(__file__).parent.parent.resolve()
        self.imagePaths = {
            'happy': str(base_path) + '/testImgs/happy_square.png',
            'sad': str(base_path) + '/testImgs/sad_square.png',
            'neutral': str(base_path) + '/testImgs/neutral_square.png',
            'surprise': str(base_path) + '/testImgs/surprise_square.png',
            'angry': str(base_path) + '/testImgs/angry_square.png',
            'fearful': str(base_path) + '/testImgs/fearful_square.png',
            'disgust': str(base_path) + '/testImgs/disgust_square.png'
            }

@dataclass
class HotkeyInfo:
    hotKeyInfo: dict[str, str] = field(default_factory=dict)
    def __init__(self):
        self.hotkeyInfo = {
            'happy': 'h',
            'sad': 's',
            'neutral': 'n',
            'surprise': 'u',
            'angry': 'a',
            'fearful': 'f',
            'disgust': 'd'
            }

@dataclass
class ConfigInfo:
    is_debug: bool = False
    render_img: bool = False
    send_img_path: bool = False
    output_type: str = 'w' # 'w': Window Output    'o': OBS Output  'h': Hotkey Output
    input_type: str = 'w' # 'w': webcam input     'o': obs input
    window_name: str = 'expressionTool output'
    obs_config_info: ObsConfigInfo = field(default_factory = ObsConfigInfo)
    webcam_info: WebcamInfo = field(default_factory = WebcamInfo)
    avatar_image_info: AvatarImageInfo = field(default_factory = AvatarImageInfo)
    hotkey_info: HotkeyInfo = field(default_factory = HotkeyInfo)
    def setIsDebug(self, input_is_debug: bool):
        self.is_debug = input_is_debug
        return self
    def setRenderImg(self, input_render_img: bool):
        self.render_img = input_render_img
        self.send_img_path = not input_render_img
        return self
    def setSendPath(self, input_send_img_path: bool):
        self.send_img_path = input_send_path
        self.render_img = not input_send_img_path
        return self
    def setOutputType(self, input_output_type: str):
        self.output_type = input_output_type
        if input_output_type == 'w' or input_output_type == 'o':
            self.setRenderImg(True)
        else:
            self.setRenderImg(False)
        return self
    def setInputType(self, input_input_type: str):
        self.input_type = input_input_type
        return self
    def setOBSHost(self, input_obs_host: str):
        self.obs_config_info.obs_host = input_obs_host
        return self
    def setOBSOutputSource(self, input_obs_output_source: str):
        self.obs_config_info.obs_output_source = input_obs_output_source
        return self
    def setOBSInputSource(self, input_obs_input_source: str):
        self.obs_config_info.obs_input_source = input_obs_input_source
        return self
    def setOBSPW(self, input_obs_pw: str):
        self.obs_config_info.obs_pw = input_obs_pw
        return self
    def setWebcamIdx(self, input_webcam_info: int):
        self.webcam_info.webcam_idx = input_webcam_info
        return self

def writeConfigInfo(configInfo: ConfigInfo, path: str = 'config.json'):
    saveConfigDict = { 'is_debug': configInfo.is_debug, \
            'render_img': configInfo.render_img, \
            'send_img_path': configInfo.send_img_path, \
            'output_type': configInfo.output_type, \
            'input_type': configInfo.input_type }

    # If the set input or output type is OBS, save OBS Websocket Host data.
    # The OBS Websocket Password will not be saved
    if configInfo.output_type == 'o' or configInfo.input_type == 'o':
        saveConfigDict['obs_config_info'] = {
                'obs_host': configInfo.obs_config_info.obs_host,
                'obs_output_source': configInfo.obs_config_info.obs_output_source,
                'obs_input_source': configInfo.obs_config_info.obs_input_source,
                }
    saveConfigDict['hotkey_info'] = configInfo.hotkey_info.hotkeyInfo

    saveConfigDict['avatar_image_info'] = configInfo.avatar_image_info.imagePaths

    try:
        with open(path, 'w') as f:
            json.dump(saveConfigDict, f)
    except FileNotFoundError:
        print('config.py writeConfigInfo ERROR: Could not find file {}'.format(path))
    except PermissionError:
        print('config.py writeConfigInfo ERROR: No Permission to open file {}'.format(path))

def readConfigInfo(path: str = 'config.json') -> ConfigInfo:
    resultConfigInfo = ConfigInfo()
    try: 
        with open(path, 'r') as f:
            configDict = json.load(f)
            resultConfigInfo.setIsDebug(configDict['is_debug'])
            resultConfigInfo.setRenderImg(configDict['render_img'])
            resultConfigInfo.setSendPath(configDict['send_img_path'])
            resultConfigInfo.setOutputType(configDict['output_type'])
            resultConfigInfo.setInputType(configDict['input_type'])
            resultConfigInfo.setOBSHost(configDict['obs_config_info']['obs_host'])
            resultConfigInfo.setOBSOutputSource(configDict['obs_config_info']['obs_output_source'])
            resultConfigInfo.setOBSInputSource(configDict['obs_config_info']['obs_input_source'])
            resultConfigInfo.hotkey_info.hotkeyInfo = configDict['hotkey_info']
            resultConfigInfo.avatar_image_info.impagePaths = configDict['avatar_image_info']
    except FileNotFoundError:
        print('config.py readConfigInfo ERROR: Could not find file {}'.format(path))
    except PermissionError:
        print('config.py readConfigInfo ERROR: No Permission to open file {}'.format(path))

    return resultConfigInfo
