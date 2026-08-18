import obsws_python as obs
import time

cl = obs.ReqClient(host='localhost', port=4455)

currentScene = cl.send('GetCurrentProgramScene', raw=True)
print('Current Scene: ', currentScene)

cl.send('CreateInput', data = {
    'sceneName': 'myScene',
    'inputName': 'My New Image Source2',
    'inputKind': 'image_source',
    'inputSettings': {
        'file':'/Users/andrewsoncha/expressionTool/testImgs/happy_square.png' 
    }
})

inputList = cl.send('GetInputList', data = {'inputKind': 'image_source'}, raw=True)
print('Input List: ', inputList)

time.sleep(5)

cl.send('SetInputSettings', data = {
    'sceneName': 'myScene',
    'inputName': 'My New Image Source2',
    'inputSettings': {
        'file':'/Users/andrewsoncha/expressionTool/testImgs/neutral_square.png' 
    }
})
