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