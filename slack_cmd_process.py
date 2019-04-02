import os
from picamera import PiCamera
from time import sleep
import requests


def cmd_process(command):
    """
      Decide the command which is to be run based on user message directed
      at bot.
    """

    if "click pic" in command:
       click_picture()


def click_picture():
    """
      execute the command on the provided host in the message and return message
      based of successfull or unsuccessful cmd execution.

    """
    try:
           camera = PiCamera()
           camera.start_preview(rotation = 180)
           camera.rotation = 180
           sleep(5)
           camera.capture('/tmp/picture.jpg')
           camera.stop_preview()
    finally:
           camera.close()

    token = os.environ.get('SLACK_BOT_TOKEN')
    upload_pic(token)

def upload_pic(token):
           
    my_file = {
                 'file' : ('/tmp/picture.jpg', open('/tmp/picture.jpg', 'rb'), 'jpg')
              }

    payload={
                 "filename":"picture.jpg",
                 "token": "{0}".format(token),
                 "channels":['#testcambot'],
             }

    r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
