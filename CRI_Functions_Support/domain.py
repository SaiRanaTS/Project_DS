import numpy as np
from matplotlib import pyplot as plt
from math import pi
import math

def domain (Vsogx, corc, Ln):
    if Vsogx == 0:
        Vsog = 0.001
    else:
        Vsog = Vsogx

    # Vsog = 10
    # corc = 90
    # Ln = 100


    #------------------------------------------------------------

    cog = (-corc)
    #print ('the velocity : ', Vsog)
    log_t = math.log10(Vsog)
    #print('log vog : ',log_t)
    kad_Top = 0.3591*math.log10(Vsog) + 0.0952
    #print('Kad top : ',kad_Top)
    kad = 10 ** (0.3591*math.log10(Vsog) + 0.0952)
    kdt = 10 ** (0.5441*math.log10(Vsog) - 0.0795)
    #print('kad : ',kad)
    #print('kdt : ',kdt)
    L = Ln * 0.000539957
    A = 70 * 0.000539957
    B = 30 * 0.000539957
    C = 15 * 0.000539957
    D = 5 * 0.000539957

    #------------------------------------------------------------
    # Rf
    Rf = A + (1.34* (math.sqrt((kad**2)+(0.5*kdt)**2)))*L
    Ra = B + (0.67 * (math.sqrt((kad)**2 + (0.5*kdt)**2)))*L
    Rs = C + (0.2 + kdt)*L
    Rp = D + (0.2 + 0.75*kdt)*L
    #print('Rf : ', Rf)
    #print('Ra : ', Ra)
    #print('Rs : ', Rs)
    #print('Rp : ', Rp)
    D1 = round(0.9 * Rs,3)
    #print ('D1 : ', D1)
    D2 = round(-0.9 * Rp,3)
    #print('D2 : ', D2)
    D3 = round(-0.9 * Ra,3)
    #print('D3 : ', D3)
    D4 = round((0.75*Rf) - (0.25*Ra),3)
    #print('D4 : ', D4)
    D5 = round(1.1* Rf,3)
    #print('D5 : ', D5)
    D = [[D1,D3],
        [D1,D4],
        [0.0,D5],
        [D2,D4],
        [D2,D3]]
    AngM = [[round(math.cos(math.radians(cog)),3),round(math.sin(math.radians(cog)),3)],
            [round(-math.sin(math.radians(cog)),3),round(math.cos(math.radians(cog)),3)]]
    xy = [[0, 0],
          [0, 0],
          [0, 0],
          [0, 0],
          [0, 0]]
    C = (np.dot(D, AngM)) + xy
    #print('C values are :')
    #print(C)
    #C for intersection

    cc = 10 * C

    #coord = [C[0], C[1], C[2], C[3], C[4]]
    #coord.append(coord[0]) #repeat the first point to create a 'closed loop'
    #xs, ys = zip(*coord) #create lists of x and y values
    #sine_degt1 = math.sin(math.radians(corc))
    #cos_degt1 = math.cos(math.radians(corc))
    #z1 = 10 * sine_degt1
    #p1 = 10 * cos_degt1
    #P=plt.quiver(0,0 , z1, p1,scale=100, color = 'red', pivot = 'middle')
    #plt.quiverkey(P,30,4,6, "Target ship",labelpos="E")


    #plt.figure()
    #plt.plot(xs,ys,label='Blocking Area')
    #plt.legend()
    #plt.show()

    C_points = C
    R_Values = [Rf,Ra,Rs,Rp]
    D_Values = [D1,D2,D3,D4,D5]
    return (C_points,R_Values,D_Values,cc)

