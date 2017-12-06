from Moindres_Carres.MC_scipy import test_MC, test_ls, test_saut_ls
from Moindres_Carres.vitesse_MC import moindreCarres
from Traitement.formatage import formatage
import numpy as np
import pylab as py

path = "C:\\Users\\Hul\\Desktop\\Projet_recherche\\TOUL_igs.xyz"

data = formatage(path)
data[140][2] = -50000
a = test_MC(data)
b = moindreCarres(data, periode=[365.25, 365.25/2], robust=True, extend=True)

#Sur axe E
t = data[:,1]
E = data[:,2]
residu_sc = a[0].fun
residu_mc = b[2][len(b[2])-1]

py.figure(0)
#py.plot(t, E, 'g', label='position sur E')
py.plot(t, E + residu_sc, 'r', label='position sur E prédit par scipy')
py.plot(t, residu_mc[1], 'b', label='position sur E predit par les paramètres moindres carrés')
py.xlabel("Temps en jour de mesure (j)")
py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
py.legend()
py.show()

