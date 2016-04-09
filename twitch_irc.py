import socket
import string
import os
import random
import traceback
import sys
import time
import math

jarPath = os.getcwd() + "\\Midi.jar"

def logistic(x, x0, L, k):
    return L / (1 + math.exp(-k * (x - x0)))

def pitchScale(str):
    if len(str) == 0:
        keyMod = -55
    else:
        str = str[:1]
        scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+qQwWeErRtTyYuUiIoOpP"
        scale += "aAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM [{]}\\|;:'\",<.>/?"

        keyMod = scale.find(str)
        keyMod = (keyMod == -1 if 96 else keyMod) - 54
        
    # 72 is middle C
    return 72 + keyMod

def pitchSemi(str):
    if len(str) == 0:
        keyMod = -48
    else:
        str = str[:1]
        scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+ [{]}\\|;:'\",<.>/?"
        scale += "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
        
        keyMod = scale.find(str)
        keyMod = keyMod == -1 if 96 else keyMod
        
        note = (keyMod + 13) % 14
        if note >= 10:
            note -= 2
        elif note >= 4:
            note -= 1
        
        octave = math.floor((keyMod - 43) / 14.0)
        keyMod = 12 * octave + note
        
     # 69 is middle A
    return 69 + keyMod
        
def pitchSmart(str):
    scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+ [{]}\\|;:'\",<.>/?"
    scale += "abcdefghijklmnopqrstuvwxyz"
    
    note = 0
    if len(str) > 0:
        tmp = str[:1].lower()
        note = scale.find(tmp) - 43
    
    sharp = 0
    if len(str) > 1:
        tmp = str[1:2]
        sharp = tmp == "#" if 1 else (tmp == "b" if -1 else 0)
    
    return 69 + note + sharp

def volume(str):
    strLen = len(str)
    text = str.replace("[\s]", "")
    
    textLen = len(text)
    capLen = len(str.replace("[^[A-Z]]", ""))
    swearingLen = len(str.replace("[^[!@#$%^&*]]" , ""))
    
    x0 = 0
    L = 127
    k = 0.5
    
    x = (8 * textLen) / (strLen * k)
    x = x * (0.75 * capLen + 0.15 * swearingLen + 0.10 * textLen)
    return logistic(x, x0, L, k) - (.45 * L)

def noteLength(str):
    str = str.strip()
    
    x0 = 0
    L = 1
    k = 0.5
    x = 8 * len(str) / k
    
    return logistic(x, x0, L, k) - (.45 * L)

def connect_to_channel(channel_name, beatLen):
    #CONFIG
    CHANNEL_NAME = channel_name
    CHANNEL_NAME = CHANNEL_NAME.lower()
    IRC_CHANNEL = "#"+CHANNEL_NAME
    PASS = "oauth:8csfankwunv7j4a054n4ju9jglubel"

    host = "irc.twitch.tv"
    port = 6667  
    nick = "ardvarks96"
    s = socket.socket()
    s.connect((host,port))
    s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(nick).encode("utf-8"))
    s.send("JOIN {}\r\n".format(IRC_CHANNEL).encode("utf-8"))

    vol = 127
    beatLen = float(beatLen)
    i = 1
    
    for i in range(3):
        response = s.recv(1024).decode("utf-8")
        
    while True:
        beat = "";
        note = ""
        mode = 0
        response = s.recv(1024).decode("utf-8")
        print(response)
        note = response.split(":")[2]
        response = note
        note = ""
        if (("!" in response) and (" "  in response)):
           if (response.split(" ")[0] == "!beat"):
              try:
                 beatLen = float(response.split(" ")[1])
                 if (beatLen > 4):
                     beatLen = 4
                 continue
              except:
                 pass
        if (("!" in response) and (" "  in response)):
           if (response.split(" ")[0] == "!vol"):
              try:
                 vol = int(response.split(" ")[1])
                 if (vol > 127):
                     vol = 127
                 if (vol < 0):
                     vol = 0
                 continue
              except:
                 pass
        for char in response:
           if ((((ord(char) >= 65) and (ord(char) <= 71)) or ((ord(char) >= 97) and (ord(char) <= 103))) and (mode == 0)):
              note = char
              mode = 1
           elif ((mode == 1) and (ord(char) >= 49) and (ord(char) <= 51)):
              note = note + ',' + char
              mode = 3
           elif ((mode == 1) and (ord(char) == 45)):
              note = note + ',' + char
              mode = 2
           elif ((mode == 2) and (ord(char) >= 49) and (ord(char) <= 51)):
              note = note + char
              mode = 3
           elif ((mode == 3 or (mode == 1)) and (ord(char) == 59)):
              mode = 4
           elif ((mode == 4) and (ord(char) == 49)):
              beat = beat + "one"
              break
           elif ((mode == 4) and (ord(char) == 46)):
              mode = 5
           elif ((mode == 5) and (ord(char) >= 48) and (ord(char) <= 57)):
              beat = beat + char
              mode = 6
           elif ((mode == 6) and (ord(char) >= 48) and (ord(char) <= 57)):
              beat = beat + char
              break
           elif (mode == 1):
              break        
        if (len(note) == 3):
            note = note.replace(",-", "")
        if (beat == ""):
            beat = "1"
            beat = int(beat)
        elif (beat == "one"):
            beat = "1"
            beat = int(beat)
        else:
           div = len(beat)
           beat = int(beat)
           beat = beat / 1.0
           beat = beat / pow(10, div)
        if (note != ""):
           num = convert(note)
           beat = (beatLen*1000*beat)
           if ("." in str(beat)):
               beat = str(beat).split(".")[0]
           print("Note: " + note + " Beat: " + str(beat) + " Num: " + str(num))
           os.system('java -jar "' + jarPath + '" "CASIO USB-MIDI" ' + str(num) + ' ' + str(vol) + ' ' + str(beat))

def play_note(num, vol, beat):
	os.system('java -jar "' + jarPath + '" "CASIO USB-MIDI" ' + str(num) + ' ' + str(vol) + ' ' + str(beat))
	
def convert(string):
    parts = string.split(",")
    octave = 0
    if len(parts) >= 2:
        octave = int(parts[1])
    sharp = (1 if parts[0].isupper() else 0)
    key = 0
    key_lower = parts[0].lower()
    if key_lower == 'a':
        key = -3
    elif key_lower == 'b':
        key = -1
    elif key_lower == 'c':
        key = 0
    elif key_lower == 'd':
        key = 2
    elif key_lower == 'e':
        key = 4
    elif key_lower == 'f':
        key = 5
    elif key_lower == 'g':
        key = 7
    return 72 + key + 12 * octave + sharp

if __name__ == "__main__":
    threads = [];
    channel_name = input("Enter a channel name: ")
    beatLen = input("Enter the length of a whole beat (in secs): ")
    connect_to_channel(channel_name, beatLen)
