import pylab as py
import numpy as np
import time
from Traitement.formatage import formatage
from MIDAS.vitesseMidas import globalMidas
from Moindres_Carres.vitesse_MC import moindreCarres
from Moindres_Carres.MC_scipy import test_MC
from Traitement.mesure_palier import palier
import os
import csv


def graphiqueUnique(link):
    """
    Fonction qui va analyser un fichier .xyz pour sortir des graphiques sur l'évolution de la vitesse calculée par
    moindres carrées en fonction du temps et comparer cela avec la vitesse obtenue avec la méthode MIDAS.
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)
    vitesseMidas = globalMidas(data)
    liste_MC_final = moindreCarres(data, [365.25, 365.25 / 2])

    # une liste avec un pas régulier pour afficher en fonction du nombre de mesure
    nb_mesures = np.arange(350, len(data), 50)

    # les listes que l'on affichera ensuite
    vitesse_E = []
    vitesse_N = []
    vitesse_h = []

    # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesures:
        data = formatage(link, nb_jour=i)
        liste_MC = moindreCarres(data, [365.25, 365.25 / 2])
        vitesse_E.append(liste_MC[1][2][0])
        vitesse_N.append(liste_MC[2][2][0])
        vitesse_h.append(liste_MC[3][2][0])

    # figure de la vitesse sur l'axe E
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

    # les listes que l'on affichera ensuite
    vitesseMidas_E = []
    vitesseMidas_N = []
    vitesseMidas_h = []
    ecartype_E = []
    ecartype_N = []
    ecartype_h = []

    # on varie la longueur du pas pour faciliter le calcul
    nb1 = np.arange(50, 400, 10)
    nb2 = np.arange(400, 1000, 50)
    nb3 = np.arange(1000, min(len(data), 1900) + 100, 100)
    nb4 = np.arange(2000, len(data), 500)
    nb_mesure = np.concatenate((nb1, nb2, nb3, nb4), axis=0)

    # pour chaque nombre de mesures, on effectue le calcul et on rempli chaques listes
    for i in nb_mesure:
        print(i)
        data = formatage(link, nb_jour=i)
        vitesseMidas = globalMidas(data)
        vitesseMidas_E.append(vitesseMidas[0][0])
        ecartype_E.append(vitesseMidas[1][0])
        vitesseMidas_N.append(vitesseMidas[0][1])
        ecartype_N.append(vitesseMidas[1][1])
        vitesseMidas_h.append(vitesseMidas[0][2])
        ecartype_h.append(vitesseMidas[1][2])

    # figure avec les vitesses sur chaque axes
    py.figure(3)

    py.plot(nb_mesure, vitesseMidas_E, 'g', label="vitesse sur l'axe E")
    py.plot(nb_mesure, vitesseMidas_N, 'r', label="vitesse sur l'axe N")
    py.plot(nb_mesure, vitesseMidas_h, 'b', label="vitesse sur l'axe h")
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Vitesse en fonction du nombre de jour de mesure (m/j)")
    py.legend()
    py.savefig("..\\graph\\MIDAS\\" + link[-12:-8] + "_vitesse")
    py.close()

    # figure avec les écart-types de la mesures des vitesses
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

    t = data[:, 1]
    E = data[:, 2]
    N = data[:, 3]
    h = data[:, 4]

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
    MC = moindreCarres(data, [365.25, 365.25 / 2])

    t = data[:, 1]
    E = data[:, 2]
    N = data[:, 3]
    h = data[:, 4]

    E_midas = []
    N_midas = []
    h_midas = []
    E_mc = MC[1][-1][1]
    N_mc = MC[2][-1][1]
    h_mc = MC[3][-1][1]

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


def graphiqueCompMC(link, periode, robust=False):
    """
    Fonction qui la position prédit par les moindres carrées et par la fonction least_squares de scipy
    Elle les enregistre dans le fichier dédié.

    :param link: chemin vers le fichier .xyz
    :type link: str
    """
    data = formatage(link)
    P = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        P[i, i] = 1

    t1 = time.time()
    MC = moindreCarres(data, periode, robust=robust, extend=True)
    t2 = time.time()
    print("temps Simeon " + str(t2 - t1))
    r = test_MC(data)
    t3 = time.time()
    print("temps ordi " + str(t3 - t2))

    t = data[:, 1]
    E = data[:, 2]
    N = data[:, 3]
    h = data[:, 4]

    E_test = r[0].fun + E
    N_test = r[1].fun + N
    h_test = r[2].fun + h

    t0 = np.mean(data[:, 1])

    E_mc = MC[1][-1][1]
    N_mc = MC[2][-1][1]
    h_mc = MC[3][-1][1]

    py.figure(12)

    py.plot(t, E, 'g', label='position sur E')
    py.plot(t, E_test, 'r', label='position sur E scipy')
    py.plot(t, E_mc, 'b', label='position sur E predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe E en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison_simple\\" + link[-12:-8] + "_E")
    py.close()

    py.figure(13)

    py.plot(t, N, 'g', label='position sur N')
    py.plot(t, N_test, 'r', label='position sur N prédit par scipy')
    py.plot(t, N_mc, 'b', label='position sur N predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe N en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison_simple\\" + link[-12:-8] + "_N")
    py.close()

    py.figure(14)

    py.plot(t, h, 'g', label='position sur h')
    py.plot(t, h_test, 'r', label='position sur h prédit par scipy')
    py.plot(t, h_mc, 'b', label='position sur h predit par les paramètres moindres carrés')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("Position sur l'axe h en fonction du nombre de jour de mesure (m)")
    py.legend()
    py.savefig("..\\graph\\comparaison_simple\\" + link[-12:-8] + "_h")
    py.close()


def graphstation(stationname):
    """
    Permet l'affichage des trois composantes de la coordonnées selon les trois methode de calculs MIDAS MC robuste et MC simple

    :param stationname: nom de la station à traiter
    :return:
    """
    fileMCrobuste = '../Resultatcsv/MC/' + stationname + '_robuste.csv'
    fileMC = '../Resultatcsv/MC/' + stationname + '.csv'
    fileMIDAS = '../Resultatcsv/MIDAS/' + stationname + '.csv'
    MC_robuste = np.genfromtxt(fileMCrobuste, delimiter=',', dtype=float, skip_header=10)
    MC = np.genfromtxt(fileMC, delimiter=',', dtype=float, skip_header=10)
    MIDAS = np.genfromtxt(fileMIDAS, delimiter=',', dtype=float, skip_header=10)
    date_mid = MIDAS[:, 0]
    date = MC[:, 0]

    E_MC = MC[:, 1] * 365.25 * 1000
    N_MC = MC[:, 3] * 365.25 * 1000
    H_MC = MC[:, 5] * 365.25 * 1000
    ecE_MC = MC[:, 2] * 365.25 * 1000
    ecN_MC = MC[:, 4] * 365.25 * 1000
    ecH_MC = MC[:, 6] * 365.25 * 1000

    E_MC_robuste = MC_robuste[:, 1] * 365.25 * 1000
    N_MC_robuste = MC_robuste[:, 3] * 365.25 * 1000
    H_MC_robuste = MC_robuste[:, 5] * 365.25 * 1000
    ecE_MC_robuste = MC_robuste[:, 2] * 365.25 * 1000
    ecN_MC_robuste = MC_robuste[:, 4] * 365.25 * 1000
    ecH_MC_robuste = MC_robuste[:, 6] * 365.25 * 1000

    E_MIDAS = MIDAS[:, 1] * 365.25 * 1000
    N_MIDAS = MIDAS[:, 3] * 365.25 * 1000
    H_MIDAS = MIDAS[:, 5] * 365.25 * 1000
    ecE_MIDAS = MIDAS[:, 2] * 365.25 * 1000
    ecN_MIDAS = MIDAS[:, 4] * 365.25 * 1000
    ecH_MIDAS = MIDAS[:, 6] * 365.25 * 1000

    py.figure(15)
    py.plot(date, E_MC, 'g', label='Moindres Carrés ')
    py.plot(date, ecE_MC + E_MC, 'g--', label='ecart-type sur les moindres carrés')
    py.plot(date, -ecE_MC + E_MC, 'g--')
    py.plot(date, E_MC_robuste, 'r', label='Moindres Carrés robuste ')
    py.plot(date, ecE_MC_robuste + E_MC_robuste, 'r--', label='ecart-type sur les moindres carrés robuste')
    py.plot(date, -ecE_MC_robuste + E_MC_robuste, 'r--')
    py.plot(date_mid, E_MIDAS, 'b', label='Midas')
    py.plot(date_mid, ecE_MIDAS + E_MIDAS, 'b--', label='ecart-type sur MIDAS')
    py.plot(date_mid, -ecE_MIDAS + E_MIDAS, 'b--')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("vitesse(mm/an))")

    py.axis([700, date[-1], E_MC[-1] - 5, E_MC[-1] + 5])
    py.savefig('../graph/triplette/' + stationname + '_E')
    py.close()

    py.figure(16)
    py.plot(date, N_MC, 'g', label='Moindres Carrés ')
    py.plot(date, ecN_MC + N_MC, 'g--', label='ecart-type sur les moindres carrés')
    py.plot(date, -ecN_MC + N_MC, 'g--')
    py.plot(date, N_MC_robuste, 'r', label='Moindres Carrés robuste ')
    py.plot(date, ecN_MC_robuste + N_MC_robuste, 'r--', label='ecart-type sur les moindres carrés robuste')
    py.plot(date, -ecN_MC_robuste + N_MC_robuste, 'r--')
    py.plot(date_mid, N_MIDAS, 'b', label='Midas')
    py.plot(date_mid, ecN_MIDAS + N_MIDAS, 'b--', label='ecart-type sur MIDAS')
    py.plot(date_mid, -ecN_MIDAS + N_MIDAS, 'b--')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("vitesse(mm/an)")
    py.axis([700, date[-1], N_MC[-1] - 5, N_MC[-1] + 5])
    py.savefig('../graph/triplette/' + stationname + '_N')
    py.close()

    py.figure(17)
    py.plot(date, H_MC, 'g', label='Moindres Carrés ')
    py.plot(date, ecH_MC + H_MC, 'g--', label='ecart-type sur les moindres carrés')
    py.plot(date, -ecH_MC + H_MC, 'g--')
    py.plot(date, H_MC_robuste, 'r', label='Moindres Carrés robuste ')
    py.plot(date, ecH_MC_robuste + H_MC_robuste, 'r--', label='ecart-type sur les moindres carrés robuste')
    py.plot(date, -ecH_MC_robuste + H_MC_robuste, 'r--')
    py.plot(date_mid, H_MIDAS, 'b', label='Midas')
    py.plot(date_mid, ecH_MIDAS + H_MIDAS, 'b--', label='ecart-type sur MIDAS')
    py.plot(date_mid, -ecH_MIDAS + H_MIDAS, 'b--')
    py.xlabel("Temps en jour de mesure (j)")
    py.ylabel("vitesse(mm/an)")
    py.axis([700, date[-1], H_MC[-1] - 5, H_MC[-1] + 5])
    py.savefig('../graph/triplette/' + stationname + '_H')

    py.close()


def graph_diff_palier(file):
    data = palier(file)
    name = file[-16:-12]
    py.figure(18)
    py.plot([700, 5000], [0, 0], 'r')
    py.plot(data[0][0], data[0][1], 'g.')
    py.ylabel('Différence par rapport  au palier')
    py.xlabel('temps en jour')
    py.axis([700, 5000, 5, -5])
    py.savefig('../graph/palier/' + name + '_E')
    py.close()

    py.figure(19)
    py.plot([700, 5000], [0, 0], 'r')
    py.plot(data[1][0], data[1][1], 'g.')
    py.ylabel('Différence par rapport  au palier')
    py.xlabel('temps en jour')
    py.axis([700, 5000, 5, -5])
    py.savefig('../graph/palier/' + name + '_N')
    py.close()

    py.figure(20)
    py.plot([700, 5000], [0, 0], 'r')
    py.plot(data[2][0], data[2][1], 'g.')
    py.ylabel('Différence par rapport  au palier')
    py.xlabel('temps en jour')
    py.axis([700, 5000, 5, -5])
    py.savefig('../graph/palier/' + name + '_H')
    py.close()


def graph_proportion(path):
    """

    :param path: chemin vers le lot de données à traiter
    :return: dtrois graph présentant la durée du palier par rapport  à la durée totale

    """
    files = os.listdir(path)

    list_saut = []
    with open('list_saut.csv', 'r') as saut:
        reader = csv.reader(saut, delimiter=' ')
        for row in reader:
            if row != []:
                list_saut.append([row[0], row[1]])
    list_stat = []
    max = 0
    for file in files:
        stat = np.genfromtxt(path + '/' + file, usecols=[0, 1, 3, 5])
        list_stat.append(
            [file[0:4], stat[0, 0], stat[0, 0] - stat[0, 1], stat[0, 0] - stat[0, 2], stat[0, 0] - stat[0, 3]])
        if stat[0][0] > max:
            max = stat[0][0]
    list_point = []
    for saut in list_saut:
        for stat in list_stat:
            if saut[0] == stat[0]:
                list_point.append([saut[1], stat[1] / max, stat[2] / max, stat[3] / max, stat[4] / max])
    ar_point = np.asarray(list_point, dtype=float)

    ar_point_saut = ar_point[np.where(ar_point[:, 0] > 4)]
    ar_point_cons = ar_point[np.where(ar_point[:, 0] <= 4)]

    x_saut = np.arange(len(ar_point_saut))
    py.figure(21)

    ar_point_saut = ar_point_saut[ar_point_saut[:, 1].argsort()]
    for i in range(len(x_saut)):
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 1])
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 2], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_E_saut.png')
    py.close()

    py.figure(22)
    for i in range(len(x_saut)):
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 1])
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 3], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_N_saut.png')
    py.close()
    py.figure(23)

    for i in range(len(x_saut)):
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 1])
        py.axvline(x_saut[i] + 1, 0, ar_point_saut[i, 4], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_H_saut.png')
    py.close()

    x_cons = np.arange(len(ar_point_cons))
    ar_point_cons = ar_point_cons[ar_point_cons[:, 1].argsort()]
    py.figure(24)
    for i in range(len(x_cons)):
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 1])
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 2], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_E.png')
    py.close()
    py.figure(25)
    for i in range(len(x_cons)):
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 1])
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 3], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_N.png')
    py.close()
    py.figure(26)
    for i in range(len(x_cons)):
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 1])
        py.axvline(x_cons[i] + 1, 0, ar_point_cons[i, 4], color='r', linewidth=2.5)
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\proportion\\proportion_H.png')

    py.close()


def boxplot_pal(path):
    """

    :param path: chemin du jeu de donnés a traiter
    :return: diagramme boite du jeu de données
    """
    list_file = os.listdir(path)
    # on cherche le plus long jeu de données
    max = 0
    maxfile = 0

    for file in list_file:
        mat = np.genfromtxt(path + "/" + file, usecols=0, delimiter=',', skip_footer=1)
        if mat[-1] > max:
            max = mat[-1]
            maxfile = file
        if mat[-1] < 4000:
            list_file.remove(file)
    mat_size = np.genfromtxt(path + '/' + maxfile, usecols=0, skip_footer=1, delimiter=',')
    mat_boxplot_E = np.zeros((len(list_file) + 1, len(mat_size) - 1))
    mat_boxplot_N = np.zeros((len(list_file) + 1, len(mat_size) - 1))
    mat_boxplot_H = np.zeros((len(list_file) + 1, len(mat_size) - 1))
    # Ligne: par fichiers valeur vitesse fin-vitesse à tmax-t
    # ligne 0 tmax-t
    j=1
    for i in range(len(mat_size)-1):
        mat_boxplot_E[0, i] = round((mat_size[-1] - mat_size[-j])/365,1)
        mat_boxplot_N[0,i ] = round((mat_size[-1] - mat_size[-j])/365,1)
        mat_boxplot_H[0,i ] = round((mat_size[-1] - mat_size[-j])/365,1)
        j+=1

    for file in range(len(list_file)):
        mat = np.genfromtxt(path + "/" + list_file[file], usecols=(1, 3, 5), delimiter=',', skip_footer=1)
        i = len(mat)-1
        j = 0
        mat = mat * 365000
        while i != 0:
            if abs(mat[-1][0] - mat[i][0]) < 2:
                mat_boxplot_E[file + 1][j] = mat[-1][0] - mat[i][0]
            if abs(mat[-1][1] - mat[i][1]) < 2:
                mat_boxplot_N[file + 1][j] = mat[-1][1] - mat[i][1]
            if abs(mat[-1][2] - mat[i][2]) < 2:
                mat_boxplot_H[file + 1][j] = mat[-1][2] - mat[i][2]
            i-=1
            #if j>12 and j%2 == 0:
             #   j+=0

            #else:
            j+=1
    py.figure(27)
    py.boxplot(mat_boxplot_E[1:,:15],sym="ro",positions=mat_boxplot_E[0,:15],widths=0.1)
    py.axis([-0.5,11,-6,6])
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\boxplot_MC2\\boxplot_E.png')

    py.figure(28)
    py.boxplot(mat_boxplot_N[1:,:15], positions=mat_boxplot_E[0,:15],sym="ro",widths=0.1)
    py.axis([-0.5, 11, -6, 6])
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\boxplot_MC2\\boxplot_N.png')
    py.figure(29)
    py.boxplot(mat_boxplot_H[1:,:15], positions=mat_boxplot_E[0,:15],sym="ro",widths=0.1)
    py.axis([-0.5, 11, -6, 6])
    py.savefig('C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\graph\\boxplot_MC2\\boxplot_H.png')


