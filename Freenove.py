from datetime import datetime
from lib2to3.pgen2.token import STRING
import math
from re import S
from telegraphbot import BOT
import requests
from anything import Anything
import time

s=BOT("FREENOVE",TOKEN)

def on(message):
    page=requests.get('http://192.168.1.3/on')
    s._bot.send_message(message.chat.id, "Alarm ON")
    s.soft_reset()

def off(message):
    page=requests.get('http://192.168.1.3/off')
    s._bot.send_message(message.chat.id, "Alarm OFF")
    s.soft_reset()

def stop(message):
    page=requests.get('http://192.168.1.3/stop')
    s._bot.send_message(message.chat.id, "Stop")
    time.sleep(4)
    s._bot.send_message(message.chat.id, "Pause finished")
    s.soft_reset()

# Bots-only commands

def settings(message):
    s._bot.send_message(message.chat.id, "Change control mode or control duration?")
    s.soft_reset()

def control_1(message):
    s._bot.send_message(message.chat.id, "Survelling...")
    start=time.time()
    while(time.time()-start<3600*HOUR_LOG+60*MIN_LOG+SEC_LOG):
        page=requests.get('http://192.168.1.3/log')
        time.sleep(0.28)
        string=page.content.decode("utf-8") # 0 if the alarm is off, 1023 otherwise
        if string[0]!="0":
            s._bot.send_message(message.chat.id, "Alarm ON")
            break
        time.sleep(2)
    s._bot.send_message(message.chat.id, "Survellance has stopped")
    s.soft_reset()

def control_2(message):
    s._bot.send_message(message.chat.id, "Survelling...")
    start=time.time()
    time.sleep(0.2)
    while(time.time()-start<3600*HOUR_LOG+60*MIN_LOG+SEC_LOG):
        page=requests.get('http://192.168.1.3/log')
        time.sleep(0.28)
        string=page.content.decode("utf-8")
        #print(string)
        if string[0]!="0":
            s._bot.send_message(message.chat.id, "Detection")
            requests.get('http://192.168.1.3/stop')
            time.sleep(3.8)
    s._bot.send_message(message.chat.id, "Survellance has stopped")
    s.soft_reset()

def control_change(message):
    global control
    if control==control_1:
        control=control_2
        s._bot.send_message(message.chat.id, "Control mode successfully changed to control_2")
    else:
        control=control_1
        s._bot.send_message(message.chat.id, "Control mode successfully changed to control_1")
    s.soft_reset()

"""
The "CHECK" command set your alarm to the *surveillance mode* and will notify you by a message when the alarm is ringing.
There are two surveillance mode: control_1 and control_2.
Control_1 will notify you the first time the alarm goes off and then it exit the control mode leaving the alarm ringing.
Control_2 will notify every time the alarm goes off, and when it does the *stop* command will be called and after the pause
 is finished the bot is ready to send you another notification the next time the alarm rings without exiting the surveillance mode.
Control_2 mode is the default.
"""

def duration_change(message):
    global MIN_LOG
    MIN_LOG=int(message.text)
    if MIN_LOG>59:
        s._bot.send_message(message.chat.id, "Control duration successfully changed to "+str(MIN_LOG//60)+" hours "+str(MIN_LOG%60)+" minutes")
    else:
        s._bot.send_message(message.chat.id, "Control duration successfully changed to "+str(MIN_LOG)+" minutes")
    s.soft_reset()

"""
Surveillance mode lasts 30 minutes by default.
"""

lz=s.lazy

control=control_2

HOUR_LOG=0
MIN_LOG=30
SEC_LOG=0

def step0(message):
    s.chat_step(0,message,None,['ON', 'OFF','STOP','CHECK','SETTINGS'],[on,off,stop,control,lz],s.unrecognized,[None,None,None,None,step1])

def step1(message):
    s.chat_step(1,message,"Change control mode or control duration?",['MODE','DURATION'],[control_change,lz],s.unrecognized,[None,step2])

def step2(message):
    s.chat_step(2,message,"Set new duration in minutes",[r'^([\s\d]+)$'],[duration_change],s.unrecognized,[])


s.steps=[step0,step1,step2]

s.presentation="_-_-_-_//FREENOVE_BOT\\\_-_-_-_"
s.start_markup=('ON', 'OFF','STOP','CHECK','/start',"SETTINGS","DURATION","MODE")
s.init_message="_-_-_-_-_-_//Here I am !\\\_-_-_-_-_-_"

while True:
    try:
        s.polling()
    except requests.exceptions.ConnectionError:
        Current_time=str(datetime.now())[5:-6]
        print("ESP Lost",Current_time)
        try:
            s._bot.send_message(s.id, "Cannot connect to ESP")
        except:
            print("Further error")
    except:
        Current_time=str(datetime.now())[5:-6]
        print("Lost connection at ",Current_time)
        time.sleep(10)