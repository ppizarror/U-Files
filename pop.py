#!/usr/bin/env python
# -*- coding: utf-8 -*-
#POP - U-Files
#Pablo Pizarro, 2014

#Importación de librerias
from lib import *

#Constantes del programa
DEFAULT_FONT_TITLE="Arial",10
COMMENT_COLOR="#666666"

class Pop: #Ventanas emergentes

    def __init__(self,properties): #Función constructora
        lang = properties[0]
        if "list" in str(type(lang)): title = lang[0]
        else: title=properties[0]
        icon = properties[1]
        typeObject = properties[2]
        size = properties[4],properties[3]
        if title=="Error" or title=="Buscar" or title=="Licencia": self.w = Toplevel()
        else: self.w = Tk()
        self.w.protocol("WM_DELETE_WINDOW", self.kill)
        self.values = []
        if size[0]!=0 and size[1]!=0:
            self.w.minsize(width=size[0], height=size[1])
            self.w.geometry('%dx%d+%d+%d' % (size[0], size[1], (self.w.winfo_screenwidth() - size[0])/2,(self.w.winfo_screenheight() - size[1])/2))
        self.w.resizable(width=False, height=False)
        self.w.focus_force()
        self.w.title(title)
        try: self.w.iconbitmap(icon)
        except: self.w.iconbitmap("data/icons/ucursos.ico")
        self.sent = False

        if typeObject=="about": #Acerca de
            Label(self.w,text=lang[1]+properties[5],font=DEFAULT_FONT_TITLE,border=5).pack()
            Label(self.w,text=lang[2]+properties[6],font=DEFAULT_FONT_TITLE,border=5).pack()
            Label(self.w,text=lang[3]+str(properties[7]),font=DEFAULT_FONT_TITLE,border=5).pack()
            Button(self.w, text=lang[4],command=self.w.destroy,relief=GROOVE).pack()
            self.w.bind("<Return>", self.destruir)
        elif typeObject=="error" or typeObject=="aviso": #Alerta
            try:
                if typeObject=="error": winsound.MessageBeep(16) #Sonido de error
                elif typeObject=="aviso": winsound.MessageBeep(1) #Sonido de error
            except: pass
            Label(self.w,text=properties[5],wraplength=250, anchor=N,border=10).pack()
            Button(self.w, text=lang[1], command=self.w.destroy,relief=GROOVE).pack()
            self.w.bind("<Return>", self.destruir)
            self.w.bind("<Escape>", self.destruir)
            self.w.focus_force()
        elif typeObject=="preguntarSNC": #Preguntar si/no/cancelar
            try:
                if properties[5]: winsound.MessageBeep(-1)
            except: pass
            self.w.focus_force()
            Label(self.w,text=lang[1],font=DEFAULT_FONT_TITLE,border=10).pack() #desea guardar
            F = Frame(self.w)
            F.pack()
            Button(F, text=lang[2],command=lambda:self.response("si"),width=5,relief=GROOVE).pack(side=LEFT) #si
            Label(F, text=" ").pack(side=LEFT)
            Button(F, text=lang[4],command=lambda:self.response("cancel"),width=8,relief=GROOVE).pack(side=LEFT) #cancelar
            Label(F, text=" ").pack(side=LEFT)
            Button(F, text=lang[3],command=lambda:self.response("no"),width=5,relief=GROOVE).pack() #no
        elif typeObject in ["licence","changelog","ayuda","longtext"]: #Licencia o gnu
            try: name = properties[6]
            except: name=""
            archivo = open(properties[5],"r")
            Yscroll = Scrollbar(self.w)
            Yscroll.pack(side=RIGHT, fill=Y)
            texto = Text(self.w,wrap=NONE,
            yscrollcommand=Yscroll.set,xscrollcommand=None)
            texto.focus_force()
            for i in archivo: texto.insert(INSERT,i)
            texto.pack(fill=BOTH)
            texto.configure(state="disabled")
            Yscroll.config(command=texto.yview)
            archivo.close()
            self.w.bind("<Return>", self.destruir)
            self.w.bind("<Escape>", self.destruir)

    def destruir(self,e=None): #Función para destruir la ventana
        self.w.destroy()

    def kill(self): #Función que destruye la ventana
        self.sent = False
        self.w.destroy()

    def response(self,res): #Función que envia una respuesta
        delMatrix(self.values)
        self.values.append(res)
        self.sent = True
        self.destruir()
