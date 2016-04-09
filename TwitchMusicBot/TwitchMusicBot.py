import socket
import string
import os
import random
import traceback
import sys
import time

def send_message(irc, channel, message):
    irc.send("PRIVMSG {0} :{1}\r\n".format(channel, message).encode("utf-8"))
    print("Message Sent: " + message)

def connect_to_channel(channel_name, music_file):
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
    # send_message(s, IRC_CHANNEL, 'Piano bot has arrived to serenade your heart && soul')
    line_number = 0
    music_name = 0
    beat_length = 1
    with open(music_file) as music:
        for line in music:
            line_number += 1
            if line_number == 1:
                music_name = line
                continue
            elif line_number == 2:
                beat_length = float(line)
                # send_message(s, IRC_CHANNEL, 'I shall now play ' + music_name)
                # time.sleep(7)

                continue
            for note in line.split(" "):
                print(note)
                send_message(s, IRC_CHANNEL, note)
                note_length = 1
                if ';' in note:
                    note_length = float(note.split(';')[1])
                time.sleep(beat_length * note_length * 1.4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' <music file> [beat_length]')
        exit(0)
    channel_name = "twitchplaysapiano"
    connect_to_channel(channel_name, sys.argv[1])
