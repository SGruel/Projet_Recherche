import numpy as np

def moindre_carres(data,covariance=False,*periode):
    """
    Renvoie le résultat d'un traitement par moindre carrés d'un jeu de données formaté par la méthode formatage. 
    Les parametres d'entrée sont envoyés par la fonction traitement.
    :param data: jeu de données comprenant date série E N U  et écarts type sur ces coordonnées.
    :param covariance: Matrice de covariance supplémentaire dans le cadre de param^tre extérieures  intervnant sur la donnée mesurée
    :param *periode: périodes influencant la donnée, celles-ci peuvent etre multiple ( a entrer sous forme de liste)
    :type data: numpy.array
    :type covariance:numpy.array
    :type periode list
    :return: liste des paramêtres déterminés pour chacun des axes avec leur écart-types, les 3 derniers éléments correspondent à l'écartype au carré total des moindres carrés.
    """










def matrice_B(data,):
    """
    creation de la matrice des observations à partir de la donnée formatée, sous forme de colonne (East) ou (North) ou(Up) celon l'axe sur lequel on mesure la vitesse
                                                                                                  
    :param data: jeu de données formaté
    :return: matrice colonne
    """



def matrice_A(data,*periode):
    """
    creation de la matrice d'estimation des paramêtre;
    autant de ligne que d'observation;
    en colonne: ( 1  t-t0   (sinusoide des périodes) (indice de saut nul si différent  1 sinon)
    
    
    :param data: jeu formaté
    :param periode: liste des périodes  utilisée
    :return: matrice
    """