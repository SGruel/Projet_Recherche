from scipy.optimize import least_squares
import numpy as np

def delta(x):
    if x<0:
        return 0
    else:
        return 1

def test_MC(data):
    def fun(x, t, t0, saut, pos):
        T = 365.25
        total_saut = 0
        for i in range(6, 6 + len(saut)):
            total_saut += x[i]*delta(t-saut[i])
        return x[0] + x[1] * (t - t0) + x[2] * np.cos((t - t0) / T) + x[3] * np.sin((t - t0) / T) + x[4] * \
                np.cos(2 * (t - t0) / T) + x[5] * np.sin(2 * (t - t0) / T) + total_saut - pos
    compt = 0
    for i in range(1,len(data)):
        if data[i][0] != data[i-1][0]:
            compt += 1
    x0 = np.ones(6 + compt)
    t = []
    pos = []
    saut = []
    for i in range(len(data)):
        t.append(data[i][1])
        pos.append(data[i][2])
        if i>0 and data[i][0]>data[i-1][0]:
            saut.append(data[i][1])
    t = np.array(t)
    pos = np.array(pos)
    t0 = np.array(len(data) * [t[abs(len(t)/2)]])
    saut = np.array(len(data) * [saut])

    res_robust = least_squares(fun, x0, loss='huber', args=(t, t0, saut, pos))

    return res_robust