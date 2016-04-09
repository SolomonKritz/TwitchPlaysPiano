import socket
import string
import os
import random
import traceback
import sys
#import sleep

def connect_to_channel(channel_name):
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

    while True:
        note = ""
        response = s.recv(1024).decode("utf-8")    
        mode = 0
        note = response.split(":")[2]
        response = note
        note = ""
        for char in response:
           if ((((ord(char) >= 65) and (ord(char) <= 71)) or ((ord(char) >= 97) and (ord(char) <= 103))) and (mode == 0)):
              note = char
              mode = 1
           elif ((mode == 1) and (ord(char) >= 49) and (ord(char) <= 51)):
              note = note + char
              break
           elif ((mode == 1) and (ord(char) == 45)):
              note = note + char
              mode = 2
           elif ((mode == 2) and (ord(char) >= 49) and (ord(char) <= 51)):
              note = note + char
              break
           elif ((mode == 1) or (mode == 2)):
              note = note.replace("-", "")
              break
        if (note is not ""):
           print(note)
        #sleep(0.1)

if __name__ == "__main__":
    channel_name = input("Enter a channel name: ")
    connect_to_channel(channel_name)
