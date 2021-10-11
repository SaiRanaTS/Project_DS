import math

def trags_calc (Tr_v,Os_v,T_x,T_y,O_x,O_y,Tang,Oang):

    def Inter_Para(O_v, T_v, O_x, O_y, T_x, T_y, O_ang, T_ang):
        vox = round(O_v * math.sin(math.radians(O_ang)), 3)
        voy = round(O_v * math.cos(math.radians(O_ang)), 3)

        vtx = round(T_v * math.sin(math.radians(T_ang)), 3)
        vty = round(T_v * math.cos(math.radians(T_ang)), 3)

        vx = vtx - vox
        vxr = round(vx, 3)
        vy = vty - voy
        vyr = round(vy, 3)

        xot = T_x - O_x
        yot = T_y - O_y
        # print('Xot : ', xot)
        # print('Yot : ',yot)
        result_1 = (vtx, vty, xot, yot)
        return result_1


    calc1 = Inter_Para(Tr_v,Os_v,T_x,T_y,O_x,O_y,Tang,Oang)

    def relative_Cor_TarS(VTx, VTy, Xot, Yot):
        tyu = VTx
        tyv = VTy
        if tyv == 0:
            tyv = 0.000001
        else:
            tyv = VTy
        vx_vy_ratio = tyu / tyv
        Vr_radio_pass = (vx_vy_ratio)

        def comp_fun(vr3):
            if tyu >= 0 and tyv >= 0:
                res = math.atan(vr3)
                # print('Option 1')
                return (res)
            elif tyu < 0 and tyv < 0:
                res = math.atan(vr3) + math.pi
                # print('Option 2')
                return (res)
            elif tyu >= 0 and tyv < 0:
                res = math.atan(vr3) + math.pi
                # print('Option 3')
                return (res)
            elif tyu < 0 and tyv >= 0:
                res = math.atan(vr3) + 2 * (math.pi)
                # print('Option 4')
                return (res)

        re_theta = comp_fun(Vr_radio_pass)

        theta_OT_Deg = ((180 / (math.pi)) * re_theta)
        if theta_OT_Deg < 0:
            theta_OT_Deg = 360 + theta_OT_Deg
        elif theta_OT_Deg >= 360:
            theta_OT_Deg = theta_OT_Deg - 360
        else:
            theta_OT_Deg = theta_OT_Deg

        xyu = Xot
        yyu = Yot
        if Yot == 0:
            yyu = 0.000001
        else:
            yyu = Yot
        # print('xyu = ', xyu)
        # print('yyu = ',yyu)
        xot_yot_ratio = xyu / yyu
        xotratio_deg = xot_yot_ratio

        # print('Real x y  ratio : ',xotratio_deg )

        def true_fun(vr5):
            if xyu >= 0 and yyu >= 0:
                res = float(math.atan(vr5))
                # print('Option 1', res)
                return (res)
            elif xyu < 0 and yyu < 0:
                res = float(math.atan(vr5) + math.pi)
                # print('Option 2')
                return (res)
            elif xyu >= 0 and yyu < 0:
                res = float(math.atan(vr5) + math.pi)
                # print('Option 3')
                return (res)
            elif xyu < 0 and yyu >= 0:
                res = float(math.atan(vr5) + 2 * (math.pi))
                # print('Option 4')
                return (res)

        real_theta = true_fun(xotratio_deg)
        theta_Real_Deg = float(((180 / (math.pi)) * real_theta))
        # if  theta_Real_Deg < 0:
        #     theta_Real_Deg = 360 + theta_Real_Deg
        # elif theta_Real_Deg >= 360:
        #     theta_Real_Deg = theta_Real_Deg - 360
        # else:
        #     theta_Real_Deg = theta_Real_Deg

        # print('Alpha OT F : ',theta_Real_Deg)
        # print('Theta OT F : ', theta_OT_Deg)

        result_2 = (theta_OT_Deg, theta_Real_Deg)
        return result_2

    calc2 = relative_Cor_TarS(calc1[0],calc1[1],calc1[2],calc1[3])

    def Relat_Motion_para(Xo, Yo, Xt, Yt, theta_o, theta_ot, theta_real):
        xd1 = Xo
        yd1 = Yo
        xd2 = Xt
        yd2 = Yt
        Vot_re = 1
        if Vot_re == 0:
            Vot_re = 0.00001
        else:
            Vot_re = 1
        DO = theta_o
        theta_OT_Deg = theta_ot
        theta_Real_Deg = theta_real
        D_Btwn = math.sqrt(((xd2 - xd1) ** 2) + ((yd2 - yd1) ** 2))
        # print('xo : ',xd1)
        # print('xt : ',xd2)
        # print('yo : ',yd1)
        # print('yt : ',yd2)
        # print('D_Between : ', D_Btwn)

        # DCPA and TCPA Calculations
        ang_D = math.sin(math.radians(theta_OT_Deg - theta_Real_Deg - 180))
        DCPA_1 = D_Btwn * ang_D
        DCPA_rnd = round(DCPA_1, 3)
        top_fun = math.cos(math.radians(theta_OT_Deg - theta_Real_Deg - 180))
        TCPA_1 = ((D_Btwn * top_fun) / Vot_re)
        TCPA_rnd = round(TCPA_1, 3)
        # print('alpha t : ', theta_Real_Deg)
        # print('Theat 0 : ', DO)
        sudo_alpha_OT = (theta_o - theta_real)
        alpha_OT = theta_real - theta_o
        if alpha_OT < 0:
            alpha_OT = alpha_OT + 360
        elif alpha_OT > 360:
            alpha_OT = alpha_OT - 360
        else:
            pass
        result_3 = ( alpha_OT )
        return result_3

    calc3 = Relat_Motion_para(T_x,T_y,O_x,O_y,Tang,calc2[0],calc2[1])
    return calc3

