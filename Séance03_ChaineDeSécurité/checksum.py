def longueurChaine(chaine):
    i=0
    for car in chaine:
        i+=1
    return i
    
def decoupeChaine(chaine):
    chaine2=chaine[1:-2]
    return chaine2

def checksum(chaine):
    chaine2=decoupeChaine(chaine)
    long=longueurChaine(chaine2)
    somme=0
    i=0
    while i<long:
        somme=somme+int(chaine2[i:i+2],16)
        i+=2
    somme=somme%256
    complement=256-somme
    complement=hex(complement)
    return(complement)


chaine = ":10455000068183207F0FF08FC021050130A740357B"
print(checksum(chaine))