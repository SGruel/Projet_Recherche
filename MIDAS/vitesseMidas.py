

def vitesseMidas(data, periode=365):
    """
    Fonction qui va appliquer la méthode de calcul de vitesse de station GNSS de l'estimateur MIDAS.

    Si la durée de la série est trop faible vis à vis de la periode des phénomènes dont on cherche à enlever l'influence,
    une alerte envoyé à l'utilisateur.

    :param data: données formatées par notre fonction formatage dans le dossier Traitement
    :param periode: la période est une durée en jour qui choisiera le nombre de jour entre deux date utiliser pour calculer la vitesse
                    avec l'estimateur MIDAS
    :return: renvoi une matrice de une ligne et deux colonnes, le première élément est la vitesse calculé avec l'estimateur MIDAS,
             le deuxième élément est l'écart-type sur la vitesse calculé.
    """