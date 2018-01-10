import numpy as np

def palier(file):
    data= np.genfromtxt(file,delimiter=',',dtype=float)
    data[:, 1:5]=365000*data[:, 1:5]
    i=len(data)-1
    #on travaille sur la coordonnée EST
    while abs(data[i,1]-data[-1,1])<0.6:
        i-=1
    palier=(data[i,1]+data[-1,1])/2
    list_E_pal=[]
    list_E_dat=[]
    while abs(data[i,1]-palier)<5 :
        list_E_pal.append(data[i,1]-palier)
        list_E_dat.append(data[i, 0])
        i-=1

    #Nord
    while abs(data[i, 3] - data[-1, 3]) < 0.6:
        i -= 1
    palier = (data[i, 3] + data[-1, 3]) / 2
    list_N_pal = []
    list_N_dat = []
    while abs(data[i, 1] - palier) < 5:
        list_N_pal.append( data[i, 3] - palier)
        list_N_dat.append(data[i, 0])
        i -= 1
    #Up
    while abs(data[i, 5] - data[-1, 5]) < 0.2:
        i -= 1
    palier = (data[i,5] + data[-1, 5]) / 2
    list_H_pal = []
    list_H_dat=[]
    while abs(data[i, 5] - palier) < 5:
        list_H_pal.append(data[i, 5] - palier)
        list_H_dat.append(data[i, 0])
        i -= 1
    list=[[list_E_dat,list_E_pal],[list_N_dat,list_N_pal],[list_H_dat,list_H_pal]]
    return list



