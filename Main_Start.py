import tkinter as tk
from tkinter import ttk
import matplotlib
import tkinter.messagebox
matplotlib.use("TkAgg")
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

from subprocess import call


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

LARGE_FONT = ("Verdana",12)

cmd = '1_Data_Downlink.py'

def data_down():
    call(["python", "2_Plotter.py"])





class SeaofBTCapp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        #tk.Tk.iconbitmap(self,default = "Support_images/icon.ico")
        tk.Tk.wm_title(self,"Decision Support Systems V.1.1")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()


        self.frames = {}

        for F in (StartPage,PageOne):

            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):

        frame = self.frames[cont]
        frame.tkraise()


def qf():
    print("You Did it")

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text ="Welcome to the Decision Support System Version 1.1", font = LARGE_FONT)
        label.pack(pady=10,padx=10)

        text_label = tk.Label(self,text ='This the initial edition of the decision support system developed by Intelligent Systems Lab at NTNU i Ålesund \n The system has mainly three operation stages:\n 1. Collection of Data from the simulator in real time ')
        text_label.pack()
        
        button1 = ttk.Button(self,text = "Get Started",command = lambda : controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


        text_label = tk.Label(self,text ='Staring the downlink will grab the data from the live simulation and save as csv in the local machine ')
        text_label.pack()

        button1 = ttk.Button(self, text="Start DownLink", command=lambda : controller.show_frame(data_down()))
        button1.pack()

        text_label = tk.Label(self,text ='Starting the plot generate live plot for the incoming data ')
        text_label.pack()
        button2 = ttk.Button(self, text="Start Plot", command=lambda : controller.show_frame(Pagetwo))
        button2.pack()

        button3 = ttk.Button(self, text="Home Page", command=lambda : controller.show_frame(StartPage))
        button3.pack()





app = SeaofBTCapp()
app.mainloop()