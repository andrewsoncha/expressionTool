import argparse
from core import Core
from renderer import Renderer
import json
import os

config_path = './config.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_type', default='w')
    parser.add_argument('-i', '--input_type', default='w')
    parser.add_argument('-ci', '--webcam_idx', default='1')
    parser.add_argument('-wh', '--obs_webserver_host')
    parser.add_argument('-wp', '--obs_webserver_password')
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()
    output_type = args.output_type
    input_type = args.input_type
    
    if output_type == 'h' or output_type == 'hotkey':
        from hotkeyModule import hotkeyModule
        output_module = hotkeyModule()
    elif output_type == 'o' or output_type == 'obs':
        from obsModule import obsOutputModule
        obs_host = args.obs_webserver_host
        obs_pw = args.obs_webserver_password
        if obs_host is None or obs_pw is None:
            print('host or password for the OBS Webserver is not provided! Use -wh and -wp options to provide them!')
            quit()
        output_module = obsOutputModule(obs_host, obs_pw)
    elif output_type == 'w' or output_type == 'windowOutput':
        from windowModule import windowModule
        output_module = windowModule()
    else:
        print("output argument -o must be either hotkey(\'h\'), obs(\'o\'), or window(\'w\')")
        quit()

    if input_type == 'w' or input_type == 'webcam':
        webcam_idx = int(args.webcam_idx)
        from webcamModule import webcamModule
        input_module = webcamModule(webcam_idx)
    elif input_type == 'o' or input_type == 'obs':
        from obsModule import obsInputModule
        obs_host = args.obs_webserver_host
        obs_pw = args.obs_webserver_password
        if obs_host is None or obs_pw is None:
            print('host or password for the OBS Webserver is not provided! Use -wh and -wp options to provide them!')
            quit()
        input_module = obsInputModule(obs_host, obs_pw)
    else:
        print('input_module argument -i must be either input(\'i\') or obs(\'o\')')
        quit()

    print('{} is a file? {}'.format(config_path, os.path.isfile(config_path)))

    readEmotionImgPaths = {}

    if os.path.isfile(config_path):
        with open(config_path, 'r') as config_file:
            config_dict = json.load(config_file)
            if 'emotionImgPaths' in config_dict:
                readEmotionImgPaths = config_dict['emotionImgPaths']
                print(readEmotionImgPaths)
                
    renderer = Renderer(readEmotionImgPaths)

    isDebug = args.debug

    coreObj = Core(input_module = input_module, renderer=renderer, output_module = output_module, debug = isDebug)
    coreObj.run()

        
