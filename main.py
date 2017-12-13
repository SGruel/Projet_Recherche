import os
import Traitement.graphique as gr
from Moindres_Carres.MC_scipy import test_MC, test_ls, test_saut_ls
from Moindres_Carres.vitesse_MC import moindreCarres
from Traitement.formatage import formatage
from Traitement.graphique import graphiqueCompMC
import time
from Traitement.sauvegardetxt import txtMidas

path='./Test'
liste_dos= os.listdir(path)
for file in liste_dos:
    if file[-1]=='z':
        txtMidas(path+'/'+file)

