import os
import Traitement.graphique as gr
from Moindres_Carres.MC_scipy import test_MC, test_ls, test_saut_ls
from Moindres_Carres.vitesse_MC import moindreCarres
from Traitement.formatage import formatage

path = "C:\\Users\\Hul\\Desktop\\Projet_recherche\\DataIGS08"

for element in os.listdir("C:\\Users\\Hul\\Desktop\\Projet_recherche\\DataIGS08"):
    print(element)
    if element[-3:] == "xyz":
        gr.graphiqueMidas(path + "\\" + element)

#data = formatage(path)
#r = test_ls(2, 5, 10, -3)
#r = test_MC(data)

#mc = moindreCarres(data, [365.25, 365.25/2])
#gr.graphiqueMidas(path)
#gr.graphiqueTot(path)

#print("E" + str(r[0].x) + "\nmc" + str(mc[1]))
#print("N" + str(r[1].x) + "\nmc" + str(mc[2]))
#print("h" + str(r[2].x) + "\nmc" + str(mc[3]))

#print("compa E" + str(r[0].x[0] - mc[1][1][0]))
#print("compa vitesse E" + str(r[0].x[1] - mc[1][2][0]))
#gr.graphiqueUnique(path)
#gr.graphiqueCompMC(path)
