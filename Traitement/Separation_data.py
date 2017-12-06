import os
import re

fichier = open("C:\\Users\\Hul\\Desktop\\Projet_recherche\\liste_dis.txt", 'r')
lignes = fichier.readlines()
fichier.close()
print(lignes)

fichier2 = open("C:\\Users\\Hul\\Desktop\\Projet_recherche\\ITRF2014-soln-gnss.snx", 'r')
exclu = fichier2.readlines()
liste_sta = []
for i in exclu:
    if "V -" in i and "00:000:00000 00:000:00000 V -" not in i:
        liste_sta.append(i[1:5])

path = "C:\\Users\\Hul\\Desktop\\Projet_recherche\\DataIGS08"
liste_dos = os.listdir(path)
for i in range(len(os.listdir(path))):
    if liste_dos[i][-3:] == "xyz":
        bool = False
        for j in lignes:
            if liste_dos[i][0:4] in j:
                bool = True
        if bool and liste_dos[i][0:4] not in liste_sta:
            trans = open(path + "\\" + liste_dos[i], 'r')
            text = trans.read()
            newtext = open(path + "\\new_dos\\" + liste_dos[i], 'w')
            newtext.write(text)
            newtext.close()
            trans.close()