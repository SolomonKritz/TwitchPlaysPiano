import socket
import string
import os
import random
import traceback
import sys
import time
import math

jarPath = "C:\\Users\\Solomon Kritz\\Documents\\TwitchPlaysPiano\\Midi.jar"

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
        if (beat is ""):
            beat = "1"
            beat = int(beat)
        elif (beat is "one"):
            beat = "1"
            beat = int(beat)
        else:
           div = len(beat)
           beat = int(beat)
           beat = beat / 1.0
           beat = beat / pow(10, div)
        if (note is not ""):
           num = convert(note)
           beat = (beatLen*1000*beat)
           if ("." in str(beat)):
               beat = str(beat).split(".")[0]
           print("Note: " + note + " Beat: " + str(beat) + " Num: " + str(num))
           os.system('java -jar "' + jarPath + '" "CASIO USB-MIDI" ' + str(num) + ' 127 ' + str(beat))

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
    channel_name = input("Enter a channel name: ")
    beatLen = input("Enter the length of a whole beat (in secs): ")
    connect_to_channel(channel_name, beatLen)
