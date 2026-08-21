import argparse
import json
import os
from src.run import run
from src.config import ConfigInfo, writeConfigInfo

config_path = './config.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_type', default='w')
    parser.add_argument('-i', '--input_type', default='w')
    parser.add_argument('-ci', '--webcam_idx', default='1')
    parser.add_argument('-wh', '--obs_webserver_host', default='localhost')
    parser.add_argument('-wpr', '--obs_webserver_port', default=4455)
    parser.add_argument('-wpw', '--obs_webserver_password', default='')
    parser.add_argument('-p', '--webserver_port', default=5000)
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    parser.add_argument('-c', '--config_file', default='')
    args = parser.parse_args()
    print('args:', args)
    output_type = args.output_type
    input_type = args.input_type

    if args.config_file != '':
        config_info = readConfigInfo(args.config_file)
    else:
        config_info = ConfigInfo()
        config_info.setOutputType(args.output_type)
        config_info.setInputType(args.input_type)
        config_info.setWebcamIdx(args.webcam_idx)
        config_info.setWebserverPort(args.webserver_port)
        config_info.setOBSHost(args.obs_webserver_host)
        config_info.setOBSPW(args.obs_webserver_password)
        config_info.setIsDebug(args.debug)

        writeConfigInfo(config_info, 'config.json')

    run(config_info)
