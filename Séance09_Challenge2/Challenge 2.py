# -*- coding: utf-8 -*-
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def EncodeXor(tabMessage,tabKey):
    """ Chiffrement Ou exclusif."""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ tabKey contient la clef sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    res = bytearray(len(tabMessage))
    i = 0
    j = 0
    for k in range(len(tabMessage)):
        res[j] = tabMessage[k] ^ tabKey[i]
        i = (i + 1) % len(tabKey)
        j += 1
    return res

def DecodeXor(tabMessage,tabKey):
    """ Chiffrement Ou exclusif."""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ tabKey contient la clef sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    return EncodeXor(tabMessage, tabKey)

def Indice(table, element):
    """ Retourne l'indice d'élément dans table"""
    for i in range(len(table)):
        if table[i] == element:
            return i
    return -1

def EncodeBase64(tabMessage):
    """ Encode en base 64 le paramètre chaine"""
    """ tabMessage contient le message sous forme de tableau d'octets"""
    """ Retourne un tableau d'octets."""
    encoded_message = base64.standard_b64encode(tabMessage)
    return encoded_message

def DecodeBase64(strMessage):
    """ Decode la chaine encodée en base 64"""
    """ strMessage doit être une chaine ASCII elle sera encodée en utf-8"""
    """ retourne un tableau d'octets"""
    decoded_message = base64.standard_b64decode(strMessage)
    return decoded_message

def EncodeAES_ECB(strMessage,tabKey):
    """ Chiffrement AES-ECB 128 bits de strMessage avec tabKey comme clef.
        La taille de chaine est quelconque et sera complétée par des
        caractères espace si nécessaire. tabKey est un tableau 16 éléments.
        Avant chiffrement la chaine est encodée en utf8 """
    if (len(strMessage)>16):
        return EncodeAES_ECB(strMessage[0:16],tabKey)+EncodeAES_ECB(strMessage[16:],tabKey)
    else:
        while (len(strMessage) < 16):
            strMessage += ' '
        cipher = Cipher(algorithms.AES(bytearray(tabKey)), modes.ECB())
        encryptor = cipher.encryptor()
        ct = encryptor.update(toTab(strMessage)) + encryptor.finalize()
        return ct

def DecodeAES_ECB(tabMessage,tabKey):
    """ Dechiffrement AES ECB de tabMessage. La clef tabKey est un tableau de 16 éléments.
        Retourne un tableau d'octets. Les caractères espace en fin de
        tableau sont supprimés."""
    cipher = Cipher(algorithms.AES(bytearray(tabKey)), modes.ECB())
    decryptor = cipher.decryptor()
    return decryptor.update(tabMessage).strip()

def Contient(aiguille,chaine):
    """ Resultat True si le paramètre chaine contient la chaine aiguille."""
    return aiguille in chaine

def EstImprimable(caractere):
    """ Liste des caractères imprimables :
        0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
    chaine = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~ "
    return Contient(caractere, chaine)

def Remplace(chaine,avant,apres):
    """ Remplace les occurrences de avant par apres dans chaine."""
    return chaine.replace(avant, apres)

def Extraire(chaine,separation,n):
    """ Retourne la valeur du nième champ de chaine.
        Les champs sont séparés par le caractÃ¨re séparation."""
    split_str = chaine.split(separation)
    return int(split_str[n])

def Format(n):
    """ Retourne une chaine de caractères de 4 caractères pour tout nombre entier de 0 à  9999
        Les valeurs seront précédées de 0."""
    chaine = str(n)
    while (len(chaine) < 4):
        chaine = "0" + chaine
    return chaine


def toTab(strMessage):
    """ Encode une chaine en tableau d'octets. l'encodage utilisé est "utf-8"""
    return bytearray(strMessage, "utf-8")

def toStr(strMessage):
    """Decode un tableau d'octets en chaine utf-8"""
    return strMessage.decode("utf-8")

def main():
    """ Tests, toutes les lignes sont correctes (résultat : True). Complèter les fonctions."""
    import sys
    print (sys.version)

    print ("Test EncodeXor() : ", EncodeXor("Bonjour".encode(),"A".encode())==b'\x03./+.43')
    print ("Test DecodeXor() : ", DecodeXor(b"\n'..-","B".encode()).decode()=="Hello")
    print ("Test 2 EncodeXor() : ", EncodeXor(b"GoodBye",b"ABA")==b'\x06-.%\x008$')
    print ("Test 2 EncodeXor() : ", DecodeXor(b'\x0e42;8',b"ZWZ")=="Tchao".encode())
    print ("Test Indice() :", Indice([1,2,3,4,5,6],3)==2)
    print ("Test EncodeBase64() : ", EncodeBase64(b"Une Chaine")==b"VW5lIENoYWluZQ==")
    print ("Test DecodeBase64() : ", DecodeBase64("VW5lIENoYWluZQ==")==b"Une Chaine")
    print ("Test EncodeAES_ECB() : ", EncodeAES_ECB("Elements",[161, 216, 149, 60, 177, 180, 108, 234, 176, 12, 149, 45, 255, 157, 80, 136])==b'Z\xf5T\xef\x9f\x8bg\x15\xb3E\xe7&gm\x96\x1d')
    print ("Test DecodeAES_ECB() : ", DecodeAES_ECB(b'Z\xf5T\xef\x9f\x8bg\x15\xb3E\xe7&gm\x96\x1d',[161, 216, 149, 60, 177, 180, 108, 234, 176, 12, 149, 45, 255, 157, 80, 136]).strip()==b"Elements")
    print ("Test Contient() :", Contient("OK","Le resultat est OK !")==True)
    print ("Test 2 Contient() :", Contient("OK","Le resultat est Ok !")==False)
    print ("Test EstImprimable() :", EstImprimable("A")==True)
    print ("Test 2 EstImprimable() :", EstImprimable("\x07")==False)
    print ("Test 3 EstImprimable(): ", EstImprimable(" ")==True)
    print ("Test Remplace() : ", Remplace("Ceci est une string typique","string","chaine")=="Ceci est une chaine typique")
    print ("Test Extraire() : ", Extraire("ROUGE,0034,4EF563",",",1)==34)
    print ("Test Format() : ", Format(3)=="0003")
    print ("Test 2 Format() : ", Format(123)=="0123")
    print ("Test toStr() : ", toStr(b"\x41\x42")=="AB")
    print ("Test toTab() : ", toTab("CD")==b"\x43\x44")
    #return


if __name__ == '__main__':
    #print(EncodeXor(b"/ISIMA/SECRET_YIDIISTSA/CHALLENGE_1/DEFI_6/GROUPE_XX/LEDS/#",b"XORKEYDESPROFS"))
    #print(DecodeXor(EncodeXor(b"/ISIMA/SECRET_YIDIISTSA/CHALLENGE_1/DEFI_6/GROUPE_XX/LEDS/#",b"XORKEYDESPROFS"), b"XORKEYDESPROFS"))
    main()
