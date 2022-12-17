# Convert hexadecimal data into a string (code ASCII)
def hex_to_ascii(data, n=1):
    """Returns ASCII string of more than n cnosecutive printable characters from data"""
    s = ""
    temp_s = ""
    for i in range(0, len(data), 2):
        if data[i:i+2].isprintable():
            temp_s += chr(int(data[i:i+2], 16))
        else:
            if len(temp_s) >= n:
                s += temp_s
            temp_s = ""
    if len(temp_s) >= n:
        s += temp_s
    return s

# Convert a string into hexadecimal
def ascii_to_hex(str):
    """Returns hex code from ascii string"""
    return str.encode("ascii").hex()

resHex = ascii_to_hex("EDUROAM")
resASCII = hex_to_ascii("C0B00C1502111079")

print(resHex)
print(resASCII)