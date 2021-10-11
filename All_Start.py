import matplotlib
import csv
import pandas as pd
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import datetime
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path
from matplotlib.markers import MarkerStyle
from matplotlib import transforms
import CRI_Functions_Support.CRI_FunExe
import math
import shapely
from matplotlib.patches import Circle
import CRI_Functions_Support.trgs_ang
import CRI_Functions_Support.deci_sup
import CRI_Functions_Support.domain



img = plt.imread('Support_images/bpo3.png')
fig, ax = plt.subplots()
fig.set_size_inches(13, 7)
plt.subplots_adjust(left=0.00, right=0.95, top=0.95, bottom=0.05)
ax.imshow(img, extent=[-4122, 6028, -400, 4675], alpha=0.96)
plt.xlim([-4122, 6028])
plt.ylim([-400, 4675])
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.grid(alpha=0.2)

ax.set_title(u"|Real Time DS System|")
ax.legend()

# departure and arrival
x = [0, -24]
y = [0, 4088]
plt.plot(x[0], y[0], c='green', marker='o', markersize=8)
plt.plot(x[1], y[1], c='red', marker='o', markersize=8)

# trajectory data
origin_x = 362024.07992
origin_y = 6918869.62932
ov_x, ov_y = [], []
tv1_x, tv1_y = [], []
tv2_x, tv2_y = [], []
tv3_x, tv3_y = [], []
tv4_x, tv4_y = [], []
tv5_x, tv5_y = [], []
ov_heading, ov_spd, ov_turn = [], [], []
tv1_heading, tv1_spd, tv1_turn = [], [], []
tv2_heading, tv2_spd, tv2_turn = [], [], []
tv3_heading, tv3_spd, tv3_turn = [], [], []
tv4_heading, tv4_spd, tv4_turn = [], [], []
tv5_heading, tv5_spd, tv5_turn = [], [], []
ln_ov, = ax.plot([], [], 'g-', animated=False, alpha=0.3)
ln_tv1, = ax.plot([], [], 'r-', animated=False, alpha=0.15)
ln_tv2, = ax.plot([], [], 'orange', animated=False, alpha=0.15)
ln_tv3, = ax.plot([], [], 'c', animated=False, alpha=0.15)
ln_tv4, = ax.plot([], [], 'blue', animated=False, alpha=0.15)
ln_tv5, = ax.plot([], [], 'yellow', animated=False, alpha=0.15)

# time_template = 'time: %.2fs'
# time = []
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white')


class RotatedRect:
    def __init__(self, cx, cy, p1, p2, p3, p4, p5, angle):
        self.cx = cx
        self.cy = cy
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.angle = angle

    def get_contour(self):
        p1 = self.p1
        p2 = self.p2
        p3 = self.p3
        p4 = self.p4
        p5 = self.p5
        # h = self.h
        c = shapely.geometry.Polygon([p1, p2, p3, p4, p5])
        # c = shapely.geometry.Polygon([(d11, d12), (d21, d22), (d31, d32),(d41,d42),(d51,d52)])
        rc = shapely.affinity.rotate(c, self.angle)
        return shapely.affinity.translate(rc, self.cx, self.cy)

    def intersection(self, other):
        return self.get_contour().intersection(other.get_contour())


def str2float(s):
    def str2num(s):
        return {str(x): x for x in range(10)}[s]

    l = s.split('.')
    s = s.replace('.', '')
    num = reduce(lambda a, b: a * 10 + b, map(str2num, s))
    return num / (10 ** len(l[-1])) if len(l) == 2 else num / 1


# CPA and CRI Function
def cpa(ov_spd, ov_heading, ov_x, ov_y, tv_spd, tv_heading, tv_x, tv_y):
    distance_ov_tv_x = round(tv_x - ov_x, 3)
    distance_ov_tv_y = round(tv_y - ov_y, 3)
    distance_ov_tv = round((distance_ov_tv_x ** 2 + distance_ov_tv_y ** 2) ** 0.5, 3)
    ov_spd_x = round(ov_spd * np.sin(np.deg2rad(ov_heading)), 3)
    ov_spd_y = round(ov_spd * np.cos(np.deg2rad(ov_heading)), 3)
    tv_spd_x = round(tv_spd * np.sin(np.deg2rad(tv_heading)), 3)
    tv_spd_y = round(tv_spd * np.cos(np.deg2rad(tv_heading)), 3)
    spd_rltv_x = round(tv_spd_x - ov_spd_x, 3)
    spd_rltv_y = round(tv_spd_y - ov_spd_y, 3)
    spd_rltv = round((spd_rltv_x ** 2 + spd_rltv_y ** 2) ** 0.5, 3)
    dcpa = round(distance_ov_tv * (spd_rltv_x / spd_rltv * distance_ov_tv_y /
                                   distance_ov_tv - spd_rltv_y / spd_rltv * distance_ov_tv_x / distance_ov_tv), 3)
    tcpa = round(distance_ov_tv * (spd_rltv_x / spd_rltv * distance_ov_tv_x / distance_ov_tv +
                                   spd_rltv_y / spd_rltv * distance_ov_tv_y / distance_ov_tv) / spd_rltv, 3)
    cpa_x = round(ov_x + (-tcpa) * ov_spd_x, 3)
    cpa_y = round(ov_y + (-tcpa) * ov_spd_y, 3)
    cpa = [cpa_x, cpa_y]

    ov_x_N = ov_x * 0.000539957
    ov_y_N = ov_y * 0.000539957
    tv_x_N = tv_x * 0.000539957
    tv_y_N = tv_y * 0.000539957
    # ---------------------------------CRI Function Module Call ---------------------------------------------------------
    Dc1 = (CRI_Functions_Support.CRI_FunExe.CRI_call(ov_spd, tv_spd, ov_x_N, ov_y_N, tv_x_N, tv_y_N, ov_heading, tv_heading))

    timm = 0
    pck = (
    Dc1[0], Dc1[2], cpa, 0.9 * Dc1[1], Dc1[3], Dc1[4], timm, ov_spd, tv_spd, dcpa, tcpa, Dc1[5], Dc1[6], Dc1[7], Dc1[8],
    Dc1[9], Dc1[10], Dc1[11], Dc1[12], Dc1[13], Dc1[14], Dc1[15], Dc1[16], Dc1[17], Dc1[18], Dc1[19], Dc1[20], Dc1[21],
    Dc1[22], Dc1[23], Dc1[23])
    return pck


# Vessel Color Function
def vsl_colr(crix):
    if crix <= 0.1:
        cl = 'midnightblue'
        return cl
    elif crix > 0.1 and crix <= 0.17:
        cl = 'blue'
        return cl
    elif crix > 0.17 and crix <= 0.25:
        cl = 'mediumblue'
        return cl
    elif crix > 0.25 and crix <= 0.6:
        cl = 'green'
        return cl
    elif crix > 0.6 and crix <= 0.7:
        cl = 'yellowgreen'
        return cl
    elif crix > 0.7 and crix <= 0.85:
        cl = 'red'
        return cl
    else:
        cl = 'yellow'
        return cl


def Vsl_Typ():
    t1 = 1
    t2 = 2
    t3 = 3
    t4 = 4
    t5 = 4
    return (t1, t2, t3, t4, t5)

tr1vx =[0]
tr1vy =[0]

y89 = [0]

fieldnames = ["Time", "TS1_CRIW", "TS2_CRIW", "TS3_CRIW", "TS4_CRIW", "TS5_CRIW"]

with open('Data_Generated/CRI.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

fieldnames1 = ["Time","T1_Alpha_OT", "T1_Distance", "T1_Speed", "T2_Alpha_OT", "T2_Distance", "T2_Speed","T3_Alpha_OT", "T3_Distance", "T3_Speed","T4_Alpha_OT", "T4_Distance", "T4_Speed","T5_Alpha_OT", "T5_Distance", "T5_Speed"]

with open('Data_Generated/Radar.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
    csv_writer.writeheader()

nx = 0
nx2 = 0
nx3 = 0
nx4 = 0
nx5 = 0

def update(frame):
    now = datetime.datetime.now()

    global nx
    global nx2
    global nx3
    global nx4
    global nx5
    n = 0
    # Ship Marker Shape:
    def_marker = Path([[-0.005, -0.02], [0.005, -0.02], [0.005, 0.01], [0, 0.02], [-0.005, 0.01], [0, 0], ],
                      [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    # -----------------------------------------------------------------------------------------------------------------#

    data0 = pd.read_csv('Data_Collected/OS_Data.csv')
    x00 = data0['Num']
    numberiii = len(x00)-1
    dataori = pd.read_csv('Data_Collected/ori/OriOS.csv')
    xo00 = dataori['Num']
    numberiiio = len(xo00)-1
    OSgen_ang = dataori['Own_Ori'][xo00][numberiiio]
    OSgen_x = data0['Lo'][x00][numberiii]
    OSgen_y = data0['La'][x00][numberiii]
    OSgen_Velo = data0['Total Speed'][x00][numberiii]
    ov_x.append(OSgen_x - origin_x)
    ov_y.append(OSgen_y - origin_y)
    ov_heading.append(OSgen_ang)
    #ov_spd.append(str2float(ov_data.row_values(frame)[5]) * 0.51444)
    ov_spd.append(OSgen_Velo)
    ov_mk_rtt = transforms.Affine2D().rotate_deg(-ov_heading[-1])
    # Fancy Compass Shape:
    def_marker_comp = Path([[-0.005, -0.02], [0.005, -0.02], [0.005, 0.01], [0, 0.02], [-0.005, 0.01], [0, 0], ],
                           [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    com_mkr = def_marker_comp.transformed(ov_mk_rtt)
    plt_ov_mk_com = ax.scatter(2500, 518, marker=com_mkr, color='white', s=15 ** 3, alpha=0.9)
    # ------------------------------------------------------------------------------------------------------------------#

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- OWN SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    ownship_ln = 100  # Length of Own Ship
    plt_ov_txt = plt.text(ov_x[-1] + 100, ov_y[-1], f'OS : Gunnerus', fontsize=10, color='white')
    #data = pd.read_csv('data.csv')
    data1 = pd.read_csv('Data_Collected/TS1_Data.csv')
    x11 = data1['Num']
    numberiii = len(x11)-1
    ts1gen_x = data1['Lo'][x11][numberiii]
    ts1gen_y = data1['La'][x11][numberiii]
    ts1gen_Velo= data1['Total Speed'][x11][numberiii]
    tr1vx.append(ts1gen_x)
    tr1vy.append(ts1gen_y)
    tv1_x.append(ts1gen_x - origin_x)
    tv1_y.append(ts1gen_y - origin_y)
    dataoriTS1 = pd.read_csv('Data_Collected/ori/OriTS1.csv')
    xo11 = dataoriTS1['Num']
    numberiiiTS1 = len(xo11)-1
    ts1gen_ang = dataoriTS1['TS1_Ori'][xo11][numberiiiTS1]
    tv1_heading.append(ts1gen_ang)
    tv1_spd.append(ts1gen_Velo)
    tv1_mk_rtt = transforms.Affine2D().rotate_deg(-tv1_heading[-1])
    pk1 = cpa(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv1_spd[-1], tv1_heading[-1], tv1_x[-1], tv1_y[-1])

    # ETA Calculation :  ----------------------------------------------------------------------------------------------
    dx = 0
    dy = 4088
    dinside = (dx - ov_x[-1]) ** 2 + (dy - ov_y[-1]) ** 2
    dtravlled = 2.207343 - ((math.sqrt(dinside) * 0.000539957))
    d2t = math.sqrt(dinside)
    if ov_spd[-1] == 0:
        spd_ow = 0.001
    else:
        spd_ow = ov_spd[-1]

    eta = round((d2t / spd_ow) / 60, 2)
    # -------------------------------------------------------------------------------------------------------------------

    dcpa_tv1 = pk1[0]
    tcpa_tv1 = pk1[1]
    cpa_tv1 = pk1[2]
    CRI_tv1 = pk1[3]
    own_speed = pk1[7]
    t1_sp = pk1[8]
    skl_T1 = (4 * t1_sp)
    skl = (5 * own_speed)
    alp_ot1 = pk1[11]
    Dbtwn1 = pk1[14]
    new_dcpa_chk = pk1[21]
    osvv1 = pk1[22]
    tsvv1 = pk1[23]
    osan1 = pk1[24]
    tsan1 = pk1[25]
    mkrc1 = vsl_colr(CRI_tv1)

    # -------------------------------------- Domain Implementation-------------------------------------------------------

    # Domain Function Call
    domain_termOS = CRI_Functions_Support.domain.domain(osvv1, osan1, ownship_ln)
    domain_all_pointsOS = domain_termOS[2]
    # Domain Parameters from Function
    OD1 = abs(domain_all_pointsOS[0])
    OD2 = abs(domain_all_pointsOS[1])
    OD3 = abs(domain_all_pointsOS[2])
    OD4 = abs(domain_all_pointsOS[3])
    OD5 = abs(domain_all_pointsOS[4])
    ov_mk = def_marker.transformed(ov_mk_rtt)
    plt_ov_mk = ax.scatter(ov_x[-1], ov_y[-1], marker=ov_mk, color='white', s=15 ** 2, alpha=0.5)

    def_Domaino = Path([[-OD2/2, -OD3], [OD1/2, -OD3], [OD1, OD4], [0, OD5], [-OD2, OD4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    # Domain Draw
    ov_dom = def_Domaino.transformed(ov_mk_rtt)
    plt_ov_dom = ax.scatter(ov_x[-1], ov_y[-1], marker=ov_dom, facecolors='none', edgecolors='white', s=1852, alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------

    circle0 = Circle([2, 2], 2)
    cir_path0 = circle0.get_path()
    t0_crk = cir_path0.transformed(ov_mk_rtt)

    plt_t0_cir = ax.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='g', s=skl ** 2.7,
                            alpha=0.7)
    plt_t00_cir = ax.scatter(ov_x[-1], ov_y[-1], marker=t0_crk, facecolors='none', edgecolors='white', s=skl ** 3.0,
                             alpha=0.4, linestyle='dashed')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- T1 SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Ts1_ln = 100  # Length of TS 1
    tv1_mk = def_marker.transformed(tv1_mk_rtt)
    plt_tv1_mk = ax.scatter(tv1_x[-1], tv1_y[-1], marker=tv1_mk, color=mkrc1, s=15 ** 2, alpha=0.5)
    # -------------------------------------- Decision Support Function Call---------------------------------------------
    T_alot = CRI_Functions_Support.trgs_ang.trags_calc(tv1_spd[-1], ov_spd[-1], tv1_x[-1], tv1_y[-1], ov_x[-1], ov_y[-1], tv1_heading[-1],
                                 ov_heading[-1])
    dec1 = CRI_Functions_Support.deci_sup.dec_sup(T_alot, Dbtwn1, CRI_tv1, alp_ot1, tv1_heading[-1])
    # -------------------------------------- Domain Implementation-------------------------------------------------------
    domain_termTS1 = CRI_Functions_Support.domain.domain(tsvv1, tsan1, Ts1_ln)
    domain_all_pointsTS1 = domain_termTS1[2]

    TS1D1 = abs(domain_all_pointsTS1[0])
    TS1D2 = abs(domain_all_pointsTS1[1])
    TS1D3 = abs(domain_all_pointsTS1[2])
    TS1D4 = abs(domain_all_pointsTS1[3])
    TS1D5 = abs(domain_all_pointsTS1[4])

    def_Domain1 = Path([[-TS1D2/2, -TS1D3], [TS1D1/2, -TS1D3], [TS1D1, TS1D4], [0, TS1D5], [-TS1D2, TS1D4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    t1_dom = def_Domain1.transformed(tv1_mk_rtt)
    plt_t1_dom = ax.scatter(tv1_x[-1], tv1_y[-1], marker=t1_dom, facecolors='none', edgecolors='white', s=1852,
                            alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------

    circle1 = Circle([2, 2], 2)
    cir_path1 = circle1.get_path()
    t1_crk = cir_path1.transformed(tv1_mk_rtt)
    plt_t1_cir = ax.scatter(tv1_x[-1], tv1_y[-1], marker=t1_crk, facecolors='none', edgecolors='r', s=skl_T1 ** 3.2,
                            alpha=0.26, linestyle='dashed')

    # --------------------------------------------------- Vessel Plot ---------------------------------------------------
    plt_tv1_cpa = ax.scatter(cpa_tv1[0], cpa_tv1[1], marker='^', color='blue', s=0)
    plt_tv1_txt = plt.text(tv1_x[-1] + 100, tv1_y[-1],f'T1: PSV_UT754WP \n CRI = {round(CRI_tv1, 3)}\nDCPA = {round(dcpa_tv1, 1)}m \nDCPA chk = {round(new_dcpa_chk, 1)}m\n TCPA = {-round(tcpa_tv1, 3)}s ',fontsize=10, color='white')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- T2 SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Ts2_ln = 100  # Length of TS 2
    data2 = pd.read_csv('Data_Collected/TS2_Data.csv')
    x22 = data2['Num']
    numberiii = len(x22)-1
    dataoriTS2 = pd.read_csv('Data_Collected/ori/OriTS2.csv')
    xo22 = dataoriTS2['Num']
    numberiiiTS2 = len(xo22)-1
    ts2gen_ang = dataoriTS2['TS2_Ori'][xo22][numberiiiTS2]
    ts2gen_x = data2['Lo'][x22][numberiii]
    ts2gen_y = data2['La'][x22][numberiii]
    ts2gen_Velo = data2['Total Speed'][x22][numberiii]
    tv2_x.append(ts2gen_x - origin_x)
    tv2_y.append(ts2gen_y - origin_y)
    tv2_heading.append(ts2gen_ang)
    tv2_spd.append(ts2gen_Velo)
    tv2_mk_rtt = transforms.Affine2D().rotate_deg(-tv2_heading[-1])
    tv2_mk = def_marker.transformed(tv2_mk_rtt)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ CRI Function Calling\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    pk2 = cpa(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv2_spd[-1], tv2_heading[-1], tv2_x[-1], tv2_y[-1])

    dcpa_tv2 = pk2[0]
    tcpa_tv2 = pk2[1]
    cpa_tv2 = pk2[2]
    CRI_tv2 = pk2[3]
    t2_sp = pk2[8]
    skl_T2 = (4 * t2_sp)
    alp_ot2 = pk2[11]
    Dbtwn2 = pk2[14]
    mkrc2 = vsl_colr(CRI_tv2)
    tsvv2 = pk2[23]
    tsan2 = pk2[25]

    # -------------------------------------- Decision Support Function Call---------------------------------------------
    T_alot2 = CRI_Functions_Support.trgs_ang.trags_calc(tv2_spd[-1], ov_spd[-1], tv2_x[-1], tv2_y[-1], ov_x[-1], ov_y[-1], tv2_heading[-1],
                                  ov_heading[-1])
    dec2 = CRI_Functions_Support.deci_sup.dec_sup(T_alot2, Dbtwn2, CRI_tv2, alp_ot2, tv2_heading[-1])

    # --------------------------------------------- Vessel Plot --------------------------------------------------------
    plt_tv2_mk = ax.scatter(tv2_x[-1], tv2_y[-1], marker=tv2_mk, color=mkrc2, s=15 ** 2, alpha=0.5)
    plt_tv2_cpa = ax.scatter(cpa_tv2[0], cpa_tv2[1], marker='^', color='orange', s=0)
    plt_tv2_txt = plt.text(tv2_x[-1] + 100, tv2_y[-1],
                           f'T2: PSV_UT751E \n CRI = {round(CRI_tv2, 3)}\nDCPA = {round(dcpa_tv2, 1)}m,\n TCPA = {-round(tcpa_tv2, 3)}s ',
                           fontsize=10, color='white')

    # --------------------------------------------- Domain Implementation-----------------------------------------------
    domain_termTS2 = CRI_Functions_Support.domain.domain(tsvv2, tsan2, Ts2_ln)
    domain_all_pointsTS2 = domain_termTS2[2]

    TS2D1 = abs(domain_all_pointsTS2[0])
    TS2D2 = abs(domain_all_pointsTS2[1])
    TS2D3 = abs(domain_all_pointsTS2[2])
    TS2D4 = abs(domain_all_pointsTS2[3])
    TS2D5 = abs(domain_all_pointsTS2[4])

    def_Domain2 = Path([[-TS2D2/2, -TS2D3], [TS2D1/2, -TS2D3], [TS2D1, TS2D4], [0, TS2D5], [-TS2D2, TS2D4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    t2_dom = def_Domain2.transformed(tv2_mk_rtt)

    plt_t2_dom = ax.scatter(tv2_x[-1], tv2_y[-1], marker=t2_dom, facecolors='none', edgecolors='white', s=1850,
                            alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------

    circle2 = Circle([2, 2], 2)
    cir_path2 = circle2.get_path()

    t2_crk = cir_path2.transformed(tv2_mk_rtt)
    plt_t2_cir = ax.scatter(tv2_x[-1], tv2_y[-1], marker=t2_crk, facecolors='none', edgecolors='orange',
                            s=skl_T2 ** 3.2, alpha=0.1, linestyle='dashed')

    ####################################################################################################################

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- T3 SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Ts3_ln = 100
    data3 = pd.read_csv('Data_Collected/TS3_Data.csv')
    x33 = data3['Num']
    numberiii = len(x33)-1
    dataoriTS3 = pd.read_csv('Data_Collected/ori/OriTS3.csv')
    xo33 = dataoriTS3['Num']
    numberiiiTS3 = len(xo33)-1
    ts3gen_ang = dataoriTS3['TS3_Ori'][xo33][numberiiiTS3]
    ts3gen_x = data3['Lo'][x33][numberiii]
    ts3gen_y = data3['La'][x33][numberiii]
    ts3gen_Velo = data3['Total Speed'][x33][numberiii]
    tv3_x.append(ts3gen_x - origin_x)
    tv3_y.append(ts3gen_y - origin_y)
    tv3_heading.append(ts3gen_ang)
    tv3_spd.append(ts3gen_Velo)
    tv3_mk_rtt = transforms.Affine2D().rotate_deg(-tv3_heading[-1])
    tv3_mk = def_marker.transformed(tv3_mk_rtt)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ CRI Function Calling\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    pk3 = cpa(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv3_spd[-1], tv3_heading[-1], tv3_x[-1], tv3_y[-1])

    dcpa_tv3 = pk3[0]
    tcpa_tv3 = pk3[1]
    cpa_tv3 = pk3[2]
    CRI_tv3 = pk3[3]
    t3_sp = pk3[8]
    skl_T3 = (4 * t3_sp)
    alp_ot3 = pk3[11]
    Dbtwn3 = pk3[14]
    mkrc3 = vsl_colr(CRI_tv3)
    tsvv3 = pk3[23]
    tsan3 = pk3[25]

    # -------------------------------------- Decision Support Function Call---------------------------------------------
    T_alot3 = CRI_Functions_Support.trgs_ang.trags_calc(tv3_spd[-1], ov_spd[-1], tv3_x[-1], tv3_y[-1], ov_x[-1], ov_y[-1], tv3_heading[-1],
                                  ov_heading[-1])
    dec3 = CRI_Functions_Support.deci_sup.dec_sup(T_alot3, Dbtwn3, CRI_tv3, alp_ot3, tv3_heading[-1])

    # --------------------------------------------- Vessel Plot --------------------------------------------------------
    plt_tv3_mk = ax.scatter(tv3_x[-1], tv3_y[-1], marker=tv3_mk, color=mkrc3, s=15 ** 2, alpha=0.5)
    plt_tv3_cpa = ax.scatter(cpa_tv3[0], cpa_tv3[1], marker='^', color='c', s=0)
    plt_tv3_txt = plt.text(tv3_x[-1] + 100, tv3_y[-1],
                           f'T3: PSV_3300CD \n CRI = {round(CRI_tv3, 3)}\nDCPA = {round(dcpa_tv3, 1)}m,\n TCPA = {-round(tcpa_tv3, 3)}s ',
                           fontsize=10, color='white')

    # -------------------------------------- Domain Implementation-------------------------------------------------------
    domain_termTS3 = CRI_Functions_Support.domain.domain(tsvv3, tsan3, Ts3_ln)
    domain_all_pointsTS3 = domain_termTS3[2]

    TS3D1 = abs(domain_all_pointsTS3[0])
    TS3D2 = abs(domain_all_pointsTS3[1])
    TS3D3 = abs(domain_all_pointsTS3[2])
    TS3D4 = abs(domain_all_pointsTS3[3])
    TS3D5 = abs(domain_all_pointsTS3[4])

    def_Domain3 = Path([[-TS3D2/2, -TS3D3], [TS3D1/2, -TS3D3], [TS3D1, TS3D4], [0, TS3D5], [-TS3D2, TS3D4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    t3_dom = def_Domain3.transformed(tv3_mk_rtt)
    plt_t3_dom = ax.scatter(tv3_x[-1], tv3_y[-1], marker=t3_dom, facecolors='none', edgecolors='white', s=1850,
                            alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------

    circle3 = Circle([2, 2], 2)
    cir_path3 = circle3.get_path()

    t3_crk = cir_path3.transformed(tv3_mk_rtt)
    plt_t3_cir = ax.scatter(tv3_x[-1], tv3_y[-1], marker=t3_crk, facecolors='none', edgecolors='c', s=skl_T3 ** 3.2,
                            alpha=0.1, linestyle='dashed')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- T4 SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Ts4_ln = 100

    data4 = pd.read_csv('Data_Collected/TS4_Data.csv')
    x44 = data4['Num']
    numberiii = len(x44)-1

    dataoriTS4 = pd.read_csv('Data_Collected/ori/OriTS4.csv')
    xo44 = dataoriTS4['Num']
    numberiiiTS4 = len(xo44)-1

    ts4gen_ang = dataoriTS4['TS4_Ori'][xo44][numberiiiTS4]


    ts4gen_x = data4['Lo'][x44][numberiii]
    print(ts4gen_x)
    ts4gen_y = data4['La'][x44][numberiii]
    ts4gen_Velo = data4['Total Speed'][x44][numberiii]
    tv4_x.append(ts4gen_x - origin_x)
    tv4_y.append(ts4gen_y - origin_y)
    tv4_heading.append(ts4gen_ang)
    tv4_spd.append(ts4gen_Velo)
    tv4_mk_rtt = transforms.Affine2D().rotate_deg(-tv4_heading[-1])
    tv4_mk = def_marker.transformed(tv4_mk_rtt)

    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ CRI Function Calling\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    pk4 = cpa(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv4_spd[-1], tv4_heading[-1], tv4_x[-1], tv4_y[-1])

    dcpa_tv4 = pk4[0]
    tcpa_tv4 = pk4[1]
    cpa_tv4 = pk4[2]
    CRI_tv4 = pk4[3]
    t4_sp = pk4[8]
    skl_T4 = (4 * t4_sp)
    alp_ot4 = pk4[11]
    mkrc4 = vsl_colr(CRI_tv4)
    Dbtwn4 = pk4[14]
    tsvv4 = pk4[23]
    tsan4 = pk4[25]

    # -------------------------------------- Decision Support Function Call---------------------------------------------
    T_alot4 = CRI_Functions_Support.trgs_ang.trags_calc(tv4_spd[-1], ov_spd[-1], tv4_x[-1], tv4_y[-1], ov_x[-1], ov_y[-1], tv4_heading[-1],
                                  ov_heading[-1])
    dec4 = CRI_Functions_Support.deci_sup.dec_sup(T_alot4, Dbtwn4, CRI_tv4, alp_ot4, tv4_heading[-1])

    # --------------------------------------------- Vessel Plot --------------------------------------------------------
    plt_tv4_mk = ax.scatter(tv4_x[-1], tv4_y[-1], marker=tv4_mk, color=mkrc4, s=15 ** 2, alpha=0.5)
    # plt_tv4_txt = plt.text(tv4_x[-1] + 100, tv4_y[-1], f'T4: Frigat 1\n DCPA = {round(dcpa_tv4, 1)}m,\n TCPA = {-round(tcpa_tv4, 3)}s,\n CRI = {round(CRI_tv4, 3)},\n Real DCPA = {round(real_dcpa4, 3)},\n Real TCPA = {round(real_tpca4, 3)}',fontsize=10, color='white')
    # plt_tv4_txt = plt.text(tv4_x[-1] + 100, tv4_y[-1],f'T4: Frigat 1\n DCPA = {round(dcpa_tv4, 1)}NM,\n TCPA = {-round(tcpa_tv4, 3)}s,\n CRI = {round(CRI_tv4, 3)},\n Alpha OT = {round(alp_ot4, 3)}',fontsize=10, color='white')
    plt_tv4_cpa = ax.scatter(cpa_tv4[0], cpa_tv4[1], marker='^', color='blue', s=0)
    plt_tv4_txt = plt.text(tv4_x[-1] + 100, tv4_y[-1],
                           f'T4: PX105_RMY \n CRI = {round(CRI_tv4, 3)}\nDCPA = {round(dcpa_tv4, 1)}m,\n TCPA = {-round(tcpa_tv4, 3)}s ',
                           fontsize=10, color='white')

    # ------------------------------------------ Domain Implementation---------------------------------------------------
    domain_termTS4 = CRI_Functions_Support.domain.domain(tsvv4, tsan4, Ts4_ln)
    domain_all_pointsTS4 = domain_termTS4[2]

    TS4D1 = abs(domain_all_pointsTS4[0])
    TS4D2 = abs(domain_all_pointsTS4[1])
    TS4D3 = abs(domain_all_pointsTS4[2])
    TS4D4 = abs(domain_all_pointsTS4[3])
    TS4D5 = abs(domain_all_pointsTS4[4])

    def_Domain4 = Path([[-TS4D2/2, -TS4D3], [TS4D1/2, -TS4D3], [TS4D1, TS4D4], [0, TS4D5], [-TS4D2, TS4D4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])

    t4_dom = def_Domain4.transformed(tv4_mk_rtt)
    plt_t4_dom = ax.scatter(tv4_x[-1], tv4_y[-1], marker=t4_dom, facecolors='none', edgecolors='white', s=1850,
                            alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------

    circle4 = Circle([2, 2], 2)
    cir_path4 = circle4.get_path()
    t4_crk = cir_path4.transformed(tv4_mk_rtt)
    plt_t4_cir = ax.scatter(tv4_x[-1], tv4_y[-1], marker=t4_crk, facecolors='none', edgecolors='blue', s=skl_T4 ** 3.2,
                            alpha=0.1, linestyle='dashed')

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ---------------------------------------------------- T5 SHIP -----------------------------------------------------
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Ts5_ln = 100

    data5 = pd.read_csv('Data_Collected/TS5_Data.csv')
    x55 = data5['Num']
    numberiii = len(x55)-1


    dataoriTS5 = pd.read_csv('Data_Collected/ori/OriTS5.csv')
    xo55 = dataoriTS5['Num']
    numberiiiTS5 = len(xo55)-1

    ts5gen_ang = dataoriTS5['TS5_Ori'][xo55][numberiiiTS5]

    ts5gen_x = data5['Lo'][x55][numberiii]
    ts5gen_y = data5['La'][x55][numberiii]
    ts5gen_Velo = data5['Total Speed'][x55][numberiii]
    tv5_x.append(ts5gen_x - origin_x)
    tv5_y.append(ts5gen_y - origin_y)
    tv5_heading.append(ts5gen_ang)
    tv5_spd.append(ts5gen_Velo)
    tv5_mk_rtt = transforms.Affine2D().rotate_deg(-tv5_heading[-1])
    tv5_mk = def_marker.transformed(tv5_mk_rtt)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ CRI Function Calling\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    pk5 = cpa(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv5_spd[-1], tv5_heading[-1], tv5_x[-1], tv5_y[-1])

    dcpa_tv5 = pk5[0]
    tcpa_tv5 = pk5[1]
    cpa_tv5 = pk5[2]
    CRI_tv5 = pk5[3]
    t5_sp = pk5[8]
    skl_T5 = (4 * t5_sp)
    alp_ot5 = pk5[11]
    Dbtwn5 = pk5[14]
    mkrc5 = vsl_colr(CRI_tv5)
    tsvv5 = pk5[23]
    tsan5 = pk5[25]

    # -------------------------------------- Decision Support Function Call---------------------------------------------
    T_alot5 = CRI_Functions_Support.trgs_ang.trags_calc(tv5_spd[-1], ov_spd[-1], tv5_x[-1], tv4_y[-1], ov_x[-1], ov_y[-1], tv5_heading[-1],
                                  ov_heading[-1])
    dec5 = CRI_Functions_Support.deci_sup.dec_sup(T_alot5, Dbtwn5, CRI_tv4, alp_ot5, tv5_heading[-1])

    # --------------------------------------------- Vessel Plot --------------------------------------------------------
    plt_tv5_mk = ax.scatter(tv5_x[-1], tv5_y[-1], marker=tv5_mk, color=mkrc5, s=15 ** 2, alpha=0.5)
    # plt_tv5_txt = plt.text(tv5_x[-1] + 100, tv5_y[-1],f'T5: Frigat 2\nDCPA = {round(dcpa_tv5, 1)}m,\n TCPA = {-round(tcpa_tv5, 3)}s,\n CRI = {round(CRI_tv5, 3)},\n Real DCPA = {round(real_dcpa5, 3)},\n Real TCPA = {round(real_tpca5, 3)}',fontsize=10, color='white')
    # plt_tv5_txt = plt.text(tv5_x[-1] + 100, tv5_y[-1],f'T5: Frigat 2\nDCPA = {round(dcpa_tv5, 1)}NM,\n TCPA = {-round(tcpa_tv5, 3)}s,\n CRI = {round(CRI_tv5, 3)},\n Alpha OT = {round(alp_ot5, 3)}',fontsize=10, color='white')
    plt_tv5_cpa = ax.scatter(cpa_tv5[0], cpa_tv5[1], marker='^', color='yellow', s=0)
    plt_tv5_txt = plt.text(tv5_x[-1] + 100, tv5_y[-1],
                           f'T5: PSV_UT776CD \n CRI = {round(CRI_tv5, 3)}\nDCPA = {round(dcpa_tv5, 1)}m,\n TCPA = {-round(tcpa_tv5, 3)}s ',
                           fontsize=10, color='white')

    # -------------------------------------- Domain Implementation-------------------------------------------------------
    domain_termTS5 = CRI_Functions_Support.domain.domain(tsvv5, tsan5, Ts5_ln)
    domain_all_pointsTS5 = domain_termTS5[2]

    TS5D1 = abs(domain_all_pointsTS5[0])
    TS5D2 = abs(domain_all_pointsTS5[1])
    TS5D3 = abs(domain_all_pointsTS5[2])
    TS5D4 = abs(domain_all_pointsTS5[3])
    TS5D5 = abs(domain_all_pointsTS5[4])

    def_Domain5 = Path([[-TS5D2/2, -TS5D3], [TS5D1/2, -TS5D3], [TS5D1, TS5D4], [0, TS5D5], [-TS5D2, TS5D4], [0, 0]],
                       [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    t5_dom = def_Domain5.transformed(tv5_mk_rtt)
    plt_t5_dom = ax.scatter(tv5_x[-1], tv5_y[-1], marker=t5_dom, facecolors='none', edgecolors='white', s=1850,
                            alpha=0.3)

    # --------------------------------------------- CAZ Implementation--------------------------------------------------
    circle5 = Circle([2, 2], 2)
    cir_path5 = circle5.get_path()
    t5_crk = cir_path5.transformed(tv5_mk_rtt)
    plt_t5_cir = ax.scatter(tv5_x[-1], tv5_y[-1], marker=t5_crk, facecolors='none', edgecolors='yellow',
                            s=skl_T5 ** 3.2,
                            alpha=0.1, linestyle='dashed')

    # -/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-



    with open('Data_Generated/CRI.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)

        info = {
            "Time": frame,
            "TS1_CRIW": round(CRI_tv1,3),
            "TS2_CRIW": round(CRI_tv2,3),
            "TS3_CRIW": round(CRI_tv3,3),
            "TS4_CRIW": round(CRI_tv4,3),
            "TS5_CRIW": round(CRI_tv5,3),



        }
        csv_writer.writerow(info)

    with open('Data_Generated/Radar.csv','a') as csv_file:
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames1)

        info = {
            "Time": frame,
            "T1_Alpha_OT": round(alp_ot1,3),
            "T1_Distance": round(Dbtwn1,3),
            "T1_Speed": round(tv1_spd[-1],3),
            "T2_Alpha_OT": round(alp_ot2,3),
            "T2_Distance": round(Dbtwn2,3),
            "T2_Speed": round(tv2_spd[-1],3),
            "T3_Alpha_OT": round(alp_ot3, 3),
            "T3_Distance": round(Dbtwn3, 3),
            "T3_Speed": round(tv3_spd[-1], 3),
            "T4_Alpha_OT": round(alp_ot4, 3),
            "T4_Distance": round(Dbtwn4, 3),
            "T4_Speed": round(tv4_spd[-1], 3),
            "T5_Alpha_OT": round(alp_ot5, 3),
            "T5_Distance": round(Dbtwn5, 3),
            "T5_Speed": round(tv5_spd[-1], 3),
        }
        csv_writer.writerow(info)

    # --------------------------------------PLOT INFROMATION-----------------------------------------------------------

    # Sudo Text:

    plt_Dec1 = plt.text(4000, 4000, f'',
                        fontsize=10, color='white')
    plt_Dec2 = plt.text(4300, 4000, f'',
                        fontsize=10, color='white')
    plt_Dec3 = plt.text(4300, 4000, f'',
                        fontsize=10, color='white')
    plt_Dec4 = plt.text(4300, 4000, f'',
                        fontsize=10, color='white')
    plt_Dec5 = plt.text(4300, 4000, f'',
                        fontsize=10, color='white')
    plt_Dec6 = plt.text(4300, 4000, f'',
                        fontsize=10, color='white')

    # DEcesion Support msg :

    if CRI_tv1 > 0.6 and Dbtwn1 < 0.4:
        plt_Dec1 = plt.text(4500, -300,
                            f'T1: PSV_UT754WP entered the CAZ \n {dec1[0]} \n {dec1[1]}\n {dec1[2]}\n {dec1[3]}\n {dec1[4]}',
                            fontsize=6, color='white')

    elif CRI_tv2 > 0.6 and Dbtwn2 < 0.4:
        plt_Dec2 = plt.text(4500, -300,
                            f'T2: PSV_UT751E entered the CAZ\n {dec2[0]} \n {dec2[1]}\n {dec2[2]}\n {dec2[3]}\n {dec2[4]}',
                            fontsize=6, color='white')
    elif CRI_tv3 > 0.6 and Dbtwn3 < 0.4:
        plt_Dec3 = plt.text(4500, -300,
                            f'T3: PSV_3300CD entered the CAZ\n {dec3[0]} \n {dec3[1]}\n {dec3[2]}\n {dec3[3]}\n {dec3[4]}',
                            fontsize=6, color='white')
    elif CRI_tv4 > 0.6 and Dbtwn4 < 0.4:
        plt_Dec4 = plt.text(4500, -300,
                            f'T4: PX105_RMY entered the CAZ\n {dec4[0]} \n {dec4[1]}\n {dec4[2]}\n {dec4[3]}\n {dec4[4]}',
                            fontsize=6, color='white')
    elif CRI_tv5 > 0.6 and Dbtwn5 < 0.4:
        plt_Dec5 = plt.text(4500, -300,
                            f'T5: PSV_UT776CD entered the CAZ\n {dec5[0]} \n {dec5[1]}\n {dec5[2]}\n {dec5[3]}\n {dec5[4]}',
                            fontsize=6, color='white')
    else:
        plt_Dec6 = plt.text(4500, -300, f'Continue The Course',
                            fontsize=6, color='white')

    # Vessel Information Plot

    ows_Info = plt.text(3750, 5300,
                        f'OS: Gunnerus \nVelocity = {round(ov_spd[-1], 1)}Knots\nHeading = {round(ov_heading[-1], 3)} Degree \nDistance Travelled = {round(dtravlled, 2)} NM\nETA = {eta} Min',
                        fontsize=10, color='white')

    Vsl1_Info = plt.text(4400, 2900,
                         f'T1: PSV_UT754WP\nDCPA = {round(dcpa_tv1, 1)}NM\nTCPA = {-round(tcpa_tv1 * 3600, 3)}s\nCRI = {round(CRI_tv1, 3)}\nVelocity = {round(tv1_spd[-1], 1)} Kn',
                         fontsize=8, color='white')
    Vsl2_Info = plt.text(4400, 2300,
                         f'T2: PSV_UT751E\nDCPA = {round(dcpa_tv2, 1)}NM\nTCPA = {-round(tcpa_tv2 * 3600, 3)}s\nCRI = {round(CRI_tv2, 3)}\nVelocity = {round(tv2_spd[-1], 1)}Kn',
                         fontsize=8, color='white')
    Vsl3_Info = plt.text(4400, 1700,
                         f'T3: PSV_3300CD\nDCPA = {round(dcpa_tv3, 1)}NM\nTCPA = {-round(tcpa_tv3 * 3600, 3)}s\nCRI = {round(CRI_tv3, 3)}\nVelocity = {round(tv3_spd[-1], 1)}Kn',
                         fontsize=8, color='white')

    Vsl4_Info = plt.text(4400, 1100,
                         f'T4: PX105_RMY\nDCPA = {round(dcpa_tv4, 1)}NM\nTCPA = {-round(tcpa_tv4 * 3600, 3)}s\nCRI = {round(CRI_tv4, 3)}\nVelocity = {round(tv4_spd[-1], 1)}Kn',
                         fontsize=8, color='white')

    Vsl5_Info = plt.text(4400, 500,
                         f'T5: PSV_UT776CD\nDCPA = {round(dcpa_tv5, 1)}NM\nTCPA = {-round(tcpa_tv5 * 3600, 3)}s\nCRI = {round(CRI_tv5, 3)}\nVelocity = {round(tv5_spd[-1], 1)}Kn',
                         fontsize=8, color='white')

    ln_ov.set_data(ov_x, ov_y)
    ln_tv1.set_data(tv1_x, tv1_y)
    ln_tv2.set_data(tv2_x, tv2_y)
    ln_tv3.set_data(tv3_x, tv3_y)
    ln_tv4.set_data(tv4_x, tv4_y)
    ln_tv5.set_data(tv5_x, tv5_y)


    time_text.set_text(now.strftime("%Y-%m-%d %H:%M:%S"))

    return time_text,plt_ov_mk_com, plt_t00_cir, ows_Info, Vsl5_Info, Vsl4_Info, Vsl3_Info, Vsl2_Info, Vsl1_Info, plt_Dec6, plt_Dec5, plt_Dec4, plt_Dec3, plt_Dec2, ln_ov, ln_tv1, ln_tv2, ln_tv3, ln_tv4, ln_tv5, plt_ov_dom, plt_ov_mk, plt_tv1_mk, plt_t1_dom, plt_tv2_mk, plt_t2_dom, plt_tv3_mk, plt_t3_dom, plt_tv4_mk, plt_t4_dom, plt_tv5_mk, plt_t5_dom, plt_ov_txt, plt_tv1_txt, plt_tv1_cpa, plt_tv2_txt, plt_tv2_cpa, plt_tv3_txt, plt_tv3_cpa, plt_tv4_txt, plt_tv4_cpa, plt_tv5_txt, plt_tv5_cpa, plt_t5_cir, plt_t4_cir, plt_t3_cir, plt_t2_cir, plt_t1_cir, plt_t0_cir, plt_Dec1,

class UnsizedMarker(MarkerStyle):

    def _set_custom_marker(self, path):
        self._transform = transforms.IdentityTransform()
        self._path = path


ani = FuncAnimation(fig, update, frames=np.arange(1, 200000, 1), blit=True, interval=10, repeat=False)  # interval (ms)

mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry("+0+0")

plt.show()
