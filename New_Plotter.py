import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import datetime
from matplotlib.path import Path
import pandas as pd
from matplotlib import transforms
from matplotlib.animation import FuncAnimation
from matplotlib.markers import MarkerStyle
import numpy as np
import CRI_Functions_Support.trgs_ang
import CRI_Functions_Support.deci_sup
import CRI_Functions_Support.domain
import CRI_Functions_Support.CRI_FunExe

#The Background Map and Canvas Layout

img = plt.imread('Support_images/pure_map.png')
fig, ax = plt.subplots()
fig.set_size_inches(13, 7)
fig.patch.set_facecolor('#000000')
plt.subplots_adjust(left=0.00, right=0.95, top=0.95, bottom=0.05)
ax.imshow(img, extent=[-4122, 6028, -400, 4675], alpha=0.96)
plt.xlim([-4122, 6028])
plt.ylim([-400, 4675])
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.grid(alpha=0.2)
ax.set_title(u"|Real Time DS System|")
ax.legend()
#--------------------------------------- Graphical Elements ----------------------------------------------------
Recco = plt.text(4500, 1500, f'Recommendation ', fontsize=10, color='white')
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, color='white')
Rect = mpimg.imread('Support_images/rect2.png')
RectBox = OffsetImage(Rect, zoom=0.75, alpha=0.5)
box1 = AnnotationBbox(RectBox, (4985, 1950), frameon=False)
color_bar = mpimg.imread('Support_images/colorbars.png')
colorbox = OffsetImage(color_bar, zoom=0.195, alpha=0.5)
color = AnnotationBbox(colorbox, (5000, 4000), frameon=False)
Comps = mpimg.imread('Support_images/comp_3.png')
compass = OffsetImage(Comps, zoom=0.15, alpha=0.5)
commp = AnnotationBbox(compass, (3000, 800), frameon=False)
Rec_box = mpimg.imread('Support_images/rec_box.png')
Rec1 = OffsetImage(Rec_box, zoom=0.8, alpha=0.5)
rec = AnnotationBbox(Rec1, (5000, 1000), frameon=False)
ax.add_artist(rec)
ax.add_artist(box1)
ax.add_artist(color)
ax.add_artist(commp)

# departure and arrival
x = [0, -24]
y = [0, 4088]
plt.plot(x[0], y[0], c='green', marker='o', markersize=8)
plt.plot(x[1], y[1], c='red', marker='o', markersize=8)

#------------------------------------------------ Plot Data----------------------------------------------------
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


class ship:
    def __init__(self,OS_V,OS_H,OS_X,OS_Y,TV_V,TV_H,TV_X,TV_Y):
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



class Ship_data:
    def __init__(self,data,ori):
        self.x = data['Num']
        self.xo = ori['Num']
        self.num = len(self.x)-1
        self.numo = len(self.xo)-1
        self.ang = ori['Ori'][self.xo][self.numo]
        self.gen_x = data['Lo'][self.x][self.num]
        self.gen_y = data['La'][self.x][self.num]
        self.velo = data['Total Speed'][self.x][self.num]

    def back_flow(self):
        return (self.gen_x,self.gen_y,self.ang,self.velo)


def Ship_Shape():
    def_marker = Path([[-0.005, -0.02], [0.005, -0.02], [0.005, 0.01], [0, 0.02], [-0.005, 0.01], [0, 0], ],
                      [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    return (def_marker)

def update(frame):
    now = datetime.datetime.now()

    ship_shape = Ship_Shape()

    # Own Ship
    OS_Data = pd.read_csv('Data_Collected/TS2_Data.csv')
    OS_Ori = pd.read_csv('Data_Collected/ori/OriTS2.csv')
    os = Ship_data(OS_Data,OS_Ori)
    os_bf = os.back_flow()
    ov_x.append(os_bf[0] - origin_x)
    ov_y.append(os_bf[1] - origin_y)
    ov_heading.append(os_bf[2])
    ov_spd.append(os_bf[3])

    #Plot Data
    ov_mk_rtt = transforms.Affine2D().rotate_deg(-ov_heading[-1])
    plt_ov_txt = plt.text(ov_x[-1] + 100, ov_y[-1], f'OS : Gunnerus', fontsize=10, color='white')
    ov_mk = ship_shape.transformed(ov_mk_rtt)
    plt_ov_mk = ax.scatter(ov_x[-1], ov_y[-1], marker=ov_mk, color='white', s=15 ** 2, alpha=0.5)


    # TS1
    TS1_Data = pd.read_csv('Data_Collected/TS1_Data.csv')
    TS1_Ori = pd.read_csv('Data_Collected/ori/OriTS1.csv')
    ts1 = Ship_data(TS1_Data,TS1_Ori)
    ts1_bf = ts1.back_flow()
    tv1_x.append(ts1_bf[0] - origin_x)
    tv1_y.append(ts1_bf[1] - origin_y)
    tv1_heading.append(ts1_bf[2])
    tv1_spd.append(ts1_bf[3])
    pk1 = ship(ov_spd[-1], ov_heading[-1], ov_x[-1], ov_y[-1], tv1_spd[-1], tv1_heading[-1], tv1_x[-1], tv1_y[-1])
    print(pk1.CRI())
    #Plot Data
    ts1_mk_rtt = transforms.Affine2D().rotate_deg(-tv1_heading[-1])
    plt_TS1_txt = plt.text(tv1_x[-1] + 100, tv1_y[-1], f'TS1 : PSV_UT754WP', fontsize=10, color='white')
    ov_mk = ship_shape.transformed(ts1_mk_rtt)
    plt_ts1_mk = ax.scatter(tv1_x[-1], tv1_y[-1], marker=ov_mk, color='white', s=15 ** 2, alpha=0.5)

    return plt_ov_txt,plt_ov_mk,plt_TS1_txt,plt_ts1_mk


class UnsizedMarker(MarkerStyle):

    def _set_custom_marker(self, path):
        self._transform = transforms.IdentityTransform()
        self._path = path

ani = FuncAnimation(fig, update, frames=np.arange(1, 200000, 1), blit=True, interval=10, repeat=False)  # interval (ms)

mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry("+0+0")

plt.show()






