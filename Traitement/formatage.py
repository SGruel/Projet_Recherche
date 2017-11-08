

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
    :return: matrice avec nb_jour ligne et 8 colonne
             la première colonne nous indique les sauts positionnement dans la série
             la deuxième donne la date en jour julien modifié, la troisième à la cinquième donnent la position en E, N et h
             la sixième à la huitième donnent la précision en E, N, h.
    """