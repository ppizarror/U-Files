# -*- coding: utf-8 -*-
#!/usr/bin/env python
#Textures - Texturas para u-files
#Pablo Pizarro, 2014

#Importación de librerías
from lib import *

#Definición de constantes
ACTUAL_FOLDER = str(os.getcwd()).replace("\\","/")+"/" #directorio actual
DATA_FOLDER = ACTUAL_FOLDER+"data/" #carpeta de datos
FOLDER_IMAGES = DATA_FOLDER+"images/" #carpeta de imágenes
FOLDER_ICONS = FOLDER_IMAGES+"icons/" #carpeta de iconos
FOLDER_FILES = FOLDER_IMAGES+"files/" #carpeta de iconos de archivos
FOLDER_SPRITES = FOLDER_IMAGES+"sprites/" #carpeta de sprites
DATA_IMAGES_BACKGROUND = FOLDER_IMAGES+"background/" #imagenes de fondo

class UfilesTextures: #Clase principal de las texturas

    def __init__(self,lang=["Cargando textura '%.gif' ...","ok"]): #Función constructora
        self.lang = lang
        self.images = {
        #links de escape--
        None:None,\
        "None":None,\

        #archivos
        "file": PhotoImage(file=FOLDER_FILES+"file.gif"),\

        #iconos
        "exclamation": FOLDER_ICONS+"exclamation.ico",\
        "folder_explore": FOLDER_ICONS+"folder_explore.ico",\
        "help": FOLDER_ICONS+"help.ico",\
        "licence": FOLDER_ICONS+"licence.ico",\
        "page_gear": FOLDER_ICONS+"page_gear.ico",\
        "ucursos": FOLDER_ICONS+"ucursos.ico",\

        #imagenes
        "box_curso": PhotoImage(file=FOLDER_SPRITES+"box_curso.gif"),\
        "box_curso_loading": PhotoImage(file=FOLDER_SPRITES+"box_curso_loading.gif"),\
        "calendario": PhotoImage(file=FOLDER_SPRITES+"calendario.gif"),\
        "cursos": PhotoImage(file=FOLDER_SPRITES+"cursos.gif"),\
        "cursos_departamento": PhotoImage(file=FOLDER_SPRITES+"cursos_departamento.gif"),\
        "datos_curso": PhotoImage(file=FOLDER_SPRITES+"datos_curso.gif"),\
        "horario_curso": PhotoImage(file=FOLDER_SPRITES+"horario_curso.gif"),\
        "integrantes": PhotoImage(file=FOLDER_SPRITES+"integrantes.gif"),\
        "lupa": PhotoImage(file=FOLDER_SPRITES+"lupa.gif"),\
        "material_alumnos": PhotoImage(file=FOLDER_SPRITES+"material_alumnos.gif"),\
        "material_docente": PhotoImage(file=FOLDER_SPRITES+"material_docente.gif"),\
        "menu_cursos_box": PhotoImage(file=FOLDER_SPRITES+"menu_cursos_box.gif"),\
        "novedades_institucion": PhotoImage(file=FOLDER_SPRITES+"novedades_institucion.gif"),\

        #fondos
        "background1": PhotoImage(file=DATA_IMAGES_BACKGROUND+"background1.gif"),\
        "background2": PhotoImage(file=DATA_IMAGES_BACKGROUND+"background2.gif")
        }

    def image(self,image): #Función que llama a las imágenes, si existe se retorna el objeto, si no se crea
        try: #si se puede se retorna el objeto
            return self.images[image]
        except: #si no existe se carga
            return None