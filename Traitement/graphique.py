import pylab as py
import numpy as np
import time
from Traitement.formatage import formatage
from MIDAS.vitesseMidas import globalMidas
from Moindres_Carres.vitesse_MC import moindreCarres
from Moindres_Carres.MC_scipy import test_MC

def graphiqueUnique(link):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculer par
    moindres carrées en fonction du temps et comparer cela avec la vitesse obtenue avec la méthode MIDAS.
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)
    vitesseMidas = globalMidas(data)
    liste_MC_final = moindreCarres(data, [365.25, 365.25/2])

    #une liste avec un pas régulier pour afficher en fonction du nombre de mesure
    nb_mesures = np.arange(350, len(data), 50)

    # les listes que l'on affichera ensuite
    vitesse_E = []
    vitesse_N = []
    vitesse_h = []

    # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesures:
        data = formatage(link, nb_jour = i)
        liste_MC = moindreCarres(data, [365.25, 365.25/2])
        vitesse_E.append(liste_MC[1][2][0])
        vitesse_N.append(liste_MC[2][2][0])
        vitesse_h.append(liste_MC[3][2][0])

    #figure de la vitesse sur l'axe E
    py.figure(0)

    py.plot(nb_mesures, vitesse_E, 'g', label='vitesse moindres carrées sur E')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[0][0]], 'r', label='vitesse MIDAS sur E')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe E en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_E")
    py.close()

    # figure de la vitesse sur l'axe N
    py.figure(1)

    py.plot(nb_mesures, vitesse_N, 'g', label='vitesse moindres carrées sur N')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[0][1]], 'r', label='vitesse MIDAS sur N')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe N en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_N")
    py.close()

    # figure de la vitesse sur l'axe h
    py.figure(2)

    py.plot(nb_mesures, vitesse_h, 'g', label='vitesse moindres carrées sur h')
    py.plot(nb_mesures, len(nb_mesures) * [vitesseMidas[0][2]], 'r', label='vitesse MIDAS sur h')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse sur l'axe h en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MC\\" + link[-12:-8] + "_h")
    py.close()


def graphiqueMidas(link):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculer par
    la méthode MIDAS en fonction du nombre de jour de mesure.
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
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
    nb3 = np.arange(1000, min(len(data),1900) + 100, 100)
    nb4 = np.arange(2000, len(data), 200)
    nb_mesure = np.concatenate((nb1, nb2, nb3, nb4), axis=0)

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
    py.figure(3)

    py.plot(nb_mesure, vitesseMidas_E, 'g', label="vitesse sur l'axe E")
    py.plot(nb_mesure, vitesseMidas_N, 'r', label="vitesse sur l'axe N")
    py.plot(nb_mesure, vitesseMidas_h, 'b', label="vitesse sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MIDAS\\" + link[-12:-8] + "_vitesse")
    py.close()

    #figure avec les écart-types de la mesures des vitesses
    py.figure(4)

    py.plot(nb_mesure, ecartype_E, 'g', label="ecart-type sur l'axe E")
    py.plot(nb_mesure, ecartype_N, 'r', label="ecart-type sur l'axe N")
    py.plot(nb_mesure, ecartype_h, 'b', label="ecart-type sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Ecart-type en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MIDAS\\" + link[-12:-8] + "_ecart_type")
    py.close()


def graphiqueData(link):
    """
    Fonction qui affiche la position d'un jeu de données sur les trois axes de coordonnées.
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)

    t = data[:,1]
    E = data[:,2]
    N = data[:,3]
    h = data[:,4]

    py.figure(5)

    py.plot(t, E, 'g', label='position sur E')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_E")
    py.close()

    py.figure(6)

    py.plot(t, N, 'g', label='position sur N')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_N")
    py.close()

    py.figure(7)

    py.plot(t, h, 'g', label='position sur h')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\position\\" + link[-12:-8] + "_h")
    py.close()


def graphiqueTot(link):
    """
    Fonction qui affiche la position d'un jeu de données sur les trois axes de coordonnées.
    Il affiche en plus la position prédit par les moindres carrées et par MIDAS
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
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
    for i in range(len(data)):
        E_midas.append(data[0][2] + vitesseMidas[0][0]*(data[i][1] - data[0][1]))
        N_midas.append(data[0][3] + vitesseMidas[0][1]*(data[i][1] - data[0][1]))
        h_midas.append(data[0][4] + vitesseMidas[0][2]*(data[i][1] - data[0][1]))
        E_mc.append(MC[1][1][0] + MC[1][2][0]*(data[i][1] - MC[0]) + MC[1][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[1][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[1][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[1][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        N_mc.append(MC[2][1][0] + MC[2][2][0]*(data[i][1] - MC[0]) + MC[2][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[2][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[2][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[2][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        h_mc.append(MC[3][1][0] + MC[3][2][0]*(data[i][1] - MC[0]) + MC[3][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[3][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[3][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[3][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))


    py.figure(8)

    py.plot(t, E, 'g', label='position sur E')
    py.plot(t, E_midas, 'r', label='position sur E prédit par MIDAS')
    py.plot(t, E_mc, 'b', label='position sur E predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_E")
    py.close()

    py.figure(9)

    py.plot(t, N, 'g', label='position sur N')
    py.plot(t, N_midas, 'r', label='position sur N prédit par MIDAS')
    py.plot(t, N_mc, 'b', label='position sur N predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_N")
    py.close()

    py.figure(10)

    py.plot(t, h, 'g', label='position sur h')
    py.plot(t, h_midas, 'r', label='position sur h prédit par MIDAS')
    py.plot(t, h_mc, 'b', label='position sur h predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\prediction\\" + link[-12:-8] + "_h")
    py.close()

def graphiqueCompMC(link):
    """
    Fonction qui la position prédit par les moindres carrées et par la fonction least_squares de scipy
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)

    t1 = time.time()
    MC = moindreCarres(data, [365.25, 365.25/2])
    t2 = time.time()
    print("temps Simeon " + str(t2-t1))
    r = test_MC(data)
    t3 = time.time()
    print("temps ordi " + str(t3-t2))

    t = data[:, 1]
    E = data[:, 2]
    N = data[:, 3]
    h = data[:, 4]

    E_test = []
    N_test = []
    h_test = []
    E_mc = []
    N_mc = []
    h_mc = []
    t0 = np.mean(data[:,1])
    for i in range(len(data)):
        E_test.append(r[0].x[0] + r[0].x[1]*(data[i][1] - t0) + r[0].x[2]*np.cos((data[i][1] - t0)/365.25) + r[0].x[3]*np.sin((data[i][1] - t0)/365.25) + r[0].x[4]*np.cos(2*(data[i][1] - t0)/365.25) + r[0].x[5]*np.sin(2*(data[i][1] - t0)/365.25))
        N_test.append(r[1].x[0] + r[1].x[1]*(data[i][1] - t0) + r[1].x[2]*np.cos((data[i][1] - t0)/365.25) + r[1].x[3]*np.sin((data[i][1] - t0)/365.25) + r[1].x[4]*np.cos(2*(data[i][1] - t0)/365.25) + r[1].x[5]*np.sin(2*(data[i][1] - t0)/365.25))
        h_test.append(r[2].x[0] + r[2].x[1]*(data[i][1] - t0) + r[2].x[2]*np.cos((data[i][1] - t0)/365.25) + r[2].x[3]*np.sin((data[i][1] - t0)/365.25) + r[2].x[4]*np.cos(2*(data[i][1] - t0)/365.25) + r[2].x[5]*np.sin(2*(data[i][1] - t0)/365.25))
        E_mc.append(MC[1][1][0] + MC[1][2][0]*(data[i][1] - MC[0]) + MC[1][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[1][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[1][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[1][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        N_mc.append(MC[2][1][0] + MC[2][2][0]*(data[i][1] - MC[0]) + MC[2][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[2][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[2][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[2][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))
        h_mc.append(MC[3][1][0] + MC[3][2][0]*(data[i][1] - MC[0]) + MC[3][3][0]*np.cos((data[i][1] - MC[0])/365.25) + MC[3][4][0]*np.sin((data[i][1] - MC[0])/365.25) + MC[3][5][0]*np.cos(2*(data[i][1] - MC[0])/365.25) + MC[3][6][0]*np.sin(2*(data[i][1] - MC[0])/365.25))

    py.figure(12)

    py.plot(t, E, 'g', label='position sur E')
    py.plot(t, E_test, 'r', label='position sur E scipy')
    py.plot(t, E_mc, 'b', label='position sur E predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison\\" + link[-12:-8] + "_E")
    py.close()

    py.figure(13)

    py.plot(t, N, 'g', label='position sur N')
    py.plot(t, N_test, 'r', label='position sur N prédit par scipy')
    py.plot(t, N_mc, 'b', label='position sur N predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison\\" + link[-12:-8] + "_N")
    py.close()

    py.figure(14)

    py.plot(t, h, 'g', label='position sur h')
    py.plot(t, h_test, 'r', label='position sur h prédit par scipy')
    py.plot(t, h_mc, 'b', label='position sur h predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison\\" + link[-12:-8] + "_h")
    py.close()