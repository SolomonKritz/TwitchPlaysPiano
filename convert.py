


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

print(convert('c'))