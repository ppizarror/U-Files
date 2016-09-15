#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Browser
#Pablo Pizarro, 2014
#Define al objeto browser encargado de obtener y manejar eventos http

#Importación de librerías
from errors import *
import cookielib
import mechanize

class Browser: #Navegador web

    def __init__(self): #Función constuctora
        self.br = mechanize.Browser() #navegador
        self.cookies = cookielib.LWPCookieJar() #cookies
        self.br.set_cookiejar(self.cookies)
        self.opened = False #define si una páginas se ha cargado
        self.selectedForm = False #define si se ha definido un formulario

        #Opciones del navegador
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_refresh(False)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def playBrowser(self): #Obtener el browser
        return self.br

    def addHeaders(self,header): #Agregar headers al navegador
        self.br.addheaders = [('User-agent', header)]

    def abrirLink(self,web): #Ingresar a una dirección web
        try: #Intento cargar la web
            self.br.open(web)
            self.opened = True
            self.selectedForm = False
        except: return BR_ERRORxNO_ACCESS_WEB

    def getHtml(self): #Obtener el código html
        if self.opened: return self.br.response().read()
        else: return BR_ERRORxNO_OPENED

    def getTitle(self): #Obtener el título
        if self.opened: return self.br.title()
        else: return BR_ERRORxNO_OPENED

    def getHeaders(self): #Obtener los headers
        if self.opened: return self.br.response().info()
        else: return BR_ERRORxNO_OPENED

    def getForms(self): #Obtener los forms
        if self.opened: return self.br.forms()
        else: return BR_ERRORxNO_OPENED

    def selectFormById(self,formid): #Definir un formulario como activo mediante un id
        formid = str(formid)
        if formid!="": #Si el id no está vacío
            if formid.isdigit(): #Si es un dígito
                try:
                    self.selectedForm = True
                    return self.br.select_form(nr=int(formid))
                except: return BR_ERRORxERROR_SET_FORM
            else: return BR_ERRORxNO_VALIDID
        else: return BR_ERRORxNO_FORMID

    def selectFormByName(self,formname): #Definir un formulario como activo mediante un id
        if formname!="": #Si el id no está vacío
            try:
                self.selectedForm = True
                return self.br.select_form(name=formname)
            except: return BR_ERRORxERROR_SET_FORM
        else: return BR_ERRORxNO_FORMID

    def submitForm(self,form,values): #Enviar un formulario
        if self.selectedForm:
            if len(form)>0 and len(values)>0:
                if len(form)==len(values):
                    try:
                        for i in range(len(form)): self.br.form[form[i]]=values[i]
                        self.br.submit()
                    except: return BR_ERRORxERROR_SET_SUBMIT
                else: return BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL
            else: return BR_ERRORxNO_VALID_SUBMIT_EMPTY
        else: return BR_ERRORxNO_SELECTED_FORM

    def clearCookies(self): #Elimina las cookies
        self.cookies.clear_session_cookies()