import numpy as np


def moindreCarres_iter(data,a,b,p,pointsFaux,extend=False):
    """

    :param data: donnée formatée
    :param a:matrice des paramêtres
    :param b: matrice des observations
    :param p: matrice de poids
    :param pointsFaux:liste des points faux trouvés par les précédentes itérations
    :param extend:
    :return:
    """





    # on calcul la matrice normale avec un traitement par ligne de meme pour le vecteur constant

    N = np.zeros((len(a[0]), len(a[0])))
    K = np.zeros((len(a[0]), 1))
    for i in range(len(a)):

        if i not in pointsFaux:
            Ni = matriceNormaleLigne(a[i], p[i, i])
            Ki = vecteurKligne(a[i, :], p[i][i], b[i])
            N += Ni
            K += Ki
    # on calcul alors les vecteurs des inconnues ainsi que le vecteur residu
    Ninv=np.linalg.inv(N)
    X = np.dot(Ninv, K)
    V = b - np.dot(a, X)
    # on  regarde ensuite le facteur unitaire
    sigma2 = np.dot(np.transpose(V), np.dot(p, V)) / (
        len(data) - len(a[1]))  # len(a[1]) correspondant au nombre de paramêtre
    # on traite ensuite les points faux
    Vnorm=np.zeros((V.shape[0],V.shape[1]))
    for i in range (len(V)):
        test=np.dot(a[i],np.dot(Ninv,a[i].reshape((len(a[i]), 1))))
        sub=sigma2*(1/p[i][i]-np.dot(a[i],np.dot(Ninv,a[i].reshape((len(a[i]), 1)))))
        Vnorm[i]=V[i]/np.sqrt(sigma2*(1/p[i][i]-np.dot(a[i],np.dot(Ninv,a[i].reshape((len(a[i]), 1))))))
    err=np.where(abs(Vnorm)>3)[0]
    max=-1
    ierr=-1
    for e in err:
        if Vnorm[e]> max and e not in pointsFaux:
            max=Vnorm[e]
            ierr=e
    if max != -1:
        pointsFaux.append(ierr)




    #on regarde ensuite les autre éléments statistiques
    covX = sigma2 * np.linalg.inv(N)

    # on extrait maintenant le rendu voulu
    res = [sigma2]
    for i in range(len(X)):
        res.append([X[i], np.sqrt(covX[i][i])])
    if extend== True:
        res.append([V,np.dot(a,X)])
    return [res,pointsFaux]


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


def matriceA(data, t0, periode):
    """
    creation de la matrice d'estimation des paramètre;
    autant de ligne que d'observation;
    en colonne: ( 1  t-t0  (cosinus des période) alterné avec (sinusoide des périodes) (indice de saut nul si différent  1 sinon)
    
    
    :param data: jeu formaté
    :param periode: liste des périodes  utilisée
    :param t0: temps de reference
    :return: matrice
    """

    liste_saut=np.unique(data[:,0])
    nb_serie = len(liste_saut)-1
    A = np.zeros((len(data), 2 + 2 * len(periode) + nb_serie))
    A[:, 0] = 1
    A[:, 1] = (data[:, 1] - t0)
    for i in range(len(periode)):
        # implementation des coefficient de périodicité
        A[:, (2 * i + 2)] = np.cos((A[:, 1] / periode[i]))
        A[:, (2 * i + 3)] = np.sin((A[:, 1] / periode[i]))
    # indice de saut

    for i in range(len(liste_saut)-1):
        loc = np.where(data[:, 0] == liste_saut[i+1])
        A[loc, i + 2 * len(periode) + 2] = 1

    return A


def matriceP(data, axe, covariance=False):
    """
    Creation de la matrice de poids, prend en compte l'ajout d'un matrice de covariance  sinon utilise les écart-types sur le mesure de la donnée formatée
    
    (ne prends pas encore en compte la covariance)8/11
    :param data: jeu de  donnée formaté 
    :param covariance:  matrice  fourni par l'utilisateur , doit etre adaptée au jeu de donnée.(celle-ci doit être diagonale)
    :param axe: axe choisi "East","North" ou "Up"
    :return: matrice de poids
    
    
    """

    P = np.zeros((len(data), len(data)))
    if not(covariance):
        indice = 0
        if axe == "North":
            indice = 6
        elif axe == "East":
            indice = 5
        else:
            indice = 7

        di = np.diag_indices_from(P)
        P[di] = 1 / data[:, indice] ** 2
    else:
        P=covariance
    return P


def matriceNormaleLigne(A, P):
    """
    Fonction de sous-calcul de la matrice normale pour le traitement ligne par ligne. effectue le produit AtPA sur une ligne de la matrice A.
    :param A: matrice  A
    :param P: Matrice de poids P
    :return: matrice carrée de la longueur de A
    """
    at = A.reshape((len(A), 1))
    A = A.reshape(1, len(A))
    N = np.dot(at, np.dot(P, A))
    return N


def vecteurKligne(A, P, B):
    """
    Fonction de calcul d'un élément du vecteur K . Le calcul est fait par ligne  de manière  à alleger ce dernier.
    :param A: ligne de la matrice A
    :param P: colonne de la matrice P correspondant  à la ligne de A
    :param B:  observation
    :return: matrice composé d'un élément unique
    """
    at = A.reshape((len(A), 1))

    K = at * P * B
    return K




def moindreCarres(data,periode,covariance=False,extend=False,robust=False):
    """
    Renvoie le résultat d'un traitement par moindre carrés d'un jeu de données formaté par la méthode formatage.
    Les parametres d'entrée sont envoyés par la fonction traitement.
    :param data: jeu de données comprenant date série E N U  et écarts type sur ces coordonnées.
    :param covariance: Matrice de covariance supplémentaire dans le cadre de param^tre extérieures  intervnant sur la donnée mesurée
    :param periode: périodes influencant la donnée, celles-ci peuvent etre multiple ( a entrer sous forme de liste)
    :param extend:ajoute la matrice des résidus des calcul au retour de la fonction
    :param robust: si True effectue un traitement des points faux par iterations
    :type data: numpy.array
    :type covariance:numpy.array
    :type periode : list
    """
    t0 = np.mean(data[:, 1])
    resultat = [t0]

    # premier traitement avec un axe, on comence par la creation de matrice
    be = matriceB(data,"East")
    # pour la date de référence, on prend cette dernière au milieu du jeu de données
    a = matriceA(data, t0, periode)
    pe = matriceP(data, "East", covariance)
    #on redéfini les matrices pour les deux autres axes
    bn=matriceB(data,'North')
    bu=matriceB(data,'Up')
    pn=matriceP(data,'North')
    pu=matriceP(data,'Up')
    if robust :
        #on traite  un premier axe une première fois pour initialiser une liste de point faux
        point_faux=moindreCarres_iter(data,a,be,pe,[])[1]
        #on itère jusqu'à ce qu'il n'y ai plus de points faux
        res=moindreCarres_iter(data,a,be,pe,[])[0]
        for i in point_faux:
            res= moindreCarres_iter(data,a,be,pe,point_faux,extend=extend)[0]
        resultat.append(res)

        res=moindreCarres_iter(data,a,bn,pn,point_faux,extend= extend)[0]
        for i in point_faux:
           res= moindreCarres_iter(data,a,bn,pn,point_faux,extend= extend)[0]
        resultat.append(res)

        res=moindreCarres_iter(data,a,bu,pu,point_faux,extend =extend)[0]
        for i in point_faux:
            res= moindreCarres_iter(data,a,bu,pu,point_faux,extend =extend)[0]

        resultat.append(res)

    else:
        res_east=moindreCarres_iter(data,a,be,pe,[],extend=extend)[0]
        res_north=moindreCarres_iter(data,a,bn,pn,[],extend= extend)[0]
        res_up= moindreCarres_iter(data,a,bu,pu,[],extend= extend)[0]
        resultat.append(res_east)
        resultat.append(res_north)
        resultat.append(res_up)
    return resultat