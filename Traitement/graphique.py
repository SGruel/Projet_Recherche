import pylab as py
import numpy as np
from Traitement.formatage import formatage
from MIDAS.vitesseMidas import globalMidas
from Moindres_Carres.vitesse_MC import moindreCarres

def graphiqueUnique(link):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculer par
    moindres carrées en fonction du temps et comparer cela avec la vitesse obtenue avec la méthode MIDAS

    :param link: chemin vers le fichier .xyz
    :type link: str
    :return:
    """
    data = formatage(link)
    vitesseMidas = globalMidas(data)
    #liste_MC_final = moindreCarres(data)

    #une liste avec un pas régulier pour afficher en fonction du nombre de mesure
    nb_mesures = np.arange(50,2000,50)

    # les listes que l'on affichera ensuite
    vitesse_E = []
    vitesse_N = []
    vitesse_h = []

    # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesure:
        data = formatage(link, nb_jour = i)
        liste_MC = moindresCarres(data)
        vitesse_E.append(liste_MC[0][2][0])
        vitesse_N.append(liste_MC[1][2][0])
        vitesse_h.append(liste_MC[2][2][0])

    #figure de la vitesse sur l'axe E
    py.figure(0)

    py.plot(nb_mesures, vitesse_E, 'g', label='vitesse moindres carrées sur E')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[0][0]], 'r', label='vitesse MIDAS sur E')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe E en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_E")

    # figure de la vitesse sur l'axe N
    py.figure(1)

    py.plot(nb_mesures, vitesse_N, 'g', label='vitesse moindres carrées sur N')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[1][0]], 'r', label='vitesse MIDAS sur N')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe N en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_N")

    # figure de la vitesse sur l'axe h
    py.figure(2)

    py.plot(nb_mesures, vitesse_h, 'g', label='vitesse moindres carrées sur h')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[2][0]], 'r', label='vitesse MIDAS sur h')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe h en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_h")


def graphiqueMidas(link):
    data = formatage(link)

    #les listes que l'on affichera ensuite
    vitesseMidas_E = []
    vitesseMidas_N = []
    vitesseMidas_h = []
    ecartype_E     = []
    ecartype_N     = []
    ecartype_h     = []

    #on varie la longueur du pas pour faciliter le calcul
    nb1 = np.arange(50, 400, 10)
    nb2 = np.arange(400, 1000, 50)
    nb3 = np.arange(1000, len(data) + 100, 100)
    nb_mesure = np.concatenate((nb1, nb2, nb3), axis=0)

    #pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesure:
        print(i)
        data = formatage(link, nb_jour = i)
        vitesseMidas = globalMidas(data)
        vitesseMidas_E.append(vitesseMidas[0][0])
        ecartype_E.append(vitesseMidas[1][0])
        vitesseMidas_N.append(vitesseMidas[0][1])
        ecartype_N.append(vitesseMidas[1][1])
        vitesseMidas_h.append(vitesseMidas[0][2])
        ecartype_h.append(vitesseMidas[1][2])

    #figure avec les vitesses sur chaque axes
    py.figure(0)

    py.plot(nb_mesure, vitesseMidas_E, 'g', label="vitesse sur l'axe E")
    py.plot(nb_mesure, vitesseMidas_N, 'r', label="vitesse sur l'axe N")
    py.plot(nb_mesure, vitesseMidas_h, 'b', label="vitesse sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MIDAS\\" + link[-12:-8] + "_vitesse")

    #figure avec les écart-types de la mesures des vitesses
    py.figure(1)

    py.plot(nb_mesure, ecartype_E, 'g', label="ecart-type sur l'axe E")
    py.plot(nb_mesure, ecartype_N, 'r', label="ecart-type sur l'axe N")
    py.plot(nb_mesure, ecartype_h, 'b', label="ecart-type sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Ecart-type en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MIDAS\\" + link[-12:-8] + "_ecart_type")

def graphiqueData(link):
    data = formatage(link)

    t = data[:,1]
    E = data[:,2]
    N = data[:,3]
    h = data[:,4]

    py.figure(0)

    py.plot(t, E, 'g', label='position sur E')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_E")

    py.figure(1)

    py.plot(t, N, 'g', label='position sur N')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_N")

    py.figure(2)

    py.plot(t, h, 'g', label='position sur h')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_h")

def graphiqueTot(link):
    data = formatage(link)
    vitesseMidas = globalMidas(data)
    MC = moindreCarres(data, [365.25, 365.25/2])

    t = data[:, 1]
    E = data[:, 2]
    N = data[:, 3]
    h = data[:, 4]

    E_midas = []
    N_midas = []
    h_midas = []
    E_mc = []
    N_mc = []
    h_mc = []
    print(MC)
    for i in range(len(data)):
        E_midas.append(data[0][2] + vitesseMidas[0][0]*(data[i][1] - data[0][1]))
        N_midas.append(data[0][3] + vitesseMidas[0][1]*(data[i][1] - data[0][1]))
        h_midas.append(data[0][4] + vitesseMidas[0][2]*(data[i][1] - data[0][1]))
        E_mc.append(MC[1][1][0] + MC[1][2][0]*(data[i][1] - MC[0]) + MC[1][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[1][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[1][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[1][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        N_mc.append(MC[2][1][0] + MC[2][2][0]*(data[i][1] - MC[0]) + MC[2][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[2][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[2][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[2][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        h_mc.append(MC[3][1][0] + MC[3][2][0]*(data[i][1] - MC[0]) + MC[3][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[3][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[3][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[3][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))


    py.figure(0)

    py.plot(t, E, 'g', label='position sur E')
    py.plot(t, E_midas, 'r', label='position sur E prédit par MIDAS')
    py.plot(t, E_mc, 'b', label='position sur E predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_E")

    py.figure(1)

    py.plot(t, N, 'g', label='position sur N')
    py.plot(t, N_midas, 'r', label='position sur N prédit par MIDAS')
    py.plot(t, N_mc, 'b', label='position sur N predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_N")

    py.figure(2)

    py.plot(t, h, 'g', label='position sur h')
    py.plot(t, h_midas, 'r', label='position sur h prédit par MIDAS')
    py.plot(t, h_mc, 'b', label='position sur h predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_h")