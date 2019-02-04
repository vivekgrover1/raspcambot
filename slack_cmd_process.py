import os
from picamera import PiCamera
from time import sleep
import requests


help="""Use below commands to get the system information.\n\ncommand apache status host <hostname> - to get the apache status.\n
command free host <hostname> - to get the amount of used and free memory in the system.\n
command last log host <hostname>- to get the last ten line of log file /var/file/messages.\n
command uptime host <hostname> - to get the time how long the system has been running and load average.\n
command list cpu host <hostname> - to get the information about CPU architecture."""

#camera = PiCamera()


def cmd_process(command):
    """
      Decide the command which is to be run based on user message directed
      at bot.
    """
    lis=command.split(" ")
   # print lis
    if lis[0].startswith("take"):
       # return "I am doing good, How about you?","good"
       try:
           camera = PiCamera()
           camera.start_preview(rotation = 180)
           camera.rotation = 180
           sleep(5)
           camera.capture('/tmp/picture.jpg')
           camera.stop_preview()
       finally:
           camera.close()
       my_file = {
                 'file' : ('/tmp/picture.jpg', open('/tmp/picture.jpg', 'rb'), 'jpg')
                 }

       payload={
                 "filename":"picture.jpg",
                 "token": "",
                 "channels":['#testcambot'],
                     }

       r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    if lis[0]=="help" and len(lis)==1:
        return help, "good"
    if lis[0]=="command" and len(lis)>=3:
        if lis[1]=="apache" and lis[2]=="status" and lis[3]=="host":
           return cmd_exec("systemctl status httpd",lis[4],"apache_status")
        if lis[1]=="free" and lis[2]=="host":
            return cmd_exec("free -m",lis[3],"free")
        if lis[1]=="last" and lis[2]=="log" and lis[3]=="host":
            return cmd_exec("sudo tail -10 /var/log/messages",lis[4],"last_10_lines_log")
        if lis[1]=="uptime" and lis[2]=="host":
              return cmd_exec("uptime",lis[3],"uptime")
        if lis[1]=="list" and lis[2]=="cpu" and lis[3]=="host":
            return cmd_exec("lscpu",lis[4],"lscpu")
        if lis[1]=="search" and lis[3]=="host":
            return cmd_exec("sudo grep %s /var/log/messages | head " %lis[2],lis[4],"search_log")
        if lis[1]=="process" and lis[3]=="host":
            return cmd_exec("sudo ps -ef | grep %s " %lis[2],lis[4],"search_process")

    return "Not sure what you mean, please use help.","danger"

