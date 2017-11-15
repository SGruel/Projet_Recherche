import pylab as py
import numpy as np
from Traitement.formatage import formatage
from MIDAS.vitesseMidas import globalMidas
from Moindres_Carres.vitesse_MC import moindreCarres

def traitementUnique(link):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculer par
    moindres carrées en fonction du temps et comparer cela avec la vitesse obtenue avec la méthode MIDAS

    :param link: chemin vers le fichier .xyz
    :type link: str
    :return:
    """
    data = formatage(link)
    vitesseMidas = globalMidas(data)
    liste_MC_final = moindresCarres(data)

    t = np.arange(50,2000,50)
    vitesse_t_E = []
    vitesse_t_N = []
    vitesse_t_h = []

    for i in t:
        data = formataga(link, nb_jour = i)
        liste_MC = moindresCarres(data)
        vitesse_t_E.append(liste_MC[0][2][0])
        vitesse_t_N.append(liste_MC[1][2][0])
        vitesse_t_h.append(liste_MC[2][2][0])

    py.figure(0)

    py.plot(t, vitesse_t_E, 'g', label='vitesse moindres carrées sur E')
    py.plot(t, len(t) * [vitesseMidas[0][0]], 'r', label='vitesse MIDAS sur E')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe E en fonction du nombre de jour de mesure (m/j)")
    py.legend()

    py.show()

    py.figure(1)

    py.plot(t, vitesse_t_N, 'g', label='vitesse moindres carrées sur N')
    py.plot(t, len(t) * [vitesseMidas[1][0]], 'r', label='vitesse MIDAS sur N')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe N en fonction du nombre de jour de mesure (m/j)")
    py.legend()

    py.show()

    py.figure(2)

    py.plot(t, vitesse_t_h, 'g', label='vitesse moindres carrées sur h')
    py.plot(t, len(t) * [vitesseMidas[2][0]], 'r', label='vitesse MIDAS sur h')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe h en fonction du nombre de jour de mesure (m/j)")
    py.legend()

    py.show()

def traitementMidas(link):
    data = formatage(link)
    vitesseMidas_final = globalMidas(data)

    vitesseMidas_E = []
    vitesseMidas_N = []
    vitesseMidas_h = []
    ecartype_E     = []
    ecartype_N     = []
    ecartype_h     = []
    t = np.arange(50, 2000, 50)
    for i in t:
        data = formatage(link, nb_jour = i)
        vitesseMidas = globalMidas(data)
        vitesseMidas_E.append(vitesseMidas[0][0])
        ecartype_E.append(vitesseMidas[0][1])
        vitesseMidas_N.append(vitesseMidas[1][0])
        ecartype_N.append(vitesseMidas[1][1])
        vitesseMidas_h.append(vitesseMidas[2][0])
        ecartype_h.append(vitesseMidas[2][1])

    py.figure(0)

    py.plot(t, vitesseMidas_E, 'g', label="vitesse sur l'axe E")
    py.plot(t, vitesseMidas_N, 'r', label="vitesse sur l'axe N")
    py.plot(t, vitesseMidas_h, 'b', label="vitesse sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse en fonction du nombre de jour de mesure (m/j)")
    py.legend()

    py.show()

    py.figure(1)

    py.plot(t, ecartype_E, 'g', label="ecart-type sur l'axe E")
    py.plot(t, ecartype_N, 'r', label="ecart-type sur l'axe N")
    py.plot(t, ecartype_h, 'b', label="ecart-type sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Ecart-type en fonction du nombre de jour de mesure (m/j)")
    py.legend()

    py.show()