from Traitement.graphique import graphiqueMidas, graphiqueUnique
#from Moindres_Carres.MC_scipy import test_MC
from Traitement.formatage import formatage

path = "C:\\Users\\Hul\\Desktop\\Projet_recherche\\TOUL_igs.xyz"

data = formatage(path)
#test_MC(data)
graphiqueMidas(path)