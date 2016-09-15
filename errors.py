#!/usr/bin/env python
# -*- coding: utf-8 -*-
#LIB
#Pablo Pizarro, 2014
#Definición de errores

#Códigos de error
BR_ERRORxERROR_SET_FORM = 8
BR_ERRORxERROR_SET_SUBMIT = 9
BR_ERRORxNO_ACCESS_WEB = 1
BR_ERRORxNO_FORM = 3
BR_ERRORxNO_FORMID = 2
BR_ERRORxNO_OPENED = 0
BR_ERRORxNO_SELECTED_FORM = 5
BR_ERRORxNO_VALIDID = 4
BR_ERRORxNO_VALID_SUBMIT_EMPTY = 6
BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL = 7
CURSOSxERROR_CANT_LOAD_CURSO = 20
DATA_ERRORxNO_APOS_IN_DATA = 18
DATA_ERRORxNO_BPOS_IN_DATA = 19
DATA_ERRORxNO_CURSOS = 17
FILESXERROR_NOEXIST = 21
FILESXERROR_NOFILES = 23
FILESXERROR_NOPERM = 22
FILESXNO_ERROR = 24
TAG_ERRORxCANT_RETRIEVE_HTML = 16
TAG_INIT_NOT_CORRECT_ENDING = 14
TAG_INIT_NOT_FINDED = 13
TAG_LAS_NOT_FINDED = 15
U_PASSPORT_ERRORxNO_LOAD = 12
U_PASSPORT_ERRORxNO_USER = 10
U_PASSPORT_ERRORxUSER_NOT_VALID = 11

#Descripción de errores
ERRORS = {
          BR_ERRORxERROR_SET_FORM : "Error al establecer el formulario activo",\
          BR_ERRORxERROR_SET_SUBMIT : "Error al enviar los datos",\
          BR_ERRORxNO_ACCESS_WEB : "No se puede acceder a la internet",\
          BR_ERRORxNO_FORM : "No existen formularios en la página actual",\
          BR_ERRORxNO_FORMID : "No existe un formulario con esa identificación",\
          BR_ERRORxNO_OPENED : "La página web no ha podido ser cargada",\
          BR_ERRORxNO_SELECTED_FORM : "No se ha seleccionado ningún formulario",\
          BR_ERRORxNO_VALIDID : "El id ingresado no es válido",\
          BR_ERRORxNO_VALID_SUBMIT_EMPTY : "Los datos del formulario no pueden estar vacíos",
          BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL : "No se satisfacen todos los datos pedidos por el formulario",\
          CURSOSxERROR_CANT_LOAD_CURSO : "Error al cargar el curso {0}",\
          DATA_ERRORxNO_APOS_IN_DATA : "No se encuentra el primer dato en el código",\
          DATA_ERRORxNO_BPOS_IN_DATA : "No se encuentra el segundo dato en el código",\
          DATA_ERRORxNO_CURSOS : "No hay cursos disponibles para cargar",\
          TAG_ERRORxCANT_RETRIEVE_HTML : "No se puede devolver el texto entre los tags",\
          TAG_INIT_NOT_CORRECT_ENDING : "No se ha encontrado > en el tag inicial",\
          TAG_INIT_NOT_FINDED : "El tag final no ha sido encontrado en el código",\
          TAG_INIT_NOT_FINDED : "El tag inicial a buscar no está en el código",\
          U_PASSPORT_ERRORxNO_LOAD : "Error al intentar conectar al servidor",\
          U_PASSPORT_ERRORxNO_USER : "Falta Usuario o Clave",\
          U_PASSPORT_ERRORxUSER_NOT_VALID : "Usuario o Clave incorrecto"
          }

def getError(id): #Retorna el error
    try: return ERRORS[id]
    except: return "Este código de error no está definido"