import numpy as np

def palier(file):
    data= np.genfromtxt(file,delimiter=',',dtype=float)
    data[:, 1:5]=365000*data[:, 1:5]
    i=len(data)-1
    #on travaille sur la coordonnée EST
    while abs(data[i,1]-data[-1,1])<0.6:
        i-=1
    palier=(data[i,1]+data[-1,1])/2
    list_E=[]
    while abs(data[i,1]-palier)<5 :
        list_E.append([data[i,0],data[i,1]-palier])
        i-=1

    #Nord
    while abs(data[i, 3] - data[-1, 3]) < 0.6:
        i -= 1
    palier = (data[i, 3] + data[-1, 3]) / 2
    list_N = []
    while abs(data[i, 1] - palier) < 5:
        list_N.append([data[i, 0], data[i, 3] - palier])
        i -= 1
    #Up
    while abs(data[i, 5] - data[-1, 5]) < 0.2:
        i -= 1
    palier = (data[i,5] + data[-1, 5]) / 2
    list_H = []
    while abs(data[i, 5] - palier) < 5:
        list_H.append([data[i, 0], data[i, 5] - palier])
        i -= 1
    list=[list_E,list_N,list_H]
    return list



