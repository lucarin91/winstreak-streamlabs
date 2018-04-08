# -*- coding: utf-8 -*-
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import io
import json
from os.path import isfile
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "WinStrike"
Website = ""
Description = "Manage the Win Strike on OBS"
Creator = "lucarin91"
Version = "0.0.1"

#---------------------------------------
# Set Variables
#---------------------------------------
_command_permission = "moderator"
_command_info = ""
_command = "!strike"
_message = "win: {} loss: {}"
_strike_path = 'Services/Twitch/Files/WinStrike.txt'
_win = 0
_loss = 0

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    settings = 'Services/Scripts/{}/settings.json'.format(ScriptName)
    if isfile(settings):
        with io.open(settings, mode='r', encoding='utf-8-sig') as f:
            string = f.read()
            Parent.Log(ScriptName, 'Load json: {}'.format(string))
            conf = json.loads(string)
            parse_conf(conf)

    if not isfile(_strike_path):
        write_strike()

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    global _win, _loss
    if data.IsChatMessage():
        if data.GetParam(0).lower() == _command\
           and data.GetParamCount() == 2\
           and Parent.HasPermission(data.User, _command_permission, _command_info):
            if data.GetParam(1).startswith('+'):
                # new win
                _win += 1 if data.GetParam(1) == '+' else int(data.GetParam(1)[1:])
            elif data.GetParam(1).startswith('-'):
                # new lose
                _loss += 1 if data.GetParam(1) == '-' else int(data.GetParam(1)[1:])
            elif data.GetParam(1) == 'reset':
                _win = 0
                _loss = 0
            else:
                return
            write_strike()

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    pass

def Unload():
    pass
    
def ReloadSettings(jsonData):
    parse_conf(json.loads(jsonData))

#---------------------------------------
# My functions
#---------------------------------------
def write_strike():
    with io.open(_strike_path, mode='w', encoding='utf-8-sig') as f:
        f.write(_message.format(_win, _loss))
    Parent.Log(ScriptName, 'Update win strike (file:{})'.format(_strike_path))
    

def parse_conf(conf):
    """Set the configuration variable."""
    global _message, _command
    _message = conf['message']
    _command = conf['command']
    Parent.Log(ScriptName, 'Load conf: {}'.format((_message, _command)))
    