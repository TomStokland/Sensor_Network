#!/usr/bin/env python
"""
This module implements the Foscam IP Camera CGI command set.

I obtained information on the CGI interface from Foscam's document
entitled "MJPEG Camera CGI v1.21.pdf" from www.foscam.com

Only the functionality that interested me is implemented here.

Additional functions can be easily added by referencing the above
CGI documentation.

Ken Ramsey, 18Feb2013
"""

import urllib
import time
from threading import Thread
import sys
import xml.etree.ElementTree as ET
# from ImageEnhance import Brightness
# from tkFont import nametofont
# from idlelib.Debugger import NamespaceViewer
# from pip._vendor.requests import models
#from test.badsyntax_future3 import result

   
def dummy_videoframe_handler(frame, userdata=None):
    """test video frame handler. It assumes the userdata coming
    in is a Counter object with an increment method and a count method"""
    sys.stdout.write('Got frame %d\r' % userdata.count())
    sys.stdout.flush()
    userdata.increment()

def findFrame(parent, fp, callback=None, userdata=None):
    while parent.isPlaying():
        line = fp.readline()
        if line[:len('--ipcamera')] == '--ipcamera':
            fp.readline()
            content_length = int(fp.readline().split(':')[1].strip())
            fp.readline()
            jpeg = fp.read(content_length)
            if callback:
                callback(jpeg, userdata)

class FoscamCamera(object):

    PTZ_UP = 0
    PTZ_DOWN = 1
    PTZ_LEFT = 2
    PTZ_RIGHT = 3
    PTZ_TOP_LEFT = 4
    PTZ_TOP_RIGHT = 5
    PTZ_BOTTOM_LEFT = 6
    PTZ_BOTTOM_RIGHT = 7
    PTZ_RESET = 8
    PTZ_STOP = 9
    
    CMD_SUCCESS = 0
    CMD_STRING_FORMAT_ERROR = -1
    CMD_USR_OR_PWD_ERROR = -2
    CMD_ACCESS_DENIED = -3
    CMD_EXECUTION_FAILED = -4
    CMD_TIMEOUT = -5
    CMD_RESERVED = -6
    CMD_UNKNOWN_ERROR = -7
    CMD_RESERVED_2 = -8
    CMD_BAD_PARAMETER = -9
    
    
    def __init__(self, url='', user='', pwd=''):
        super(FoscamCamera, self).__init__()
        self._user = user
        self._pwd = pwd
        self._url = url
        self._isPlaying = 0
        
###############################################################################
#
#    Utility functions
#
###############################################################################

    def isPlaying(self):
        return self._isPlaying

    def setIsPlaying(self, val):
        self._isPlaying = val

    def setURL(self, url):
        self._url = url

    def url(self):
        return self._url
    
    def setUser(self, usr):
        self._user = usr

    def user(self):
        return self._user

    def setPassword(self, pwd):
        self._pwd = pwd

    def password(self):
        return self._pwd

    def setUserAndPassword(self, user, password):
        self.setUser(user)
        self.setPassword(password)
        
    def test_limits(self, value_to_test, low_limit=0, high_limit=100):
        if(value_to_test < low_limit):
            value_to_test = low_limit
        elif(value_to_test > high_limit):
            value_to_test = high_limit
        return value_to_test

###############################################################################
#
#    AV functions
#
###############################################################################

# getImageSetting
#TESTED WORKS
    def get_image_settings(self):
        data = self.sendCommand_return_xml('getImageSetting')
        return data
        
# setBrightness
#TESTED WORKS
    def set_brightness(self, brightness):
        brightness = self.test_limits(brightness)
        command = 'setBrightness&brightness=%s' % (str(brightness), )
        result = self.sendCommand(command, {})
        return result
    
# setContrast
# This command doesn't work. It is a foscam issue
    def set_contrast(self, contrast):
        contrast = self.test_limits(contrast)
        command = 'setContrast&contrast=%s' % (str(contrast), )
        result = self.sendCommand(command, {})
        return result
    
# setHue
#TESTED WORKS
    def set_hue(self, hue):
        hue = self.test_limits(hue)
        command = 'setHue&hue=%s' % (str(hue), )
        result = self.sendCommand(command, {})
        return result
    
# setSaturation
#TESTED WORKS
    def set_saturation(self, saturation):
        saturation = self.test_limits(saturation)
        command = 'setSaturation&saturation=%s' % (str(saturation), )
        result = self.sendCommand(command, {})
        return result
    
# setSharpness
#TESTED WORKS
    def set_sharpness(self, sharpness):
        sharpness = self.test_limits(sharpness)
        command = 'setSharpness&sharpness=%s' % (str(sharpness), )
        result = self.sendCommand(command, {})
        return result
    
# resetImageSetting
#TESTED WORKS
    def reset_image_settings(self):
        command = 'resetImageSetting'
        result = self.sendCommand(command, {})
        return result
         
# getMirrorAndFlipSetting
#TESTED WORKS
    def get_mirror_and_flip_settings(self):
        command = 'getMirrorAndFlipSetting'
        result = self.sendCommand_return_xml(command)
        return result

# mirrorVideo
#TESTED WORKS
    def set_video_mirrored(self, on):
        if(on):
            sub_command = '1'
        else:
            sub_command = '0'
        command = 'mirrorVideo&isMirror=' % (sub_command, )
        result = self.sendCommand(command, {})
        return result

# flipVideo
#TESTED WORKS
    def set_video_flipped(self, on):
        if(on):
            sub_command = '1'
        else:
            sub_command = '0'
        command = 'flipVideo&isFlip=' % (sub_command, )
        result = self.sendCommand(command, {})
        return result

# setPwrFreq
    def set_video_frequency(self, frequency):
        if(frequency == 50):
            sub_command = '1'
        elif(frequency == 60):
            sub_command = '0'
        else:
            return(1)
        command = 'setPwrFreq&freq=%s' % (sub_command, )
        result = self.sendCommand(command, {})
        return result

# getVideoStreamParam
    def get_video_stream_parameters(self):
        return_dict = dict()
        command = 'getMirrorAndFlipSetting'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
         
# setVideoStreamParam
    def set_video_stream_parameters(self, 
                                    stream_number, 
                                    resolution,
                                    bit_rate,
                                    frame_rate,
                                    gop,
                                    isvpr):
        stream_number = self.test_limits(stream_number, low_limit=0, high_limit=3)
        
        command = 'setVideoStreamParam&streamType=' +  str(stream_number) +   \
                '&resolution=' + str(resolution) +                          \
                '&bitRate=' + str(bit_rate) +                               \
                '&frameRate=' + str(frame_rate) +                           \
                '&GOP=' + str(gop) +                                       \
                '&isVBR=' + str(0)    # isvpr not implemented yet
        result = self.sendCommand(command, {})
        return result
    
# getMainVideoStreamType
    def get_main_video_stream_type(self):
        command = 'getMainVideoStreamType'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getSubVideoStreamType
    def get_sub_video_stream_type(self):
        command = 'getSubVideoStreamType'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setMainVideoStreamType
    def set_main_video_stream_type(self, stream_type):
        stream_type = self.test_limits(stream_type, low_limit=0, high_limit=3)
        command = 'setMainVideoStreamType&streamType=' + str(stream_type)
        result = self.sendCommand(command, {})
        return result

# setSubVideoStreamType
    def set_sub_video_stream_type(self, stream_type):
        if(stream_type in 'H264'):
            stream_type = '0'
        elif(stream_type in 'MotionJpeg'):
            stream_type = '1'
        command = 'setSubVideoStreamType&streamType=' + stream_type
        result = self.sendCommand(command, {})
        return result

# GetMJStream
    def get_mj_stream(self):
        command = 'getMJStream'
        result = self.sendCommand_return_binary(command)
        return result

# getOSDSetting
    def get_osd_settings(self):
        command = 'getOSDSetting'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# setOSDSetting
    def set_osd_settings(self, time_stamp_enabled, device_name_enabled, display_position, osd_mask_enabled):
        if(time_stamp_enabled in 'True'):
            time_stamp_enabled = '1'
        else:
            time_stamp_enabled = '0'
        if(device_name_enabled in 'True'):
            device_name_enabled = '1'
        else:
            device_name_enabled = '0'
        display_position = str(display_position)
        if(osd_mask_enabled in 'True'):
            osd_mask_enabled = '1'
        else:
            osd_mask_enabled = '0'
            command = 'setOSDSetting&isEnableTimeStamp=' + time_stamp_enabled + \
                '&isEnableDevName=' + device_name_enabled +                     \
                '&dispPos=' + display_position +                                \
                '&isEnableOSDMask=' + osd_mask_enabled
        result = self.sendCommand(command, {})
        return result
    
# getOsdMaskArea
    def get_osd_mask_area(self):
        command = 'getOSDMaskArea'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# setOsdMaskArea
    def set_osd_mask_area(self, x1_0, y1_0, x2_0, y2_0, x1_1, y1_1, x2_1, y2_1, x1_2, y1_2, x2_2, y2_2, x1_3, y1_3, x2_3, y2_3):
        x1_0 = str(x1_0)
        y1_0 = str(y1_0)
        x2_0 = str(x2_0)
        y2_0 = str(y2_0)
        x1_1 = str(x1_1)
        y1_1 = str(y1_1)
        x2_1 = str(x2_1)
        y2_1 = str(y2_1)
        x1_2 = str(x1_2)
        y1_2 = str(y1_2)
        x2_2 = str(x2_2)
        y2_2 = str(y2_2)
        x1_3 = str(x1_3)
        y1_3 = str(y1_3)
        x2_3 = str(x2_3)
        y2_3 = str(y2_3)
        command = 'setOsdMaskArea&x1_0=%s&y1_0=%s&x2_0=%s&y2_0=%s&x1_1=%s&y1_1=%s&x2_1=%s&y2_1=%s&x1_2=%s&y1_2=%s&x2_2=%s&y2_2=%s&x1_3=%s&y1_3=%s&x2_3=%s&y2_3=%s' \
                    % (x1_0, y1_0, x2_0, y2_0, x1_1, y1_1, x2_1, y2_1, x1_2, y1_2, x2_2, y2_2, x1_3, y1_3, x2_3, y2_3)
        result = self.sendCommand(command, {})
        return result

# getMotionDetectConfig
    def get_motion_detection_configuration(self):
        command = 'getMotionDetectConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# setMotionDetectConfig
    def set_motion_detection_configuration(self, enabled, linkage, snap_interval, sensitivity, trigger_interval, 
                                           schedule_0, 
                                           schedule_1, 
                                           schedule_2, 
                                           schedule_3, 
                                           schedule_4, 
                                           schedule_5, 
                                           schedule_6, 
                                           area_0, 
                                           area_1, 
                                           area_2, 
                                           area_3, 
                                           area_4, 
                                           area_5, 
                                           area_6, 
                                           area_7, 
                                           area_8, 
                                           area_9):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
            
        
        command = 'isEnable=%s          \
                   &linkage=%s          \
                   &snapInterval=%s     \
                   &sensitivity=%s      \
                   &triggerInterval=%s  \
                   &schedule0=%s        \
                   &schedule1=%s        \
                   &schedule2=%s        \
                   &schedule3=%s        \
                   &schedule4=%s        \
                   &schedule5=%s        \
                   &schedule6=%s        \
                   &area0=%s            \
                   &area1=%s            \
                   &area2=%s            \
                   &area3=%s            \
                   &area4=%s            \
                   &area5=%s            \
                   &area6=%s            \
                   &area7=%s            \
                   &area8=%s            \
                   &area9=1024' % (enabled, linkage, snap_interval, sensitivity, trigger_interval, 
                                   schedule_0,schedule_1, schedule_2, schedule_3, schedule_4, schedule_5, schedule_6, 
                                   area_0, area_1, area_2, area_3, area_4, area_5, area_6, area_7, area_8, area_9)
        result = self.sendCommand(command, {})
        return result

# getSnapConfig
    def get_snapshot_configuration(self):
        command = 'getSnapConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# setSnapConfig
    def set_snapshot_configuration(self, picture_quality, save_location):
        picture_quality = self.test_limits(picture_quality, 0, 2)
        save_location = self.test_limits(save_location, 0, 2)
        if(save_location == 1):
            return self.CMD_BAD_PARAMETER
        command = 'setSnapConfig&snapPicQuality=%s&saveLocation=%s' % (str(picture_quality), str(save_location))
        result = self.sendCommand(command, {})
        return result

# snapPicture
    def snap_picture(self):
        command = 'snapPicture'
        result = self.sendCommand_return_binary(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# snapPicture2
# TESTED WORKS
    def snapshot_file(self, file_name):
        data = self.sendCommand_return_binary('snapPicture2')
        open(file_name, 'wb').write(data)        
        #return f.read()                                                     
    
# getRecordList
    def get_record_list(self, record_path, start_time, end_time, record_type, start_number):
        return None # need more info for this command

# getAlarmRecordConfig
    def get_alarm_record_configuration(self):
        command  = 'getAlarmRecordConfig'
        result = self.sendCommand(command, {})
        return result

# setAlarmRecordConfig
    def set_alarm_recording_configuration(self, preview_record_enabled, preview_record_time, alarm_record_time):
        if(preview_record_enabled in 'True'):
            preview_record_enabled = '1'
        else:
            preview_record_enabled = '0'
        command = 'setAlarmRecordConfig&isEnablePreRecord=%s&preRecordSecs=%s&alarmRecordSecs=%s' % \
                    (preview_record_enabled, str(preview_record_time), str(alarm_record_time))
        result = self.sendCommand(command, {})
        return result

# setIOAlarmConfig
    def set_io_alarm_configuration(self, 
                                   enabled,
                                   linkage,
                                   alarm_level,
                                   snap_interval,
                                   trigger_interval,
                                   schedule_0,
                                   schedule_1,
                                   schedule_2,
                                   schedule_3,
                                   schedule_4,
                                   schedule_5,
                                   schedule_6
                                   ):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        linkage = self.test_limits(linkage, 0, 15)
        command = 'setIOAlarmConfig&          \
                   isEnable=%s&               \
                   linkage=%s&                \
                   snapInterval=%s&           \
                   alarmLevel=%s&             \
                   triggerInterval=%s&        \
                   schedule0=%s&              \
                   schedule1=%s&              \
                   schedule2=%s&              \
                   schedule3=%s&              \
                   schedule4=%s&              \
                   schedule5=%s&              \
                   schedule6=1024' %          \
                   (enabled, str(linkage), str(alarm_level), str(snap_interval), str(trigger_interval), \
                    str(schedule_0), str(schedule_1), str(schedule_2), \
                    str(schedule_3), str(schedule_4), str(schedule_5), str(schedule_6))
        result = self.sendCommand(command, {})
        return result

# getIOAlarmConfig
    def get_io_alarm_configuration(self):
        command = 'getIOAlarmConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
# clearIOAlarmOutput
    def clear_io_alarm_output(self):
        command = 'clearIOAlarmOutput'
        result = self.sendCommand(command, {})
        return result

# getMultiDevList
    def get_multi_device_list(self):
        command = 'getMultiDevList'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getMultiDevDetailInfo
    def get_multi_device_detailed_info(self, channel):
        command = 'getMultiDevDetailInfo&chnnl=%s' % (str(channel),)
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# addMultiDev
    def add_multiple_devices(self, channel, device_type, ip, web_port, media_port, user_name, password, device_name):
        command = 'addMultiDev&chnnl=2&productType=%s&ip=%s&port=%s&mediaPort=%s&userName=%s&passWord=%s&devName=%s' \
                    % (str(channel), str(device_type), str(ip), str(web_port), str(media_port), user_name, password, device_name)
        result = self.sendCommand(command, {})
        return result
        
# delMultiDev
    def delete_multiple_devices(self, channel):
        command = 'delMultiDev&chnnl=%s' % (str(channel),)
        result = self.sendCommand(command, {})
        return result

###############################################################################
#
#    User Account functions
#
###############################################################################
# addAccount
    def add_account(self, user_name, password, privilege):
        privilege = self.test_limits(privilege, 0, 2)
        command = 'addAccount&usrName=%s&usrPwd=%s&privilege=%s' % (user_name, password, str(privilege))
        result = self.sendCommand(command, {})
        return result

# delAccount
    def delete_account(self, user_name):
        command = 'delAccount&usrName=%s' % (user_name, )
        result = self.sendCommand(command, {})
        return result

# changePassword
    def change_password(self, user_name, old_password, new_password):
        command = 'changePassword&usrName=%s&oldPwd=%s&newPwd=%s' % (user_name, old_password, new_password)
        result = self.sendCommand(command, {})
        return result

# changeUserName
    def change_user_name(self, old_user_name, new_user_name):
        command = 'changeUserName&usrName=%s&newUsrName=%s' % (old_user_name, new_user_name)
        result = self.sendCommand(command, {})
        return result

# logIn
    def login(self, user_name, ip, group_id):
        command = 'logIn&usrName=%s&ip=%s&groupId=%s' % (user_name, ip, group_id)
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# logOut
    def logout(self, user_name, ip, group_id):
        command = 'logOut&usrName=%s&ip=%s&groupId=%s' % (user_name, ip, group_id)
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getSessionList
    def get_session_list(self):
        command = 'getSessionList'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getUserList
    def get_user_list(self):
        command = 'getUserList'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# usrBeatHeart
    def user_heartbeat(self, user_name, remote_ip, group_id):
        command = 'usrBeatHeart&usrName=%s&ip=%s&groupId=%s' % (user_name, remote_ip, group_id)
        result = self.sendCommand(command, {})
        return result

###############################################################################
#
#    PTZ Control functions
#
###############################################################################
# ptzMoveUp
# ptzMoveDown
# ptzMoveLeft
# ptzMoveRight
# ptzMoveTopLeft
# ptzMoveTopRight
# ptzMoveBottomLeft
# ptzMoveBottomRight
# ptzStopRun
# ptzReset
# TESTED WORKS
    def move(self, direction):
        direction_list = ['ptzMoveUp', 
                          'ptzMoveDown', 
                          'ptzMoveLeft',
                          'ptzMoveRight',
                          'ptzMoveTopLeft',
                          'ptzMoveTopRight',
                          'ptzMoveBottomLeft',
                          'ptzMoveBottomRight',
                          'ptzReset',
                          'ptzStopRun']
        command = direction_list[direction]
        result = self.sendCommand(command, {})
        return result

# getPTZSpeed
    def get_ptz_speed(self):
        command = 'getPTZSpeed'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setPTZSpeed
    def set_ptz_speed(self , speed):
        speed = self.test_limits(speed, 0, 4)
        command = 'setPTZSpeed&speed=%s' % (str(speed), )
        result = self.sendCommand(command, {})
        return result

# getPTZPresetPointList
    def get_ptz_preset_point_list(self):
        command = 'getPTZPresetPointList'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
    
# ptzAddPresetPoint
    def add_ptz_preset_point(self, name):
        command = 'ptzAddPresetPoint&name=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# ptzDeletePresetPoint
    def delete_ptz_preset_point(self, name):
        command = 'ptzDeletePresetPoint&name=%s' % (name, )
        result = self.sendCommand(command, {})
        return result
    
# ptzGotoPresetPoint
    def goto_ptz_preset_point(self, name):
        command = 'ptzGotoPresetPoint&name=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# ptzGetCruiseMapList
    def get_ptz_cruise_list(self):
        command = 'ptzGetCruiseMapList'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# ptzGetCruiseMapInfo
    def get_ptz_cruise_map_info(self, name):
        command = 'ptzGetCruiseMapInfo&name=%s' % (name, )
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# ptzSetCruiseMap
    def set_ptz_cruise_map(self, name, point_list):
        command = 'ptzSetCruiseMap&        \
                    name=%s&               \
                    point0=%s&             \
                    point1=%s&             \
                    point2=%s&             \
                    point3=%s&             \
                    point4=%s&             \
                    point5=%s&             \
                    point6=%s&             \
                    point7=%s' % \
                    (name, \
                     point_list[0], point_list[1], point_list[2], point_list[3], \
                     point_list[4], point_list[5], point_list[6], point_list[7], )

# ptzDelCruiseMap
    def delete_ptz_cruise_map(self, name):
        command = 'ptzDelCruiseMap&name=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# ptzStartCruise
    def start_ptz_cruise(self, name):
        command = 'ptzStartCruise&mapName=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# ptzStopCruise
    def stop_ptz_cruise(self):
        command = 'ptzStopCruise'
        result = self.sendCommand(command, {})
        return result

# zoomIn
    def zoom_in(self):
        command = 'zoomIn'
        result = self.sendCommand(command, {})
        return result

# zoomOut
    def zoom_out(self):
        command = 'zoomOut'
        result = self.sendCommand(command, {})
        return result

# zoomStop
    def zoom_stop(self):
        command = 'zoomStop'
        result = self.sendCommand(command, {})
        return result

# getZoomSpeed
    def get_zoom_speed(self):
        command = 'getZoomSpeed'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setZoomSpeed
    def set_zoom_speed(self, speed):
        speed = self.test_limits(speed, 0, 2)
        command = 'setZoomSpeed&speed=%s' % (str(speed), )
        result = self.sendCommand(command, {})
        return result

# setPTZSelfTestMode
    def set_ptz_self_test_mode(self, mode):
        mode = self.test_limits(mode, 0, 2)
        command = 'setPTZSelfTestMode&mode=%s' % (str(mode), )
        result = self.sendCommand(command, {})
        return result

# getPTZSelfTestMode
    def get_ptz_self_test_mode(self):
        command = 'getPTZSelfTestMode'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setPTZPrePointForSelfTest
    def set_ptz_self_test_preset_point(self, name):
        command = 'setPTZPrePointForSelfTest&name=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# getPTZPrePointForSelfTest
    def get_ptz_self_test_preset_point(self):
        command = 'getPTZPrePointForSelfTest'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# set485Info
    def set_rs485_info(self, protocol, address, baudrate, data_bits, stop_bits, parity):
        command = 'set485Info&          \
                   rs485Protocol=%s&    \
                   rs485Addr=%s&        \
                   rs485Baud=%s&        \
                   rs485DataBit=%s&     \
                   rs485StopBit=%s&     \
                   rs485Check=%s' %     \
                   (protocol, address, str(baudrate), str(data_bits), str(stop_bits), parity)
        result = self.sendCommand(command, {})
        return result

# get485Info
    def get_rs485_info(self):
        command = 'get485Info'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
        
###############################################################################
#
#    Network Functions
#
###############################################################################

# getIPInfo
    def get_ip_info(self):
        command = 'getIPInfo'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setIpInfo
    def set_ip_info(self, is_dhcp, ip, gate, mask, dns_1, dns_2):
        if(is_dhcp in 'True'):
            is_dhcp = '1'
        else:
            is_dhcp = '0'
        command = 'setIpInfo&        \
                   isDHCP=%s&        \
                   ip=%s&            \
                   gate=%s&          \
                   mask=%s&          \
                   dns1=%s&          \
                   dns2=%s' %        \
                   (is_dhcp, ip, gate, mask, dns_1, dns_2)
        result = self.sendCommand(command, {})
        return result

# refreshWifiList
    def refresh_wifi_list(self):
        command = 'refreshWifiList'
        result = self.sendCommand(command, {})
        return result

# getWifiList
    def get_wifi_list(self, start_number):
        command = 'getWifiList&startNo=%s' % (start_number, )
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setWifiSetting
    def set_wifi_settings(self,
                          enabled,
                          use_wifi,
                          ssid,
                          net_type,
                          encryption_type,
                          psk,
                          authentication_mode,
                          key_format,
                          default_key,
                          key_1,
                          key_2,
                          key_3,
                          key_4,
                          key_1_length,
                          key_2_length,
                          key_3_length,
                          key_4_length
                          ):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        if(use_wifi in 'True'):
            use_wifi = '1'
        else:
            use_wifi = '0'
        command = 'setWifiSetting&        \
                   isEnable=%s&           \
                   isUseWifi=%s&          \
                   ssid=%s&               \
                   netType=%s&            \
                   encryptType=%s&        \
                   psk=%s&                \
                   authMode=%s&           \
                   keyFormat=%s&          \
                   defaultKey=%s&         \
                   key1=%s&               \
                   key2=%s&               \
                   key3=%s&               \
                   key4=%s&               \
                   key1Len=%s&            \
                   key2Len=%s&            \
                   key3Len=%s&            \
                   key4Len=%s' %          \
                   (enabled, use_wifi, ssid, net_type, encryption_type, 
                    psk, authentication_mode, key_format, default_key,
                    key_1, key_2, key_3, key_4,
                    key_1_length, key_2_length, key_3_length, key_4_length)
        result = self.sendCommand(command, {})
        return result

# getWifiConfig
    def get_wifi_configuration(self):
        command = 'getWifiConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getPortInfo
    def get_port_information(self):
        command = 'getPortInfo'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setPortInfo
    def set_port_information(self, web_port, media_port, https_port):
        command = 'setPortInfo&webPort=%s&mediaPort=%s&httpsPort=%s' % (web_port, media_port, https_port)
        result = self.sendCommand(command, {})
        return result

# getUPnPConfig
    def get_upnp_configuration(self):
        command = 'getUPnPConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setUPnPConfig
    def set_upnp_configuration(self, enabled):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        command = 'setUPnPConfig&isEnable=%s'
        result = self.sendCommand(command, {})
        return result

# getDDNSConfig
    def get_ddns_configuration(self):
        command = 'getDDNSConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setDDNSConfig
    def set_ddns_configuration(self,
                               enabled,
                               host_name,
                               ddns_server,
                               user_name,
                               password):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        command = 'setDDNSConfig&isEnable=%s&hostName=%s&ddnsServer=%s&user=%s&password=%s' % \
        (enabled, host_name, ddns_server, user_name, password)
        result = self.sendCommand(command, {})
        return result

# setFtpConfig
    def set_ftp_configuration(self,
                              address,
                              port,
                              mode,
                              user_name,
                              password):
        command = 'setFtpConfig&ftpAddr=%s&ftpPort=%s&mode=%s&userName=%s&password=%s' % \
                    (address, port, mode, user_name, password)
        result = self.sendCommand(command, {})
        return result

# getFtpConfig
    def get_ftp_configuration(self):
        command = 'getFtpConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# testFtpServer
    def test_ftp_server(self,
                        address,
                        port,
                        mode,
                        user_name,
                        password):
        command = 'testFtpServer&ftpAddr=%s&ftpPort=%s&mode=%s&userName=%s&password=%s' % \
                    (address, port, mode, user_name, password)
        result = self.sendCommand(command, {})
        return result

# getSMTPConfig
    def get_smtp_configuration(self):
        command = 'getSMTPConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setSMTPConfig
    def set_smtp_configuration(self,
                               enabled,
                               server,
                               port,
                               needs_authorization,
                               tls,
                               user_name,
                               password,
                               sender,
                               receiver):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        if(needs_authorization in 'True'):
            needs_authorization = '1'
        else:
            needs_authorization = '0'
        command = 'setSMTPConfig&isEnable=%s&server=%s&port=%s&isNeedAuth=%s&user=%s&password=%s&send=%s&reciever=%s' % \
                    (enabled, server, port, needs_authorization, tls, user_name, password, sender, receiver)
        result = self.sendCommand(command, {})
        return result

# smtpTest
    def test_smtp(self,
                  server,
                  port,
                  needs_authorization,
                  tls,
                  user_name,
                  password):
        if(needs_authorization in 'True'):
            needs_authorization = '1'
        else:
            needs_authorization = '0'
        command = 'smtpTest&smtpServer=%s&port=%s&isNeedAuth=%s&user=%s&password=%s' % \
                    (server, port, needs_authorization, tls, user_name, password)
        result = self.sendCommand(command, {})
        return result

###############################################################################
#
#    Device Management Functions
#
###############################################################################

# setSystemTime
    def set_system_time(self,
                        source,
                        server,
                        date_format,
                        time_format,
                        time_zone,
                        dst_enabled,
                        dst,
                        year,
                        month,
                        day,
                        hour,
                        minute,
                        second):
        command = 'setSystemTime&        \
                   timeSource=%s&        \
                   ntpServer=%s&         \
                   dateFormat=%s&        \
                   timeFormat=%s&        \
                   timeZone=%s&          \
                   isDst=%s&             \
                   dst=%s&               \
                   year=%s&              \
                   mon=%s&               \
                   day=%s&               \
                   hour=%s&              \
                   minute=%s&            \
                   sec=%s' % \
                   (source, server, date_format, time_format, time_zone,
                    dst_enabled, dst, 
                    year, month, day,
                    hour, minute, second)
        result = self.sendCommand(command, {})
        return result

# getSystemTime
    def get_system_time(self):
        command = 'getSystemTime'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# openInfraLed
# closeInfraLed
    def set_infrared_leds(self, on):
        if(on in 'True'):
            command = 'openInfraLed'
        else:
            command = 'closeInfraLed'
        result = self.sendCommand(command, {})
        return result

# getInfraLedConfig
    def get_infrared_led_configuration(self):
        command = 'getInfraLedConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setInfraLedConfig
    def set_infrared_led_configuration(self, mode):
        if(mode in 'Auto'):
            mode = '0'
        else:
            mode = '1'
        command = 'setInfraLedConfig&mode=%s' % (mode, )
        result = self.sendCommand(command, {})
        return result

# getDevState
    def get_device_state(self):
        command = 'getDevState'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# getDevName
    def get_device_name(self):
        command = 'getDevName'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
    
# setDevName
    def set_device_name(self, name):
        command = 'setDevName&devName=%s' % (name, )
        result = self.sendCommand(command, {})
        return result

# getDevInfo
    def get_device_info(self):        
        command = 'getDevState'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

###############################################################################
#
#    System functions
#
###############################################################################

# rebootSystem
    def reboot_system(self):
        command = 'setDevName'
        result = self.sendCommand(command, {})
        return result

# restoreToFactorySetting
    def restore_to_factory_settings(self):
        command = 'restoreToFactorySetting'
        result = self.sendCommand(command, {})
        return result

# exportConfig
    def export_configuration_file(self):
        command = 'exportConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# ImportConfig
    def import_configuration_file(self, configuration_file):
        # need to do a post for this command
        command = 'importConfig'
        result = self.sendCommand(command, {})
        return result

# FwUpgrade
    def upgrade_firmware(self):
        command = 'fwUpgrade'
        result = self.sendCommand(command, {})
        return result

###############################################################################
#
#    Miscellaneous functions
#
###############################################################################

# getFirewallConfig
    def get_firewall_configuration(self):
        command = 'getFirewallConfig'
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None

# setFirewallConfig
    def set_firewall_configuration(self,
                                   enabled,
                                   rule,
                                   list_0,
                                   list_1,
                                   list_2,
                                   list_3,
                                   list_4,
                                   list_5,
                                   list_6,
                                   list_7
                                   ):
        if(enabled in 'True'):
            enabled = '1'
        else:
            enabled = '0'
        command = 'setFirewallConfig&        \
                   isEnable=%s&              \
                   rule=%s&                  \
                   ipList0=%s&               \
                   ipList1=%s&               \
                   ipList2=%s&               \
                   ipList3=%s&               \
                   ipList4=%s&               \
                   ipList5=%s&               \
                   ipList6=%s&               \
                   ipList7=%s' % \
                   (enabled, rule,
                    list_0, list_1, list_2, list_3,
                    list_4, list_5, list_6, list_7)
        result = self.sendCommand(command, {})
        return result
                   
# getLog
    def get_log(self,
                offset,
                count):
        command = 'getLog&offset=%s&count=%s' % (str(offset), str(count))
        result = self.sendCommand_return_xml(command)
        if(result != self.CMD_UNKNOWN_ERROR):
            xmldoc = ET.fromstring(result)
            return_dict = {}
            for child in xmldoc:
                return_dict[child.text] = child
            return return_dict
        else:
            return None
    
#----------------------------------------------------------------------------

    def startVideo(self, callback=None, userdata=None):
        if not self.isPlaying():
            cmds = { 'resolution':32, 'rate':0 }
            f = self.sendCommand('videostream.cgi', cmds)

            self.videothread = Thread(target=findFrame,
                                      args=(self, f, callback, userdata))
            self.setIsPlaying(1)
            self.videothread.start()

    def stopVideo(self):
        if self.isPlaying():
            self.setIsPlaying(0)
            self.videothread.join()
        



    def sendCommand(self, command, parameterDict):
        url = 'http://%s/cgi-bin/CGIProxy.fcgi?cmd=%s&usr=%s&pwd=%s' % (self.url(),
                                                                        command,
                                                                        self.user(),
                                                                        self.password())
        status = urllib.urlopen(url).read()
        return self.get_result_from_xml(status)    
    
    def sendCommand_return_binary(self, command):
        url = 'http://%s/cgi-bin/CGIProxy.fcgi?cmd=%s&usr=%s&pwd=%s' % (self.url(),
                                                                        command,
                                                                        self.user(),
                                                                        self.password())
        data = urllib.urlopen(url).read()
        return data
    
    def sendCommand_return_xml(self, command):
        url = 'http://%s/cgi-bin/CGIProxy.fcgi?cmd=%s&usr=%s&pwd=%s' % (self.url(),
                                                                        command,
                                                                        self.user(),
                                                                        self.password())
        data = urllib.urlopen(url).read()
        result = self.get_result_from_xml(data)
        if(result == self.CMD_SUCCESS):
            return data
        else:
            return self.CMD_UNKNOWN_ERROR
    
    def get_result_from_xml(self, stat):
        xmldoc = ET.fromstring(stat)
        for child in xmldoc:
            if child.tag in 'result':
                return self.CMD_SUCCESS
        return self.CMD_UNKNOWN_ERROR 


    
if __name__ == '__main__':

    TESTURL = '192.168.0.22:88'

    print
    print 'testing the Foscam camera code'
    print
    
    foscam = FoscamCamera(TESTURL, 'TBR', '7uckR8h')

    def move_a_little(fos, go, stop):
        fos.move(go)
        time.sleep(2)
        print ' - stopping move'
        fos.move(stop)
        
    print 'moving up'
    move_a_little(foscam, foscam.UP, foscam.STOP_UP)
    print 'moving down'
    move_a_little(foscam, foscam.DOWN, foscam.STOP_DOWN)
    print 'moving left'
    move_a_little(foscam, foscam.LEFT, foscam.STOP_LEFT)
    print 'moving right'
    move_a_little(foscam, foscam.RIGHT, foscam.STOP_RIGHT)

    print
    print 'taking a few snapshots'
    for i in xrange(1, 11):
        data = foscam.snapshot()
        open('snapshot-%02d.jpg' % i, 'wb').write(data)
        sys.stdout.write('wrote snapshot %d\r' % i)
        sys.stdout.flush()

    print

    class Counter(object):
        def __init__(self):
            super(Counter,self).__init__()
            self._count = 0
        def increment(self):
            self._count += 1
        def count(self):
            return self._count

    print       
    print 'playing a little video (30 seconds worth)'
    counter = Counter()
    foscam.startVideo(dummy_videoframe_handler, counter)
    time.sleep(30)
    print
    print 'stopping video'
    foscam.stopVideo()
    print

    nframes = counter.count() - 1

    print
    print nframes, 'frames in ~30 secs for ~', nframes/30.0, 'fps'
    print
    print 'done!'
    
    
