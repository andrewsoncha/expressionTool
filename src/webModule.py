import cv2
import base64
import numpy as np
from src.outputModule import outputModule

from flask import Flask, render_template, jsonify, make_response, request

from multiprocessing import Process
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

app = Flask(__name__)

global avatar_img_base64
global tab_name

tab_name = 'expressToolOutput'
avatar_img_base64 = ''

def startServer(port):
    print('INFO webOutputModule.py:  app.run(port={})'.format(port))
    app.run(host='127.0.0.1', port=port)

class webOutputModule(outputModule):
    def __init__(self, tabName:str = 'expressToolOutput', port:int = 5000):
        self.tabName = tabName
        self.port = port
        global avatar_img_base64
        global tab_name
        tab_name = self.tabName
        avatar_img_base64 = ''
        p = Process(target = startServer, args=(port, ))
        p.start()

    def outputImg(self, img: np.ndarray) -> int:
        if img is None:
            print('windowModule.show: the image is None!')
            return -1
        if img.shape == ():
            print('windowModule.show: the image is empty!')
            return -1
        success, encodedImg = cv2.imencode('.jpg', img)
        if success:
            base64_bytes = base64.b64encode(encodedImg)
            global avatar_img_base64
            avatar_img_base64 = 'data:image/jpeg;base64,' + base64_bytes.decode('utf-8')
            request_obj = {'img': avatar_img_base64}
            request_url = 'http://127.0.0.1:'+self.port+'/changeImg'
            try:
                requests.post(request_url, json=request_obj, timeout=1)
            except Timeout:
                print('INFO webOutputModule.py: Timeout error! The Flask server is probably not set up yet. If you still get this error after 10 seconds, something is wrong.')
            except ConnectionRefusedError:
                print('INFO webOutputModule.py ConnectionRefusedError! The Flask server is probably not set up yet. If you still get this error after 10 seconds, something is wrong.')
            except RequestException:
                print('INFO webOutputModule.py RequestException! The Flask server is probably not set up yet. If you still get this error after 10 seconds, something is wrong.')
        return 0


# Endpoint to get the main webpage.
@app.route('/', methods=['GET'])
def sendPage():
    global tab_name
    return render_template('index.html', title=tab_name)

# Endpoint to get the avatar image. Only hit by the webpage. Polled every 100 ms (~ish)
@app.route('/avatarImg', methods=['GET'])
def sendImg():
    global avatar_img_base64
    return make_response(jsonify(avatar_img_base64), 200)

# Endpoint to change the displayed avatar image. Only hit by the expressionTools python script.
@app.route('/changeImg', methods=['POST'])
def changeImg():
    global avatar_img_base64
    request_json = request.get_json()
    request_img = request_json['img']
    if request_img is not None and request_img != '':
        avatar_img_base64 = request_img
        return ("Avatar Image Changed Succesfully", 201)
    else:
        return ("Something is wrong with the base64 image string provided", 400)


