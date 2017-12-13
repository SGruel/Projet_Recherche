import numpy as np
from MIDAS.vitesseMidas import globalMidas
from Traitement.formatage import formatage
from Moindres_Carres.vitesse_MC import moindreCarres
import csv


def txtMidas(link, date_deb=0):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculer par
    la méthode MIDAS en fonction du nombre de jour de mesure.
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)

    # on varie la longueur du pas pour faciliter le calcul
    nb1 = np.arange(50, 400, 10)
    nb2 = np.arange(400, 1000, 50)
    nb3 = np.arange(1000, min(len(data), 1900) + 100, 100)
    nb4 = np.arange(2000, min(len(data), 5000), 500)
    nb_mesure = np.concatenate((nb1, nb2, nb3, nb4, np.array([len(data)])), axis=0)
    path = '../Resultatcsv/MIDAS/'
    with  open(path + link[-12:-8] + '.csv', 'w') as filename :
        file = csv.writer(filename)
        # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
        for i in nb_mesure:
            print(i)
            data = formatage(link, nb_jour=i, date_debut=date_deb)
            vitesseMidas = globalMidas(data)
            vitesseMidas_E = vitesseMidas[0][0]
            ecartype_E = vitesseMidas[1][0]
            vitesseMidas_N = vitesseMidas[0][1]
            ecartype_N = vitesseMidas[1][1]
            vitesseMidas_h = vitesseMidas[0][2]
            ecartype_h = vitesseMidas[1][2]
            file.writerow([i, vitesseMidas_E, ecartype_E, vitesseMidas_N, ecartype_N, vitesseMidas_h, ecartype_h])






def txtMC(link,periode=[365.25,365.25/2],robust=False):
    data = formatage(link)

    liste_MC_final = moindreCarres(data, periode,robust=False)

    # une liste avec un pas régulier pour afficher en fonction du nombre de mesure
    nb_mesures = np.arange(350, len(data), 50)
    path='../Resultatcsv/MC'
    if robust:
        with open(path+link[-12:-8]+'_robuste.csv') as filename:
            file=csv.writer(filename,'w')
            boucle(file,link,periode,robust,nb_mesures)
    else:
        with open(path+link[-12:-8]+'.csv') as filename:
            file=csv.writer(filename,'w')
            boucle(file,link,periode,robust,nb_mesures)

def boucle(file,link,periode,robust,nb_mesures):
    # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesures:
        data = formatage(link, nb_jour=i)
        liste_MC = moindreCarres(data, periode,robust)
        vitesse_E=liste_MC[1][2][0]
        vitesse_N=liste_MC[2][2][0]
        vitesse_h=liste_MC[3][2][0]
        ecart_E = liste_MC[1][2][1]
        ecart_N = liste_MC[2][2][1]
        ecart_h = liste_MC[3][2][1]
        file.writerow([i,vitesse_E,ecart_E,vitesse_N,ecart_N,vitesse_h,ecart_h])