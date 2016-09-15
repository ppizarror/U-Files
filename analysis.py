#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Analisis
#Pablo Pizarro, 2014
#Examina el código html de u-cursos y envia distintos datos

#Importación de librerías
from errors import *

def buscarArchivos(html,http,ano,semestre,seccion,material): #Buscar archivos en el contenido html
    def _analizarLink(link, href_madre): #Analiza el link del curso y retorna el tipo de archivo, el link y el nombre
        tipo = getBetween(link, 'class="file ', '" href')
        nombre = getBetween(link, '">', '</a>').replace("."+tipo,"").replace(tipo,"")
        link = getBetween(link, 'href="', '">')
        return (nombre, tipo, http+link)
    def _calcularPeso(txt): #Calcula el peso de un archivo en kilobytes
        txt = txt.replace(",",".").strip().split(" ")
        peso = 0.0
        if txt[1]=="kb": peso = float(txt[0])
        elif txt[1]=="mb": peso = float(txt[0])*1000
        elif txt[1]=="gb": peso = float(txt[0])*1000000
        return int(peso)
    def _comprobarDigito(dig): #Comprueba si es un dígito y devuelve
        if dig.isdigit(): return int(dig)
        else: return dig
    def _transformarFecha(fecha,y): #Transforma el formato de la fecha
        if "/" in fecha:
            return fecha
        else:
            meses = {"Enero":"01","Febrero":"02","Marzo":"03","Abril":"04","Mayo":"05","Junio":"06","Julio":"07","Agosto":"08",\
                     "Septiembe":"09","Octubre":"10","Noviembre":"11","Diciembre":"12"}
            fecha = fecha.strip().split(" ")
            if len(fecha)>3: fecha.pop(0)
            else: pass
            dia = fecha[0].zfill(2)
            try: mes = meses[fecha[2]]
            except: mes = fecha[2]
            try: return dia+"/"+mes+"/"+str(y)
            except: return " ".join(fecha)
    def _verUploader(html): #Revisa quién subió el documento
        try:
            html = html.lower()
            if "de" in html: return "profesor"
            elif "auxiliar" in html: return "auxiliar"
            else: return "alumno"
        except:
            print "Error::verUploader("+str(html)+")"
            return "<-ERROR->"
    if html != BR_ERRORxNO_OPENED: #Si el link se abrió
        material = material.replace("/","")
        html = getBetweenTags(html, '<h1 class="modulo">', '</table>')
        files = []
        while True: #Busco por los archivos
            cont = getWithTags(html,'<tr id','</tr>') #se consulta por el tag completo
            if cont != TAG_INIT_NOT_FINDED and cont !="": #Si el contenido existe
                (nombre_archivo, tipo_archivo, link_archivo) = _analizarLink(getWithTags(cont, '<a class="file ', '</a>'),http)
                peso_archivo = _calcularPeso(getBetweenTags(getBetween(cont, '<em>', '</em>'),'(',')'))
                tipo_uploader = _verUploader(getBetween(cont, '<td><div title="', 'class="sprite_cargos '))
                uploader = getBetweenTags(cont, '<a class="usuario" href=', '</a></td>')
                descargas = _comprobarDigito(getBetweenTags(getBetweenTags(cont, '<td rel="', '</a>'),'<td>','</td>'))
                fecha_subida = _transformarFecha(getBetweenTags(cont, '<td rel="', '</td>'),ano)
                files.append([reemplazarCaracteresHtml(nombre_archivo),tipo_archivo,peso_archivo,descargas,reemplazarCaracteresHtml(uploader),ano,\
                              semestre,seccion,fecha_subida,link_archivo,tipo_uploader,material])
                html = html.replace(cont, "") #se elimina de los datos
            else: break #si ya no existe termina el bucle
        return files
    else: return []

def comprobarCarga(html): #Se comprueba el estado de la carga de las páginas de archivos
    if html != BR_ERRORxNO_OPENED: #Si el link se abrió
        error = getBetweenTags(getBetweenTags(html, '<div class="mensaje2 merror">', '</div>'),'<li>','</li')
        if error != TAG_INIT_NOT_FINDED:
            if "buscando no existe" in error: return FILESXERROR_NOEXIST
            elif "No tiene permisos para ver esta pagina" in error: return FILESXERROR_NOPERM
        else: #Si no se encontró algun mensaje de error análogo
            state = getBetweenTags(getBetweenTags(html, '<thead class="sticky">', '</table>'),'<td colspan="0">','.</td>')
            if state=="No hay materiales": return FILESXERROR_NOFILES
            else: return FILESXNO_ERROR

def comprobarLogin(html): #Se comprueba que se conectó a u-pasaporte / retorna <True/False>
    if html != BR_ERRORxNO_OPENED: #Si el link se abrió
        if "Falta Usuario o Clave" in html: return U_PASSPORT_ERRORxNO_USER
        elif "Usuario o Clave incorrecto" in html: return U_PASSPORT_ERRORxUSER_NOT_VALID
        else: return True
    else: return U_PASSPORT_ERRORxNO_LOAD

def getBetween(html,a,b): #Retorna un texto entre a y b en los datos html
    try: posa = html.index(a) #se encuentra el primer puntero
    except: return DATA_ERRORxNO_APOS_IN_DATA
    posa+=len(a)
    try: posb = html.index(b,posa) #se encuentra el primer puntero
    except: return DATA_ERRORxNO_BPOS_IN_DATA
    return html[posa:posb]

def getCursos(html): #Retorna los cursos del usuario
    def _delCodigo(nombreCurso): #Elimina el código del curso
        nombreCurso = nombreCurso.split(" "); nombreCurso.pop(0); return " ".join(nombreCurso)
    def _getCodigo(nombreCurso): #Retorna el código del curso
        return nombreCurso.split(" ").pop(0)
    if html != BR_ERRORxNO_OPENED: #Si el link se abrió
        data = getBetweenTags(html,'<div id="cursos"','<div id="comunidades"')
        cursos = [] #matriz de datos de los cursos
        while True: #Se recorre el contenido html en busca de los cursos
            cont = getWithTags(data,'<li id="curso.','</li>') #se consulta por el tag completo
            if cont != TAG_INIT_NOT_FINDED: #Si el contenido exise
                cursos.append(cont.strip()) #se agrega el curso
                data = data.replace(cont, "") #se elimina de los datos
            else: break #si ya no existe termina el bucle
        if len(cursos)>0: #Si hay cursos cargados
            for i in range(len(cursos)): #Recorro los cursos
                cursos[i]=getBetweenTags(cursos[i],'<li id="curso.','</li>').replace('<div title="Alumno" class="sprite_cargos cargos_alumno"></div>',"")
                if getWithTags(cursos[i],'<div class="nuevo">','</a></div>')!= TAG_INIT_NOT_FINDED: #Si hay novedades
                    cursos[i] = cursos[i].replace(getWithTags(cursos[i],'<div class="nuevo">','</a></div>'),"")
                nombre_curso = getBetween(cursos[i],'<span>','</span>')
                cursos[i]= [_delCodigo(nombre_curso),getBetween(cursos[i],'<a href="','">'),_getCodigo(nombre_curso)]
        else: return DATA_ERRORxNO_CURSOS #si no se han encontrado cursos disponibles
        return cursos
    else:
        return [["Curso 1","link_curso_1","C-1001"],["Curso 2","link_curso_2","C-1002"],["Curso 3","link_curso_3","C-1003"]]

def getBetweenTags(html,tagi,tagf): #Función que retorna un valor entre dos tags
    tagi = tagi.strip()
    tagf = tagf.strip()
    try: #Busco el primer tag
        posi = html.index(tagi) #busco el primer tag
        if ("<" in tagi) and (">" not in tagi): #Si el tag incluia la viñeta < y no finalizaba
            c = 1
            while True:
                try:
                    if html[posi+c]==">":posi+=(c+1); break
                    c+=1
                except: return TAG_INIT_NOT_CORRECT_ENDING
        else: posi+=len(tagi)
    except: return TAG_INIT_NOT_FINDED #no se encontró el primer tag
    try:
        posf = html.index(tagf, posi) #busco el segundo tag
    except: return TAG_LAS_NOT_FINDED
    try: return html[posi:posf] #devuelvo la cadena entre los tags
    except: return TAG_ERRORxCANT_RETRIEVE_HTML

def getWithTags(html,tagi,tagf): #Función que retorna el código incluido los tags
    tagi = tagi.strip() #elimino los espacios en blanco
    tagf = tagf.strip()
    try: posi = html.index(tagi) #busco el primer tag
    except: return TAG_INIT_NOT_FINDED #no se encontró el primer tag
    try:
        posf = html.index(tagf, posi) #busco el segundo tag
        if ("<" in tagf) and (">" not in tagf): #Si el tag incluia la viñeta < y no finalizaba
            c = 1
            while True:
                try:
                    if html[posf+c]==">":posf+=(c+1); break
                    c+=1
                except: return TAG_INIT_NOT_CORRECT_ENDING
        else: posf+=len(tagf)
    except: return TAG_LAS_NOT_FINDED
    try: return html[posi:posf] #devuelvo la cadena entre los tags
    except: return TAG_ERRORxCANT_RETRIEVE_HTML

def obtenerInfoLink(link): #Obtener la información de un curso mediante un link
    link = link.split("/")
    return (int(link[4]),int(link[5]),int(link[7]))

def reemplazarCaracteresHtml(html): #Elimina carácteres especiales
    html=html.replace("&aacute;","á").replace("&eacute;","é").replace("&iacute;","í").replace("&oacute;","ó").replace("&uacute;","ú")
    html=html.replace("&Aacute;","Á").replace("&Eacute;","É").replace("&Iacute;","Í").replace("&Oacute;","Ó").replace("&Uacute;","Ú")
    html=html.replace("&ntilde;","ñ").replace("&Ntilde;","Ñ").replace("&nbsp;"," ").replace("&lt;","<").replace("&gt;",">").replace("&amp;","&")
    html=html.replace("&quot;",'"').replace("&iexcl;","¡").replace("&iquest;","¿").replace("&reg;","®").replace("&copy;","©").replace("&euro;","€")
    html=html.replace("&uuml;","ü").replace("&Uuml;","Ü")
    return html

def transformarLink(link):
    link = link.split("/")
    return link[0]+"//"+link[2]+"/"+link[3]