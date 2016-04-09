# TwitchPlaysPiano

Source code for the TwitchPlaysAPiano bot. See twitch.tv/twitchplaysapiano and visit our setup to see the code in action!

##Overview
Twitch Plays Piano lets you control a piano with a lot of other people by typing commands into the TwitchPlaysAPiano Twitch chat located at https://www.twitch.tv/twitchplaysapiano . Work with others to try and build a song!

This is achieved with a Python script that reads chat messages as they happen live via an IRC connection to the Twitch chat. It then feeds into a Java program that outputs MIDI signals to a real keyboard.

Note that this currently only works locally with a real keyboard, and has only been tested with a Casio-brand keyboard.

##Usage (in Twitch chat)
###Playing Notes
* There are seven musical notes: C, D, E, F, G, A, and B. Each note also has a "sharp" variant ♯.
* To play the musical tone C, just type **lowercase**  **"c".**
* To play the musical tone C♯, type **uppercase** **"C"**
* To play the musical tone C one octave up, type **"c1"**.
* To play the musical tone C one octave down, type **"c-1"**.
* To play C for 0.5x the default time, type **"c;.5"**.
* To play C for 2x the default time. type **"c;2"**.
* To play C♯ two octaves down for 0.75x the usual time, type **"C-2;0.75"**.

###Other Commands
* To change the volume to 100, type **"!vol 100"**. The allowed range is between 0 and 127.
* To double the default time a note is played, type **"!beat 2"**. There is an upper limit on this command to prevent excessively long notes from being played.

##Credits and Thanks:
###Authors:
Vincent Choo  
SaiArvind Ganganapalle  
Eric Goren  
David Liang  
Solomon Kritz

###Special Thanks:
BitCamp  
The University of Maryland  
MLH 
All the mentors!  
