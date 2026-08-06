import argparse
from src.core import Core
from src.renderer import Renderer
import json
import os
from src.config import ConfigInfo

def run(config_info: ConfigInfo):
    renderImg = config_info.render_img
    if config_info.output_type == 'h' or config_info.output_type == 'hotkey':
        from src.hotkeyModule import hotkeyModule
        config_info.render_img = False
        output_module = hotkeyModule()
    elif config_info.output_type == 'o' or config_info.output_type == 'obs':
        from src.obsModule import obsOutputModule
        obs_host = config_info.obs_config_info.obs_webserver_host
        obs_pw = config_info.obs_config_info.obs_webserver_password
        if obs_host is None or obs_pw is None:
            print('host or password for the OBS Webserver is not provided! Use -wh and -wp options to provide them!')
            quit()
        output_module = obsOutputModule(obs_host, obs_pw)
    elif config_info.output_type == 'w' or config_info.output_type == 'windowOutput':
        from src.windowModule import windowModule
        renderImg = True
        output_module = windowModule()
    else:
        print("output argument -o must be either hotkey(\'h\'), obs(\'o\'), or window(\'w\')")
        quit()

    if config_info.input_type == 'w' or config_info.input_type == 'webcam':
        webcam_idx = int(config_info.webcam_info.webcam_idx)
        from src.webcamModule import webcamModule
        input_module = webcamModule(webcam_idx)
    elif config_info.input_type == 'o' or config_info.input_type == 'obs':
        from src.obsModule import obsInputModule
        obs_host = config_info.obs_config_info.obs_webserver_host
        obs_pw = config_info.obs_config_info.obs_webserver_password
        if obs_host is None or obs_pw is None:
            print('host or password for the OBS Webserver is not provided! Use -wh and -wp options to provide them!')
            quit()
        input_module = obsInputModule(obs_host, obs_pw)
    else:
        print('input_module argument -i must be either input(\'i\') or obs(\'o\')')
        quit()

    print('{} is a file? {}'.format(config_path, os.path.isfile(config_path)))

    isDebug = config_info.is_debug

    if renderImg:
        coreObj = Core(input_module = input_module, renderer=renderer, output_module = output_module, debug = isDebug)
    else:
        coreObj = Core(input_module = input_module, output_module = output_module, renderImg = renderImg, debug = isDebug)

    coreObj.run()

        
