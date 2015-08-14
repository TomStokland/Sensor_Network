'''
Created on Jul 24, 2015

@author: Tom Stokland
'''
#import sys
import foscam
#import Image
#from StringIO import StringIO
import time

ImageReadyEventId = 1382
direction = 0
devcam = None
CAM_URL = '192.168.0.22:88'
CAM_USR = 'TBR'
CAM_PWD = '7uckR8h'
CameraError = 0

def main():
    global devcam
    devcam = foscam.FoscamCamera(CAM_URL, CAM_USR, CAM_PWD)
    try:
#         devcam.set_video_frequency(1)
#         devcam.set_video_frequency(0)
        picture = devcam.snap_picture()
        
        status = devcam.move(devcam.PTZ_BOTTOM_LEFT)
        if(status != 0):
            raise CameraError
        time.sleep(1)
        status = devcam.move(devcam.PTZ_STOP)
        if(status != 0):
            raise CameraError
        time.sleep(1)
        status = devcam.move(devcam.PTZ_RESET)
        if(status != 0):
            raise CameraError
        pass
    except CameraError:
        pass

def playVideo():
    pass#devcam.startVideo(videoCallback)

def stopVideo():
    devcam.stopVideo()
        


if __name__ == '__main__':
    main()
    