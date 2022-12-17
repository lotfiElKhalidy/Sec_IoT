#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      loelkhalid
#
# Created:     07/10/2022
# Copyright:   (c) loelkhalid 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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

def conversionFichier(fichier):
    file = open(fichier, "r")
    lines = file.readlines()
    file.close()

    file2 = open("fichierConvert.txt", "w")

    for line in lines:
        line = line [9:-2]
        file2.write(hex_to_ascii(line))
        #print(hex_to_ascii(line))
    file2.close()


#resASCII = hex_to_ascii("454455524f414d")
#print(resASCII)

conversionFichier("fichierBase.txt")