# -*- coding: utf-8 -*-
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import io
import json
import re
from os.path import isfile
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "WinStreak"
Website = "https://github.com/lucarin91/winstreak-streamlabs"
Description = "Manage the host win streak on OBS"
Creator = "lucarin91"
Version = "2.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
Command = "!streak"
Message = "win: {} loss: {}"
_command_permission = "moderator"
_command_info = ""
_streak_path = 'Services/Twitch/Files/WinStreak.txt'
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

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    global _win, _loss
    if data.IsChatMessage() or data.IsWhisper():
        if data.GetParam(0).lower() == Command\
           and data.GetParamCount() > 1\
           and data.GetParamCount() < 4\
           and Parent.HasPermission(data.User, _command_permission, _command_info):
            # TODO: test all the parsing
            # parameter parsing
            param = data.GetParam(1)
            if param == '+':
                _win += 1
                Parent.Log(ScriptName, 'add a win')
            elif param == '-':
                _loss += 1
                Parent.Log(ScriptName, 'add a loss')
            elif param == 'reset':
                _win, _loss = 0, 0
                Parent.Log(ScriptName, 'reset win and loss')
            else:
                # for each parameter
                for i in range(1, data.GetParamCount()):
                    param = data.GetParam(i)
                    # parse parameter with numebers
                    params = re.findall(r'(\+|-)([0-9]*)$', param)
                    
                    # parameter error
                    if not params:
                        Parent.Log(ScriptName, 'unknown parameters')
                        return
                    
                    # use parameters to set win or loss
                    sign, num = params[0][0], int(params[0][1])
                    if sign == '+':
                        _win = num
                        Parent.Log(ScriptName, 'set win to {}'.format(num))
                    elif sign == '-':
                        _loss = num
                        Parent.Log(ScriptName, 'set loss to {}'.format(num))
            write_streak()

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
def write_streak():
    """Write the win and the loss on the file"""
    with io.open(_streak_path, mode='w', encoding='utf-8-sig') as f:
        f.write(Message.format(_win, _loss))
    Parent.Log(ScriptName, 'Update win streak (file:{})'.format(_streak_path))


def parse_conf(conf):
    """Set the configuration variable."""
    global Message, Command
    Message = conf['message']
    Command = conf['command']
    write_streak()
    Parent.Log(ScriptName, 'Load conf: {}'.format((Message, Command)))
    