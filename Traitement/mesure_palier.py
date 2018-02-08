import numpy as np
import csv


def palier(file):
    """
    Mesure la différence à la dernière date et l'écrit sur un fichier pour toute les dae
    :param file: fichier de mesure résultant d'un calcul MIDAS ou MC
    :return:
    """
    data = np.genfromtxt(file, delimiter=',', dtype=float)
    data[:, 1:7] = 365000 * data[:, 1:7]
    i = len(data) - 1
    # on travaille sur la coordonnée EST
    e_max = max(data[-1, 1], data[i, 1])
    e_min = min(data[-1, 1], data[i, 1])
    while e_max - e_min < 0.6 and i > 0:
        i -= 1
        if data[i, 1] < e_min:
            e_min = data[i, 1]
        elif data[i, 1] > e_max:
            e_max = data[i, 1]
    palier = (data[i + 1, 1] + data[-1, 1]) / 2
    date_pal_E = data[i + 1, 0]
    list_E_pal = []
    list_E_dat = []

    i = len(data)
    while i > 0:
        i -= 1
        list_E_pal.append(data[i, 1] - palier)
        list_E_dat.append(data[i, 0])

    # Nord
    j = len(data) - 1
    e_max = max(data[-1, 3], data[j, 3])
    e_min = min(data[-1, 3], data[j, 3])
    while e_max - e_min < 0.6 and j > 0:
        j -= 1
        if data[j, 3] < e_min:
            e_min = data[j, 3]
        elif data[j, 1] > e_max:
            e_max = data[j, 3]
    palier = (data[j + 1, 3] + data[-1, 3]) / 2
    date_pal_N = (data[j + 1, 0])
    list_N_pal = []
    list_N_dat = []

    j = len(data)-1
    while j > 0:
        list_N_pal.append(data[j, 3] - palier)
        list_N_dat.append(data[j, 0])
        j -= 1
    # Up
    k = len(data) - 1
    e_max = max(data[-1, 5], data[k, 5])
    e_min = min(data[-1, 5], data[k, 5])
    while e_max - e_min < 0.6 and k > 0:
        k -= 1
        if data[k, 5] < e_min:
            e_min = data[k, 5]
        elif data[k, 5] > e_max:
            e_max = data[k, 5]
    palier = (data[k + 1, 5] + data[-1, 5]) / 2
    date_pal_H = data[k, 0]
    list_H_pal = []
    list_H_dat = []

    k = len(data) - 1
    while k > 0:
        list_H_pal.append(data[k, 5] - palier)
        list_H_dat.append(data[k, 0])
        k -= 1
    list = [[list_E_dat, list_E_pal], [list_N_dat, list_N_pal], [list_H_dat, list_H_pal],
            [date_pal_E, date_pal_N, date_pal_H]]
    if list_E_dat[0]>4000:
        # On écrit dans un csv
        file_name = file[-16:-12]
        file_loc = 'C:\\Users\\simeon\\Documents\\ENSG\\Projets\\Recherche\\Resultatcsv\\ecart_palier\\'
        with open(file_loc + file_name + '.csv', 'w') as file_content:
            file_writer = csv.writer(file_content, delimiter=' ')
            for i in range(len(list_E_pal)-1):
                file_writer.writerow([list_E_dat[i], date_pal_E, list_E_pal[i], date_pal_N, list_N_pal[i], date_pal_H,
                                     list_H_pal[i]])
    return list
