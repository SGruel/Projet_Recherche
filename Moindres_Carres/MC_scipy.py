from scipy.optimize import least_squares
import numpy as np

def delta(x):
    """
    Focntion qui gère un flottant ou une liste de flottant et qui renvoit 1 si le nombre est positif, 0 sinon.
    Correspond à une fonction escalier.

    :param x: l'argument de notre fonction escalier
    :type x: float ou liste
    :return: le résultat de la fonction escalier sur l'entrée
    :type return: float ou liste, du même type que l'entrée
    """
    #on différentie le cas ou on traite une liste et le cas ou on traite un nombre
    if type(x) == type(np.array(1)):
        l = []
        for i in x:
            if i<0:
                l.append(0)
            else:
                l.append(1)
        l = np.array(l)
        return l
    else:
        if x<0:
            return 0
        else:
            return 1

def test_MC(data):
    """
    Fonction qui teste un module de moindres carrés robuste de scipy sur nos séries de mesures traité.
    On défini la fonction qui correspond au problème et on l'utilise dans la fonction de moindres carrés robuste.

    :param data: données formatées par notre fonction formatage localisée dans le dossier Traitement
    :type data: np.array (n,8)
    :return: le résultat de la fonction least_squares sur les trois coordonnées
    :type return: liste de 3 return de la fonction least_squares
    """

    def fun(x, t, t0, saut, pos):
        """


        :param x: vecteur des paramètres à estimer
        :param t: vecteur temps
        :param t0: veteur uniforme contenant le temps origine
        :param saut: vecteur temps des différents sauts
        :param pos: vecteur position au temps donné
        :return:
        """
        T = 365.25
        A = np.zeros((len(t), 6+saut.shape[1]))
        for i in range(len(A)):
            A[i][0] = 1
        A[: ,1] = t - t0
        A[: ,2] = np.cos((t - t0) / T)
        A[: ,3] = np.sin((t - t0) / T)
        A[: ,4] = np.cos(2 * (t - t0) / T)
        A[: ,5] = np.sin(2 * (t - t0) / T)
        for i in range(6, A.shape[1]):
            A[: ,i] = delta(t - saut[0][i-6])
        return np.dot(A,x)-pos

    compt = 0
    for i in range(1,len(data)):
        if data[i][0] != data[i-1][0]:
            compt += 1

    x0_E = np.concatenate((np.array([data[0][2], (data[0][2]-data[-1][2])/(data[0][1]-data[-1][1]), 0, 0, 0, 0]), np.array(compt*[0])), axis=0)
    x0_N = np.concatenate((np.array([data[0][3], (data[0][3]-data[-1][3])/(data[0][1]-data[-1][1]), 0, 0, 0, 0]), np.array(compt*[0])), axis=0)
    x0_h = np.concatenate((np.array([data[0][4], (data[0][4]-data[-1][4])/(data[0][1]-data[-1][1]), 0, 0, 0, 0]), np.array(compt*[0])), axis=0)
    t = []
    pos_E = []
    pos_N = []
    pos_h = []
    saut = []
    for i in range(len(data)):
        t.append(data[i][1])
        pos_E.append(data[i][2])
        pos_N.append(data[i][3])
        pos_h.append(data[i][4])
        if i>0 and data[i][0]>data[i-1][0]:
            saut.append(data[i][1])
    t = np.array(t)
    pos_E = np.array(pos_E)
    pos_N = np.array(pos_N)
    pos_h = np.array(pos_h)
    t0 = np.array(len(t) * [np.mean(data[:,1])])
    saut = np.array(len(t) * [saut])

    res_robust_E = least_squares(fun, x0_E, args=(t, t0, saut, pos_E))
    res_robust_N = least_squares(fun, x0_N, args=(t, t0, saut, pos_N))
    res_robust_h = least_squares(fun, x0_h, args=(t, t0, saut, pos_h))

    return [res_robust_E, res_robust_N, res_robust_h]

def test_ls(a, b, c, d):
    """
    Fonction de test de la fonction least_squares sur un polynome du troisième degré

    :return: le résultat de la fonction least_squares
    """
    def squares(x, t, pos):
        return x[0] + x[1]*t + x[2]*t**2 + x[3]*t**3 - pos

    x0 = [a+np.random.random(), b+np.random.random(), c+np.random.random(), d+np.random.random()*0.1]
    t = np.arange(0,100,0.01)
    pos = []
    for i in t:
        pos.append(a + b*i + c*i**2 + d*i**3 + np.random.normal(0,1))
    pos = np.array(pos)

    test = least_squares(squares, x0, loss='huber', args=(t, pos))

    return test

def test_saut_ls(a, b, c, d, e):
    """
    Fonction de test de la fonction least_squares sur un polynome du quatrième degré avec un saut au milieu de la série

    :return: le résultat de la fonction least_squares
    """
    def up(x, t, pos):
        sum = 0
        for i in [2,3,4]:
            sum += x[i]*t**i
        return sum + x[0] + x[1]*t + x[5]*delta(t-500)- pos

    x0 = [a+np.random.random(), b+np.random.random(), c+np.random.random(), d+np.random.random()*0.1, e+np.random.random()*0.01, -1000]
    t = np.arange(0, 1000, 1)
    pos = []
    for i in t:
        pos.append(a + b*i + c*i**2 + d*i**3 + e*i**4 - 1000**delta(i-500) + np.random.random())
    pos = np.array(pos)

    test = least_squares(up, x0, loss='huber', args=(t, pos))
    return test