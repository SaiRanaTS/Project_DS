import numpy as np
import CRI_Functions_Support.trgs_ang
import CRI_Functions_Support.deci_sup
import CRI_Functions_Support.domain
import CRI_Functions_Support.CRI_FunExe

class ship:
    def __init__(self,TV_X,TV_Y,TV_H,TV_V,OS_X,OS_Y,OS_V,OS_H):
        #Own Ship Data
        self.OS_X = OS_X
        self.OS_Y = OS_Y
        self.OS_V = OS_V
        self.OS_H = OS_H
        #Target Ship Data
        self.TV_X = TV_X
        self.TV_Y = TV_Y
        self.TV_H = TV_H
        self.TV_V = TV_V

    def CRI(self):

        ov_x_N = self.OS_X * 0.000539957
        ov_y_N = self.OS_Y * 0.000539957
        tv_x_N = self.TV_X * 0.000539957
        tv_y_N = self.TV_Y * 0.000539957
        # ---------------------------------CRI Function Module Call ---------------------------------------------------------
        M_fun = (CRI_Functions_Support.CRI_FunExe.CRI_call(self.OS_X, self.TV_V, ov_x_N, ov_y_N, tv_x_N, tv_y_N, self.OS_H,
                                                         self.TV_H))
        self.DCPA = M_fun[0]
        self.CRI_Index = M_fun[1]
        self.TCPA = M_fun[2]
        self.Alp_OT = M_fun[5]
        self.Theta_OT = M_fun[9]
        self.D_BTwn = M_fun[8]

        return (self.DCPA,self.CRI_Index,self.TCPA,self.Alp_OT,self.Theta_OT,self.D_BTwn)







ts1 = ship(364295.0,6922400.0,-110.0,0.13721773531607276,361936.0,6920425.0,3,-113.43)
print(ts1.CRI())





class Ship_data:
    def __init__(self,data,ori):
        self.x = data['Num']
        self.xo = ori['Num']
        self.num = len(self.x)-1
        self.numo = len(self.xo)-1
        self.ang = data['TS2_Ori'][self.xo][self.numo]
        self.gen_x = data['Lo'][self.x][self.num]
        self.gen_y = data['La'][self.x][self.num]
        self.velo = data['Total Speed'][self.x][self.num]

    def back_flow(self):
        return (self.gen_x,self.gen_y,self.ang,self.velo)

