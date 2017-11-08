import numpy as np

def globalMidas(data, periode=365):
    """
    Fonction qui va appliquer la méthode de calcul de vitesse de station GNSS de l'estimateur MIDAS. Sur chaque coordonnées de la station.

    Si la durée de la série est trop faible vis à vis de la periode des phénomènes dont on cherche à enlever l'influence dans le
    calcul de la vitesse, une alerte envoyé à l'utilisateur.

    :param data: données formatées par notre fonction formatage localisée dans le dossier Traitement
    :param periode: la période est une durée en jour qui choisiera le nombre de jour entre deux date utiliser pour calculer la vitesse
                    avec l'estimateur MIDAS
    :type data: np.array
    :type periode: int
    :return: renvoi une matrice de deux lignes et trois colonnes, la première ligne est la vitesse sur chaque coordonnées
             calculé avec l'estimateur MIDAS la deuxième ligne est l'écart-type des vitesses calculées
    :type return: np.array
    """

    #reformatage
    mat_E = np.zeros((len(data), 2))
    mat_N = np.zeros((len(data), 2))
    mat_h = np.zeros((len(data), 2))

    for i in range(len(data)):
        mat_E[i][0] = data[i][1]
        mat_E[i][1] = data[i][2]
        mat_N[i][0] = data[i][1]
        mat_N[i][1] = data[i][3]
        mat_h[i][0] = data[i][1]
        mat_h[i][1] = data[i][4]

    #mise en forme de la matrice retour
    retour = np.zeros((2,3))

    E = vitesseMidas(mat_E, periode)
    N = vitesseMidas(mat_N, periode)
    h = vitesseMidas(mat_h, periode)

    retour[0][0] = E[0]
    retour[1][0] = E[1]
    retour[0][1] = N[0]
    retour[1][1] = N[1]
    retour[0][2] = h[0]
    retour[1][2] = h[1]

    return retour

def vitesseMidas(data, periode):
    """
    Fonction qui applique la méthode d'estimation de vitesse MIDAS sur une série de coordonnées datée.

    :param data: matrice de taille (2,n) qui contient les dates sur la première colonne et les positions sur la deuxième
    :param periode: la période est une durée en jour qui choisiera le nombre de jour entre deux date utiliser pour calculer la vitesse
                    avec l'estimateur MIDAS
    :type data: np.array
    :type param: int
    :return: un array de taille 2 qui contient la vitesse calculé par l'estimateur MIDAS et l'écart-type qui lui est associé
    :type return: list
    """
    #la liste contenant toute les vitesses calculer
    liste_sens_direct = appairage_vitesse(data, periode)
    data_indirect = data[::-1]
    liste_sens_indirect = appairage_vitesse(data_indirect, -periode)

    liste_vitesse = liste_sens_direct + liste_sens_indirect
    vitesse = np.array(liste_vitesse)
    mediane = np.median(vitesse)
    delta_vitesse = vitesse - mediane
    delta_vitesse = abs(delta_vitesse)
    mad = np.median(delta_vitesse))
    mad = np.median(delta_vitesse)
    sigma = 1.4826*mad

    liste_vitesse_epurre = []
    for i in vitesse:
        if abs(i - mediane) < 2*sigma:
            liste_vitesse_epurre.append(i)
    liste_vitesse_epurre = np.array(liste_vitesse_epurre)
    mediane = np.median(liste_vitesse_epurre)
    delta_vitesse = liste_vitesse_epurre - mediane
    delta_vitesse = abs(delta_vitesse)
    mad = np.median(delta_vitesse)
    sigma = 1.4826*mad
    return [mediane, sigma]

def appairage_vitesse(data, periode):
    """
    Fonction qui appaire entre elles les mesures de coordonnées pour correspondre à l'algorithme de MIDAS
    et en déduire une liste de vitesse

    :param data: matrice de taille (2,n) qui contient les dates sur la première colonne et les positions sur la deuxième
    :param periode: la période est une durée en jour qui choisiera le nombre de jour entre deux date utiliser pour calculer la vitesse
                    avec l'estimateur MIDAS
    :type data: np.array
    :type param: int
    :return: une liste de vitesse
    :type return: list
    """
    liste_vitesse = []
    #vecteur qui indiquera si une valeur de position à déjà été appairé à une autre
    pairage = np.zeros(len(data))

    #on fait les appairages évident car distant de 1 an
    for i in range(len(data)):
        for j in range(i, len(data)):
            if data[i][0] == data[j][0] + periode:
                liste_vitesse.append((data[j][1] - data[i][1])/(data[j][0] - data[i][0]))
                pairage[i] = 1
                pairage[j] = 1
                break

    #on cherche pour chacune mesures non appairées la mesures la plus proche de une période en temps
    for i in range(len(data)):
        dist_opti = -1
        indice_opti = False
        if not(pairage[i]):
            #on recherche la meilleure paire
            for j in range(len(data)):
                if not(pairage[j]) and i!=j:
                    delta = data[j][0] - data[i][0]
                    dist_periode = abs(delta - periode)
                    dist_moins_periode = abs(delta + periode)
                    if dist_opti > dist_periode or dist_opti ==-1:
                        dist_opti = dist_periode
                        indice_opti = j
                    if dist_opti > dist_moins_periode:
                        dist_opti = dist_moins_periode
                        indice_opti = j
            #on l'utilise pour calculer une vitesse
            if indice_opti != False:
                liste_vitesse.append((data[indice_opti][1] - data[i][1]) / (data[indice_opti][0] - data[i][0]))
                pairage[i] = 1
                pairage[indice_opti] = 1
            #si il n'y a plus de meilleure autre paire alors c'est qu'il n'y a plus aucune valeur disponible et donc on peut sortir
            #de la boucle
            else:
                break
    return liste_vitesse