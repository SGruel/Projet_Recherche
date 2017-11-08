import numpy as np

def formatage(link, nb_jour=-1, date_debut=-1):
    """
    Fonction qui prend en entrée le chemin vers un fichier .xyz, la date du début de considération des données et
    le nombre de jour mesurés que l'on veut étudier à partir de cette date.
    Elle formatera les données contenues dans le .xyz dans un format matriciel exploitable par nos programmes
    Le programme affichera une alerte si la précision de la mesure de la position de la station n'est pas noté par un 'A'.
    Le programme retournera une erreur si le nombre de jour demandé ne correspond pas avec la fin fixé au 15 janvier 2015 de nos series
    de mesures.

    Si le nombre de jour vaut -1, on étudie toute la serie depuis la date de début et
    si la date de début vaut -1, on étudie toute la série depuis le démarrage de la prise de mesures de la station.

    :param link: chemin vers le fichier .xyz
    :param nb_jour: nombre de jour à étudier sur la série
    :param date_debut: date en jour julien modifié à partir de laquelle on commence à étudier la série
    :type link: str
    :type nb_jour: int
    :type date_debut: int
    :return: matrice avec nb_jour ligne et 8 colonne
             la première colonne nous indique les sauts positionnement dans la série
             la deuxième donne la date en jour julien modifié, la troisième à la cinquième donnent la position en E, N et h
             la sixième à la huitième donnent la précision en E, N, h.
    :type return: np.array
    """
    #ouverrture du fichier pour tester la qualité des données
    fichier = open(link, "r")
    liste_lignes = fichier.readlines()
    date_fin = 57037.5

    #on a besoin du j si on a une date de début et un nombre de jour.
    # Dans ce cas, il faut que le nombre de ligne parcouru soit inférieur au nombre de jour
    split = liste_lignes[0].split()
    if date_debut < float(split[3]):
        j = nb_jour
    else:
        j = len(liste_lignes)

    #pour chaque ligne qui fait parti de la suite de jour qui est demandé on teste la qualité pour voir si elle vaut 'A'
    for i in range(0, len(liste_lignes)):
        test_qualite = liste_lignes[i].split()
        if int(float(date_debut)) == int(float(test_qualite[3])):
            j = i + nb_jour

        test_qualite = liste_lignes[i].split()
        if test_qualite[1] != "A" and date_debut <= float(test_qualite[3]) and ((nb_jour == -1 and float(test_qualite[3]) <= date_fin) or (nb_jour != -1 and date_debut == -1 and i < nb_jour) or (nb_jour != -1 and date_debut != -1 and i < j)):
            print("La mesures du jour " + test_qualite[3] + " sur la station " + test_qualite[0] + " n'est noté que " + test_qualite[1])

    fichier.close()

    mat_brute = np.genfromtxt(link )
    if nb_jour == -1:
        if date_debut < float(split[4]): #split[4] correspond à la date de la première mesure
            mat_affinee = np.zeros((len(liste_lignes), 8))
        else:
            indice_ligne_debut_mesure = j - nb_jour
            mat_affinee = np.zeros((len(liste_lignes) - indice_ligne_debut_mesure), 8)
    else:
        mat_affinee = np.zeros((nb_jour, 8))

    num_ligne = 0
    for i in range(0, len(mat_brute)):
        if date_debut <= mat_brute[i][3] and ((nb_jour == -1 and mat_brute[i][3] <= date_fin) or (nb_jour != -1 and date_debut == -1 and i < nb_jour) or (nb_jour != -1 and date_debut != -1 and i < j)):
            mat_affinee[num_ligne][0] = mat_brute[i][2]
            mat_affinee[num_ligne][1] = mat_brute[i][3]
            mat_affinee[num_ligne][2] = mat_brute[i][6]
            mat_affinee[num_ligne][3] = mat_brute[i][7]
            mat_affinee[num_ligne][4] = mat_brute[i][8]
            mat_affinee[num_ligne][5] = mat_brute[i][9]
            mat_affinee[num_ligne][6] = mat_brute[i][10]
            mat_affinee[num_ligne][7] = mat_brute[i][11]
            num_ligne += 1

    return mat_affinee