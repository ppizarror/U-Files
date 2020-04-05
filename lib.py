#!/usr/bin/env python
# -*- coding: utf-8 -*-
#LIB
#Pablo Pizarro, 2014
#Este fichero carga las librerías importantes y las funciones globales
#Importación de librerías

#Importación de liberías de alto nivel
import sys
import os

#Configuración de las librerías de alto nivel
reload(sys)
sys.setdefaultencoding('UTF8') #defino la codificación UTF-8
sys.dont_write_bytecode = True #cancelo la compilación .pyc
_actualpath = str(os.getcwd()).replace("\\","/")
sys.path.append(_actualpath+"/lib/")
sys.path.append(_actualpath+"/lib/mechanize/")
try: sys.path.append(_actualpath+"/lib/wconio/")
except: pass
try: os.remove("lib.pyc") #elimino el archivo pyc compilado
except: pass

#Importación de librerías de bajo nivel
from Tkinter import *
from VerticalScrolledFrame import *
from functools import partial
from test import *
try: import WConio
except: pass
import ctypes
import random
import re
import time
import tkFont
import ttk
import urllib
import webbrowser
try: import winsound
except: pass

#Definición de constantes
CONSOLE_WRAP = -25 #define la partición del texto de la consola
CMD_COLORS = {"red":0x40,"lred":0xC0,"gray":0x80,"lgray":0x70,"white":0xF0,"blue":0x10,\
             "green":0x20,"purple":0x50,"yellow":0x60,"lblue":0x90,"lgreen":0xA0,\
             "lpurple":0xD0,"lyellow":0xE0}

#Métodos
def colorcmd(cmd,color): #Función que imprime un mensaje con un color
    try:
        if color in CMD_COLORS: color = CMD_COLORS[color]
        else: color = 0x0F
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)
        print cmd,
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x07)
    except: pass

def delMatrix(matrix): #Borrar una matriz
    a = len(matrix)
    if a>0:
        for k in range(a): matrix.pop(0)

def getTerminalSize(): #Devuelve el tamaño de la consola
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr: cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])

def loadFromArchive(archive,lang="Cargando archivo '{0}' ...",showState=True): #Carga un archivo y retorna una matriz
    if showState!=False: print lang.format("(...)"+archive[CONSOLE_WRAP:].replace("//","/")).replace("\"",""),
    try: #Se carga el archivo
        l = list()
        archive = open(archive,"r")
        for i in archive:
            l.append(i.decode('utf-8').strip())
        archive.close()
        if showState!=False: print "ok"
    except:
        if showState!=False: print "error"
        l = []
    return l

def openWeb(url,event): #Abre una dirección web
    webbrowser.open(url)

def printAsciiArt(): #Imprime el arte ascii de la introducción
    try: WConio.clrscr() #limpio la pantalla previa
    except: pass
    try:
        (width,height) = getTerminalSize() #se obtiene el largo de la consola para dejarlo centrado
        asciiart = open("data/documents/ascii.txt","r")
        for i in asciiart: print " "*(int((width-26)/2)-6), i.rstrip()
        asciiart.close()
    except: pass
