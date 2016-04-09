import math
# Created on Apr 9, 2016

# @author: W
# '''

def logistic(x, x0, L, k):
    return L / (1 + math.exp(-k * (x - x0)))

def pitchScale(string):
    if len(string) == 0:
        keyMod = -55
    else:
        string = string[:1]
        scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+qQwWeErRtTyYuUiIoOpP"
        scale += "aAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM [{]}\\|;:'\",<.>/?"

        keyMod = scale.find(str)
        keyMod = (keyMod == -1 if 96 else keyMod) - 54
        
    # 72 is middle C
    return 72 + keyMod

def pitchSemi(string):
    if len(str) == 0:
        keyMod = -48
    else:
        string = string[:1]
        scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+ [{]}\\|;:'\",<.>/?"
        scale += "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
        
        keyMod = scale.find(string)
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
        
def pitchSmart(string):
    scale = "`~1!2@3#4$5%6^7&8*9(0)-_=+ [{]}\\|;:'\",<.>/?"
    scale += "abcdefghijklmnopqrstuvwxyz"
    
    note = 0
    if len(str) > 0:
        tmp = string[:1].lower()
        note = scale.find(tmp) - 43
    
    sharp = 0
    if len(string) > 1:
        tmp = string[1:2]
        sharp = tmp == "#" if 1 else (tmp == "b" if -1 else 0)
    
    return 69 + note + sharp

def volume(string):
    strLen = len(string)
    text = string.replace("[\s]", "")
    
    textLen = len(text)
    capLen = len(string.replace("[^[A-Z]]", ""))
    swearingLen = len(string.replace("[^[!@#$%^&*]]" , ""))
    
    x0 = 0
    L = 127
    k = 0.5
    
    x = (8 * textLen) / (strLen * k)
    x = x * (0.75 * capLen + 0.15 * swearingLen + 0.10 * textLen)
    return logistic(x, x0, L, k) - (.45 * L)

def noteLength(string):
    string = string.strip()
    
    x0 = 0
    L = 1
    k = 0.5
    x = 8 * len(str) / k
    
    return logistic(x, x0, L, k) - (.45 * L)
