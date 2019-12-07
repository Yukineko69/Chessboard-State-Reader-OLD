#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:54:36 2019

@author: tuan
"""

import sys
import tkinter as tk #or Tkinter if you're on Python2.7
from PIL import ImageTk, Image

def button1():
    novi = tk.Toplevel()
    canvas = tk.Canvas(novi, width = 1000, height = 800)
    canvas.pack(expand = tk.YES, fill = tk.BOTH)
#    gif1 = PhotoImage(file = '28.jpg')
    basewidth = 500
    img = Image.open('28.jpg')
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    gif1 = ImageTk.PhotoImage(img)
                                #image not visual
    canvas.create_image(0, 0, image = gif1, anchor = tk.NW)
    #assigned the gif1 to the canvas object
    canvas.gif1 = gif1


mGui = tk.Tk()
button1 = tk.Button(mGui,text ='Sklop',command = button1, height=5, width=20).pack()

mGui.mainloop()