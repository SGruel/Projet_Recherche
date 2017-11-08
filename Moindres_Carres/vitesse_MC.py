import numpy as np


def moindreCarres(data, covariance=False, *periode):
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


def matriceB(data, axe):
    """
    creation de la matrice des observations à partir de la donnée formatée, sous forme de colonne (East) ou (North) ou(Up) celon l'axe sur lequel on mesure la vitesse
                                                                                                  
    :param data: jeu de données formaté
    :param axe: axe choisi "East","North" ou "Up"
    
    :return: matrice colonne
    """
    indice = 0
    if axe == "North":
        indice = 3
    elif axe == "East":
        indice = 2
    else:
        indice = 4

    B = np.zeros((len(data), 1))
    B[:, 0] = data[:, indice]
    return B


def matriceA(data, t0, *periode):
    """
    creation de la matrice d'estimation des paramètre;
    autant de ligne que d'observation;
    en colonne: ( 1  t-t0  (cosinus des période) alterné avec (sinusoide des périodes) (indice de saut nul si différent  1 sinon)
    
    
    :param data: jeu formaté
    :param periode: liste des périodes  utilisée
    :param t0: temps de reference
    :return: matrice
    """
    nb_serie = int(data[-1:0])
    A = np.zeros((len(data), 2 + 2 * len(*periode)) + nb_serie)
    A[:0] = 1
    A[:1] = (data[:1] - t0) / 365.25
    for i in range(len(*periode)):
        #implementation des coefficient de périodicité
        A[:i + 2] = np.cos(((data[:1] - t0) / 365.25) / periode[i])
        A[:i + 3] = np.sin(((data[:1] - t0) / 365.25) / periode[i])
    #indice de saut
    A[:int(data[:0]) + 1 + 2 * len(*periode)] = 1

    return A

def matriceP(data, axe,covariance=False):
    """
    Creation de la matrice de poids, prend en compte l'ajout d'un matrice de covariance  sinon utilise les écart-types sur le mesure de la donnée formatée
    
    (ne prends pas encore en compte la covariance)8/11
    :param data: jeu de  donnée formaté 
    :param covariance:  matrice  fourni par l'utilisateur , doit etre adaptée au jeu de donnée.
    :param axe: axe choisi "East","North" ou "Up"
    :return: matrice de poids
    
    
    """
    P=np.zeros((len(data),len(data)))
    indice = 0
    if axe == "North":
        indice = 6
    elif axe == "East":
        indice = 5
    else:
        indice = 7
    if covariance == False:
        di=np.diag_indices_from(P)
        P[di] = 1/data[:indice]**2
    return P
        
def matriceNormaleLigne(A, P):
    """
    Fonction de sous-calcul de la matrice normale pour le traitement ligne par ligne. effectue le produit AtPA sur une ligne de la matrice A.
    :param A: ligne de la matrice A 
    :param P: poids de la mesure correspondant à la ligne A
    :return: matrice carrée de la longueur de A
    """
    Nligne=np.dot(np.transpose(A),P*A)
    return Nligne
def vecteurKligne(A, P, B):
    """
    Fonction de calcul d'un élément du vecteur K . Le calcul est fai par ligne  de manière  à alleger ce dernier.
    :param A: ligne de la matrice A
    :param P: poids de la mesure correspondant  à la ligne  A
    :param B:  observation
    :return: matrice composé d'un élément unique
    """
    Kligne=np.dot(np.transpose(A),P*B)

