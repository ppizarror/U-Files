#!/usr/bin/env python
# -*- coding: utf-8 -*-
# U-files - archivo principal del programa
# Pablo Pizarro, 2014

# Importación de librerías de alto nivel
from lib import *

# Información del programa
AUTOR_NAME = "Pablo Pizarro"
AUTOR_NAME_EMAIL = "pablopizarro9@gmail.com"  # mi correo
PROGRAM_VERSION = "0.8"
PROGRAM_TITLE = "U-Files"
printAsciiArt()  # imprimo el arte
colorcmd("\nU-Files - version: " + PROGRAM_VERSION, "purple")
print "\nAutor: " + AUTOR_NAME

# Importación de librerías de bajo nivel
print "\nImportando librerias ...",
try:
    from analysis import *
    from browser import *
    from pop import *
    from textures import *
    from test import *
    import gc

    print "ok"
except:
    print "abortado"; exit()

# Configuración de las librerias
gc.enable()

# Constantes del programa
CONFIGURATION_DATA = ["ES", "background1"]  # configuraciones del programa
COLORED_ARGUMENT = False  # define si se colorean las entradas en la consola
FOLDER_CONFIG = ACTUAL_FOLDER + "config/"  # carpeta de configuraciones
FOLDER_DOCUMENTS = DATA_FOLDER + "documents/"  # carpeta de documentos
FOLDER_LANGS = ACTUAL_FOLDER + "langs/"  # carpeta de idiomas
HREF_HEADERS = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"  # headers para el browser
HREF_UPASAPORTE = "https://www.u-cursos.cl/upasaporte/login?servicio=ucursos&UCURSOS_SERVER=web38-int"  # página de inicio de upasaporte
LOGIN_FORM = ["username", "password"]  # formulario de inicio de sesión (por defecto)
PROGRAM_SIZE = [750, 450]  # tamaño en pixeles del programa
U_CURSOS_MT = ["material_docente/", "material_alumnos/"]  # links de materiales
U_CURSOS_SC = 8  # numero máximo de secciones a buscar
U_CURSOS_Y = 2009  # primer año para buscar desde u-cursos

try:  # Se cargan la lista de idiomas disponibles
    LANG_LIST = loadFromArchive(FOLDER_LANGS + "/config/langs.txt", "Cargando archivo '{0}' ...", False)
    LANG_CONST = loadFromArchive(FOLDER_LANGS + "/config/const.ini", "Cargando archivo '{0}' ...", False)
    LANG_END = LANG_CONST[0]
    LANG_SEP = LANG_CONST[1].replace("*", " ")
except:  # Si ocurre un error al cargar el archivo de idiomas se termina la ejecución del programa
    print "Error fatal"
    Pop([["Error fatal", "Cerrar"], FOLDER_ICONS + "cross.ico", "error", 85, 300,
         "No se encuentra el archivo de idiomas, " + \
         PROGRAM_TITLE + " no puede iniciarse."]).w.mainloop(0)
    exit()

# Idiomas
LANG = {}  # lista de strings para el idioma


def loadLang(first=True):  # Carga el idioma
    try:  # Se carga el idioma
        # Cargo el idioma definido por el archivo de configuraciones
        if COLORED_ARGUMENT:  # argumento colorido
            if first:
                print "Cargando idioma",; colorcmd(CONFIGURATION_DATA[0].lower(), "lgray"); print "...",
            else:
                print lang(746),; colorcmd(CONFIGURATION_DATA[0].lower(), "lgray"); print "...",
        else:
            if first:
                print "Cargando idioma", CONFIGURATION_DATA[0].lower(), "...",
            else:
                print lang(746), CONFIGURATION_DATA[0].lower(), "...",
        archivo = open(FOLDER_LANGS + CONFIGURATION_DATA[0] + LANG_END, "r")
        for i in archivo:
            item = i.strip().replace("\ufeff", "").split(LANG_SEP)
            if "\xef\xbb\xbf" in item[0]: item[0] = item[0][3:]  # elimino caracteres que no sean utf-8
            if item[0] == "": item[0] = "10"
            LANG[int(item[0].replace("\ufeff", ""))] = item[1].replace("|", " ")  # asigno los espacios
        archivo.close()
        print "ok"
    except:  # Error al cargar idioma, muestra mensaje y termina el programa
        print "Error fatal";
        Pop([["Error fatal", "Cerrar"], FOLDER_ICONS + "cross.ico", "error", 85, 300,
             "Error al cargar el archivo de idioma '" + \
             CONFIGURATION_DATA[0] + "', " + PROGRAM_TITLE + " no puede iniciarse"]).w.mainloop(0)
        os._exit(1)


def lang(i, a="", b="", c=""):  # Función que recibe un id y retorna el string correspondiente a dicho id
    try:  # Si existe el lang en la matriz de datos
        if len(a + b + c) != 0:
            return LANG[i].replace("%", a).replace("&", b).replace("$", c)
        else:
            return LANG[i]
    except:
        print "Error: ID[{0}] no existe en el archivo de idiomas '".format(i) + CONFIGURATION_DATA[0] + "'"
        return "%LANG ID[{0}]".format(i)


class Ufiles:  # U-files, entorno gráfico e interacción de objetos

    def __init__(self):  # Función constructora

        # Métodos del constructor
        def _about():  # Carga el acerca de
            e = Pop(
                [[lang(19), lang(31), lang(32), lang(33), lang(26)], self.images.image("ucursos"), "about", 115, 220, \
                 AUTOR_NAME, AUTOR_NAME_EMAIL, PROGRAM_VERSION])
            e.w.mainloop(1);
            del e

        def _ayuda(a=None, b=None):  # Carga la ayuda
            e = Pop([lang(18), self.images.image("help"), "ayuda", 400, 600, FOLDER_DOCUMENTS + "ayuda.txt"])
            e.w.mainloop(1);
            del e

        def _configuracion():  # Configuración del programa
            print "configurar"

        def _changelog():  # Carga la lista de cambios
            e = Pop(
                [lang(21), self.images.image("page_gear"), "changelog", 400, 600, FOLDER_DOCUMENTS + "changelog.txt"])
            e.w.mainloop(1);
            del e

        def _licence():  # Carga la licencia
            e = Pop(
                [lang(34), self.images.image("licence"), "licence", 400, 600, FOLDER_DOCUMENTS + "/licence/GNU.txt"])
            e.w.mainloop(1);
            del e

        # Creación de la ventana
        self.root = Tk()
        self.root.title(PROGRAM_TITLE)  # título
        self.root.minsize(width=PROGRAM_SIZE[0], height=PROGRAM_SIZE[1])  # tamaño mínimo y máximo
        self.root.resizable(width=False, height=False)
        self.root.geometry(
            '%dx%d+%d+%d' % (PROGRAM_SIZE[0], PROGRAM_SIZE[1], (self.root.winfo_screenwidth() - PROGRAM_SIZE[0]) / 2, \
                             (self.root.winfo_screenheight() - PROGRAM_SIZE[1] - 50) / 2))
        self.root.focus_force()
        self.root.focus()

        # Creación de variables
        self.activecurso = False  # define si se ha cargado ya un curso
        self.browser = Browser()  # instancio el objeto browser
        self.browser.addHeaders(HREF_HEADERS)  # se agregan los headers al browser
        self.files = []  # matriz de información de los archivos
        self.filesTitles = [
            [lang(69), 230],  # titulo
            [lang(40), 40],  # tipo
            [lang(39), 60],  # peso
            [lang(43), 80],  # descargas totales
            [lang(70), 180],  # publicador
            [lang(71), 40],  # año de la publicación
            [lang(52), 70],  # semestre de la publicación
            [lang(53), 70],  # sección de la publicación
            [lang(73), 120],  # fecha de la publicación
            ["", 0],  # link
            ["", 0],  # tipo de subida
            ["", 0]  # tipo de material
        ]
        self.fonts = [tkFont.Font(family="Helvetica", size=9, weight=tkFont.BOLD),
                      tkFont.Font(family="Helvetica", size=8), \
                      tkFont.Font(family="Helvetica", size=8, weight=tkFont.BOLD), tkFont.Font(family="Arial", size=12), \
                      tkFont.Font(family="Arial", size=13), tkFont.Font(family="Arial", size=11), \
                      tkFont.Font(family="Helvetica", size=10, slant="italic"), tkFont.Font(family="Arial", size=9)]
        self.loaded = False  # define si se ha iniciado la sesión
        print lang(11), ;
        self.images = UfilesTextures([lang(13), lang(12)]);
        print lang(12)  # cargo las texturas

        # Genero la interfaz gráfica
        print lang(56), ;
        self.root.iconbitmap(self.images.image("ucursos"))  # icono del programa
        self.menubar = Menu(self.root)  # creación de menús
        self.root.config(menu=self.menubar, cursor="arrow")
        self.archivomenu = Menu(self.menubar, tearoff=0)
        self.archivomenu.add_command(label=lang(10), command=self.iniciar_sesion, accelerator="Ctrl+I")
        self.archivomenu.add_command(label=lang(15), command=self.cerrar_sesion, accelerator="Ctrl+L")
        self.archivomenu.add_separator()
        self.archivomenu.add_command(label=lang(16), command=_configuracion, accelerator="Ctrl+C")
        self.archivomenu.add_command(label=lang(17), command=self.salir, accelerator="Ctrl+S")
        self.archivomenu.entryconfig(1, state=DISABLED)
        self.menubar.add_cascade(label=lang(14), menu=self.archivomenu)
        self.vermenu = Menu(self.menubar, tearoff=0)
        self.ayudamenu = Menu(self.menubar, tearoff=0)
        self.ayudamenu.add_command(label=lang(19), command=_about)
        self.ayudamenu.add_command(label=lang(18), command=_ayuda, accelerator="Ctrl+A")
        self.ayudamenu.add_command(label=lang(21), command=_changelog)
        self.ayudamenu.add_command(label=lang(20), command=_licence)
        self.menubar.add_cascade(label=lang(18), menu=self.ayudamenu)
        self.root.config(border=0, padx=0)
        self.background = Canvas(self.root, width=PROGRAM_SIZE[0], height=PROGRAM_SIZE[1], bd=-10, state=DISABLED,
                                 highlightthickness=0)
        self.background.pack(padx=0, pady=0, fill=BOTH, anchor=NW)
        self.background.create_image(PROGRAM_SIZE[0] / 2, PROGRAM_SIZE[1] / 2,
                                     image=self.images.image(CONFIGURATION_DATA[1]));
        self.background.update()
        self.box_login();
        print lang(12)

        # Establezco los eventos del programa
        def _callback(event): self.root.focus()

        print lang(57), ;
        self.root.bind("<Control-A>", _ayuda);
        self.root.bind("<Control-a>", _ayuda)
        self.root.bind("<Control-C>", _configuracion);
        self.root.bind("<Control-c>", _configuracion)
        self.root.bind("<Control-I>", self.iniciar_sesion);
        self.root.bind("<Control-i>", self.iniciar_sesion)
        self.root.bind("<Control-L>", self.cerrar_sesion);
        self.root.bind("<Control-l>", self.cerrar_sesion)
        self.root.bind("<Control-S>", self.salir);
        self.root.bind("<Control-s>", self.salir)
        self.root.bind("<F1>", _ayuda)
        self.root.protocol("WM_DELETE_WINDOW", self.salir);
        print lang(12);
        print lang(59) + "\n"  # evento de salida
        self.background.bind("<Button-1>", partial(_callback))

        # Solo para probar
        self.loaded = True;
        self.box_main();
        HREF_UPASAPORTE = "x";
        self.test = True

    def box_error(self, code, string=""):  # Crea un diálogo de error
        self.root.config(menu=self.menubar, cursor="arrow")
        if string == "":
            box = Pop([[lang(25), lang(26)], self.images.image("exclamation"), "aviso", 70, 300, getError(code)])
        else:
            box = Pop([[lang(25), lang(26)], self.images.image("exclamation"), "aviso", 70, 300,
                       getError(code).format(string)])
        box.w.mainloop(1)
        del box

    def box_main(self):  # Carga la página principal
        if self.loaded:
            self.background.delete(ALL)
            self.loginPassword.pack_forget()
            self.loginPassword.pack_forget()
            self.background.create_image(PROGRAM_SIZE[0] / 2, PROGRAM_SIZE[1] / 2,
                                         image=self.images.image("background2"))
            self.background.config(bd=-10)
            self.background.create_text(40, 120, text=lang(35), font=self.fonts[0], anchor=W, fill="#cb9a2d")
            self.background.update()
            self.box_menu_cursos()

    def box_menu_cursos(self):  # Dibujar los cursos del usuario
        def color_config(widget, color, event):
            widget.configure(foreground=color)

        if self.loaded:  # Si se ha iniciado sesión
            print lang(58), ;
            cursos = getCursos(self.browser.getHtml())
            font = tkFont.Font(family="Helvetica", size=9)
            height = 148
            cursos.sort()
            for curso in cursos:
                cursosFrame = Frame(self.background)
                curso_label = Label(cursosFrame, text=curso[0], font=self.fonts[1], \
                                    anchor=W, fg="#858585", background="#FBFBFB", activeforeground="#CCCCCC",
                                    takefocus=True, width=24, cursor="hand2")
                curso_label.pack(fill=X, anchor=W)
                curso_label.bind("<Button-1>", partial(self.cargar_curso, curso[0], curso[2], curso[1]))
                curso_label.bind("<Button-3>", partial(openWeb, curso[1]))
                curso_label.bind("<Enter>", partial(color_config, curso_label, "#666666"))
                curso_label.bind("<Leave>", partial(color_config, curso_label, "#858585"))
                self.background.create_image(92, height, image=self.images.image("menu_cursos_box"))
                self.background.create_window(100, height, window=cursosFrame)
                self.background.create_image(13, height, image=self.images.image("cursos"))
                height += 27
            self.background.update();
            print lang(12)

    def box_login(self):  # Dibuja el box de login
        def _clearLogin():  # Limpia las cajas de texto de login
            self.loginPassword.delete(0, END)
            self.loginUsername.delete(0, END)
            self.loginUsername.focus()

        def _send(event):  # Envia el formulario
            self.iniciar_sesion("box")

        def _toPassword(event):  # Mueve el cursor al recuadro de contraseñas
            self.loginPassword.focus()

        self.background.delete(ALL)
        self.root.title(PROGRAM_TITLE)
        self.background.create_image(PROGRAM_SIZE[0] / 2, PROGRAM_SIZE[1] / 2,
                                     image=self.images.image(CONFIGURATION_DATA[1]))
        loginFrame = Frame(self.background)
        self.loginUsername = Entry(loginFrame, font=self.fonts[4], relief=GROOVE, fg="#333333")
        self.loginUsername.pack(pady=1)
        self.loginPassword = Entry(loginFrame, font=self.fonts[4], relief=GROOVE, fg="#333333");
        self.loginPassword.pack(pady=1)
        self.loginPassword.config(show="*")
        self.loginPassword.bind("<Return>", _send)
        self.loginUsername.bind("<Return>", _toPassword)
        self.loginUsername.focus()
        self.background.create_text(PROGRAM_SIZE[0] / 2 - 155, PROGRAM_SIZE[1] / 2 - 36, text=lang(22),
                                    font=self.fonts[3], anchor=W)
        self.background.create_text(PROGRAM_SIZE[0] / 2 - 155, PROGRAM_SIZE[1] / 2 - 12, text=lang(23),
                                    font=self.fonts[3], anchor=W)
        button1Frame = Frame(self.background)
        bt_iniciarSesion = Button(button1Frame, text=lang(10), font=tkFont.Font(family="Times", size=12), \
                                  relief=GROOVE, command=lambda: self.iniciar_sesion("box"), bg="#F6F7F8").pack(padx=0,
                                                                                                                pady=0)
        self.background.create_window(PROGRAM_SIZE[0] / 2 + 75 - 125, PROGRAM_SIZE[1] / 2 + 45, window=button1Frame)
        button2Frame = Frame(self.background)
        bt_iniciarReset = Button(button2Frame, text=lang(24), font=tkFont.Font(family="Times", size=12), \
                                 relief=GROOVE, command=_clearLogin, bg="#F6F7F8").pack(padx=0, pady=0)
        self.background.create_window(PROGRAM_SIZE[0] / 2 + 50, PROGRAM_SIZE[1] / 2 + 45, window=button2Frame)
        self.background.create_window(PROGRAM_SIZE[0] / 2 + 55, PROGRAM_SIZE[1] / 2 - 25, window=loginFrame)
        self.background.update()

    def buscar(self, term):  # Función de buscar
        if self.loaded:  # Si se ha iniciado la sesión
            if self.activecurso:  # Si se ha cargado un curso
                if term != "" and term != lang(64):  # Si el término a buscar no está vacío
                    term = term.lower()
                    query = []
                    id_pack = 0
                    for k in self.files:  # Recorro los archivos
                        id_elem = 0
                        for j in k:  # Recorro los packs
                            for t in range(0, 8):  # Recorro las propiedades del archivo
                                if term in str(j[t]).lower():  # Si se encuentra el término
                                    query.append([id_pack, id_elem]);
                                    break
                            id_elem += 1
                        id_pack += 1
                    if len(query) != 0:  # Si se han encontrado archivos
                        self.filtrar("ver:busqueda", query)
                    else:  # Si no se encontró nada
                        box = Pop(
                            [[lang(49), lang(26)], self.images.image("folder_explore"), "aviso", 70, 300, lang(74)])
                        box.w.mainloop(1)
                        del box

    def cargar_curso(self, nombre, codigo, link, event):  # Carga un curso
        def _delete_files_frame():  # Elimina el frame de los archivos
            self.background.delete('buscar_form');
            self.background.delete('buscar_lupa')
            self.background.delete('button1');
            self.background.delete('button1:txt')
            self.background.delete('button2');
            self.background.delete('button2:txt')
            self.background.delete('button3');
            self.background.delete('button3:txt')
            self.background.delete('button4');
            self.background.delete('button4:txt')
            self.background.delete('button5');
            self.background.delete('button5:txt')
            self.background.delete('files');
            self.background.delete('files_background')
            self.background.update()

        def _delete_loading_widget():  # Elimina el frame "cargando..."
            self.background.delete('loading_text');
            self.background.delete('loading_widget');
            self.background.delete('loading_background')

        def _files_frame():  # Dibuja el frame de los archivos
            def _buscar(form, event):  # Buscar un string
                self.buscar(form.get())  # busco el contenido
                form.delete(0, END)  # elimino el mensaje anterior
                form.insert(0, lang(64))  # inserto el mensaje de inicio
                self.root.focus_force()  # saco el foco al buscador

            def _del_search_form(form, event):  # Borra el contenido del campo de texto si este no ha sido escrito
                if form.get() == lang(64):  # Si coincide con el mensaje de entrada
                    form.delete(0, END)  # se borra su contenido
                    form.insert(0, "")  # inserto un campo vacío

            def _filtrar(filtro, event):  # Filtrar los resultados
                print filtro

            def _quit_focus(form, event):  # Quita el foco al buscador
                self.background.focus_force()  # quito el foco
                if form.get() == "":  # Si no tenia algo escrito
                    form.delete(0, END)  # borro el contenido
                    form.insert(0, lang(64))  # inserto el contenido por defecto

            self.background.create_image(490, 230, image=self.images.image("box_curso"), tag='files_background')
            frame_buscar = Frame(self.background)
            buscar_input = Entry(frame_buscar, width=30, font=self.fonts[6], fg="#6A7180", relief=GROOVE, bd=0,
                                 highlightbackground="#CCCCCC", \
                                 highlightcolor="#969CEB", highlightthickness=1, bg="#F6F7F8")
            buscar_input.pack()
            buscar_input.insert(0, lang(64))
            buscar_button_Frame = Frame(self.background, bg="#CCCCCC", cursor="hand2")
            canvas_buscarf = Canvas(buscar_button_Frame, width=20, height=20, bd=-2, bg="#F6F7F8", highlightthickness=0)
            canvas_buscarf.pack(anchor=NW, padx=0, pady=0)
            canvas_buscarf.create_image(9, 9, image=self.images.image("lupa"))
            button1 = Frame(self.background, cursor="hand2", bg="#E0E0E0")
            button1_canvas = Canvas(button1, width=42, height=38, bd=-3, bg="#E0E0E0", highlightthickness=0)
            button1_canvas.pack()
            button1_canvas.create_image(20, 17, image=self.images.image("material_docente"))
            button2 = Frame(self.background, cursor="hand2", bg="#E0E0E0")
            button2_canvas = Canvas(button2, width=42, height=38, bd=-3, bg="#E0E0E0", highlightthickness=0)
            button2_canvas.pack()
            button2_canvas.create_image(20, 17, image=self.images.image("material_alumnos"))
            button3 = Frame(self.background, cursor="hand2", bg="#E0E0E0")
            button3_canvas = Canvas(button3, width=42, height=38, bd=-3, bg="#E0E0E0", highlightthickness=0)
            button3_canvas.pack()
            button3_canvas.create_image(20, 17, image=self.images.image("calendario"))
            button4 = Frame(self.background, cursor="hand2", bg="#E0E0E0")
            button4_canvas = Canvas(button4, width=42, height=38, bd=-3, bg="#E0E0E0", highlightthickness=0)
            button4_canvas.pack()
            button4_canvas.create_image(20, 17, image=self.images.image("integrantes"))
            button5 = Frame(self.background, cursor="hand2", bg="#E0E0E0")
            button5_canvas = Canvas(button5, width=42, height=38, bd=-3, bg="#E0E0E0", highlightthickness=0)
            button5_canvas.pack()
            button5_canvas.create_image(20, 17, image=self.images.image("cursos_departamento"))
            button1_canvas.bind("<Button-1>", partial(self.filtrar, "material:docente"))
            button2_canvas.bind("<Button-1>", partial(self.filtrar, "material:alumnos"))
            button3_canvas.bind("<Button-1>", partial(self.filtrar, "fecha:todo"))
            button4_canvas.bind("<Button-1>", partial(self.filtrar, "integrantes:todo"))
            button5_canvas.bind("<Button-1>", partial(self.filtrar, "ver:filtros"))
            canvas_buscarf.bind("<Button-1>", partial(_buscar, buscar_input))
            buscar_input.bind("<Escape>", partial(_quit_focus, buscar_input))
            buscar_input.bind("<FocusIn>", partial(_del_search_form, buscar_input))
            buscar_input.bind("<FocusOut>", partial(_quit_focus, buscar_input))
            buscar_input.bind("<Return>", partial(_buscar, buscar_input))
            self.background.create_window(PROGRAM_SIZE[0] - 112, 15, window=frame_buscar, tag='buscar_form')
            self.background.create_window(PROGRAM_SIZE[0] - 16, 14, window=buscar_button_Frame, tag='buscar_lupa')
            self.background.create_window(PROGRAM_SIZE[0] - 525, 26, window=button1, tag='button1')
            self.background.create_text(PROGRAM_SIZE[0] - 546, 45, text=lang(41), font=self.fonts[7], fill="#666666",
                                        width=50, anchor=NW, tag="button1:txt")
            self.background.create_window(PROGRAM_SIZE[0] - 463, 26, window=button2, tag='button2')
            self.background.create_text(PROGRAM_SIZE[0] - 487, 45, text=lang(42), font=self.fonts[7], fill="#666666",
                                        width=50, anchor=NW, tag="button2:txt")
            self.background.create_window(PROGRAM_SIZE[0] - 400, 26, window=button3, tag='button3')
            self.background.create_text(PROGRAM_SIZE[0] - 419, 45, text=lang(66), font=self.fonts[7], fill="#666666",
                                        width=50, anchor=NW, tag="button3:txt")
            self.background.create_window(PROGRAM_SIZE[0] - 335, 26, window=button4, tag='button4')
            self.background.create_text(PROGRAM_SIZE[0] - 364, 45, text=lang(67), font=self.fonts[7], fill="#666666",
                                        width=60, anchor=NW, tag="button4:txt")
            self.background.create_window(PROGRAM_SIZE[0] - 270, 26, window=button5, tag='button5')
            self.background.create_text(PROGRAM_SIZE[0] - 299, 45, text=lang(68), font=self.fonts[7], fill="#666666",
                                        width=62, anchor=NW, tag="button5:txt")

        def _loading_frame():  # Dibuja el frame "cargando"
            self.background.create_image(490, -150, image=self.images.image("box_curso"), tag='loading_background')
            frame_loading = Frame(self.background)
            ttk.Progressbar(frame_loading, mode='indeterminate', name='bp', phase=0, length=200).pack()
            bp = frame_loading.nametowidget('bp')
            bp.start(20)
            self.background.create_window(PROGRAM_SIZE[0] / 2 + 130, 49, window=frame_loading, tag='loading_text')
            self.background.create_text(PROGRAM_SIZE[0] / 2 - 57, 50, text=lang(63), font=self.fonts[5], anchor=W,
                                        tag='loading_widget')
            self.background.focus_force()
            self.background.update()

        if self.loaded:  # si se ha iniciado sesión
            print lang(62).format(codigo),
            if self.activecurso: _delete_files_frame()
            if True:  # Se carga el curso
                _loading_frame()
                (ano, semestre, seccion) = obtenerInfoLink(link)
                link = transformarLink(link)
                codigo = codigo.strip().split("-")[0]
                consultas = 0  # cantidad de consultas realizadas
                for y in range(U_CURSOS_Y, ano + 1):  # Se recorren los años
                    for s in range(1, 3):  # Se recorren los semestres
                        if y == ano and s == 2: break
                        for mat in U_CURSOS_MT:
                            for sec in range(1, U_CURSOS_SC + 1):  # Se recorren las secciones
                                consultas += 1
                                query_link = link + "/" + str(y) + "/" + str(s) + "/" + codigo + "/" + str(
                                    sec) + "/" + mat
                                if self.browser.abrirLink(
                                        query_link) == BR_ERRORxNO_ACCESS_WEB:  # Si no se pudo cargar la web
                                    break
                                estado_carga = comprobarCarga(self.browser.getHtml())
                                if estado_carga == FILESXERROR_NOEXIST:
                                    break
                                elif estado_carga == FILESXERROR_NOPERM:
                                    pass
                                elif estado_carga == FILESXERROR_NOFILES:
                                    pass
                                elif estado_carga == FILESXNO_ERROR:
                                    self.files.append(
                                        buscarArchivos(self.browser.getHtml(), query_link, y, s, sec, mat))
                                time.sleep(0.5)
                _delete_loading_widget()
                _files_frame()
                self.activecurso = True;
                print lang(12)
                self.root.title(nombre)
                self.filtrar("material:docente")
                print lang(65, str(consultas))  # cantidad total de consultas web
            else:  # error al cargar el curso
                _delete_loading_widget()
                _delete_files_frame()
                self.root.title(PROGRAM_TITLE)
                self.box_error(CURSOSxERROR_CANT_LOAD_CURSO, codigo);
                print lang(61)
                self.activecurso = False;
                return

    def cerrar_sesion(self, event=None):  # Cerrar la sesion
        if self.loaded:  # Si hay una sesión activa
            e = Pop([[lang(15), lang(27), lang(28), lang(29), lang(30)], self.images.image("help"), "preguntarSNC", \
                     75, 250, True])  # Se pregunta si quiere guardar o no
            e.w.mainloop(1)
            if e.sent:  # Se procede en función de la respuesta
                if e.values[0] == "si":  # Se cierra la sesión
                    self.archivomenu.entryconfig(1, state=DISABLED);
                    self.browser.clearCookies()
                    self.box_login()
                    self.activecurso = False;
                    self.loaded = False
                    return True
                else:
                    return False
            del e
        else:
            return True

    def filtrar(self, filtro, event=None):  # Se filtran y dibujan los resultados según un filtro
        def _descargar(event):  # Descargar un archivo tras hacerle click o apretar enter
            try:
                item = tree.selection()[0]
                values = tree.item(item, "values")
                for i, elem in enumerate(values):
                    if i == len(values) - 1:  # se obtiene el link
                        openWeb(elem, None)
            except:
                pass

        def _sortby(tree, col, descending):  # Función que ordena las columnas segun orden
            data = [(tree.set(child, col), child) for child in tree.get_children('')]  # Obtiene los datos para ordenar
            new_data = []
            for (text, id) in data:
                if text != '': new_data.append((text, id))
            del data
            new_data.sort(reverse=descending)  # se reordenan y modifican
            for indx, item in enumerate(new_data): tree.move(item[1], '', indx)
            tree.heading(col, command=lambda col=col: _sortby(tree, col, int(not descending)))

        if self.loaded:  # Si se ha iniciado sesión
            if self.activecurso:  # Si se ha cargado un curso
                self.background.delete('files')  # borro la actual lista
                self.background.update()
                filtros = []
                nombre_columnas = []
                # Filtros disponibles:
                #    0 : titulo
                #    1 : tipo
                #    2 : peso
                #    3 : descargas totales
                #    4 : publicador
                #    5 : año de la publicación
                #    6 : semestre de la publicación
                #    7 : sección de la publicación
                #    8 : fecha de la publicación
                #    9 : link
                #    10: tipo de subida {query:profesor/auxiliar/alumno, indx:0} #INDEX
                #    11: seccion de material {query:material_alumno,material_docente, indx:1} #INDEX
                if filtro == "material:docente":
                    filtros = [0, 4, 1, 5, 6, 7]; tipo = "material_docente"
                elif filtro == "material:alumnos":
                    filtros = [0, 1, 4, 5, 6, 7]; tipo = "material_alumnos"
                elif filtro == "fecha:todo":
                    filtros = [8, 6, 7, 0, 4, 1]
                elif filtro == "integrantes:todo":
                    filtros = [4, 0, 1, 2]
                elif filtro == "ver:filtros":
                    return
                elif filtro == "ver:busqueda":
                    filtros = [0, 1, 4, 5, 6, 7, 8, 2, 3]
                for i in filtros: nombre_columnas.append(self.filesTitles[i][0])
                frame = Frame(self.background, border=-1, height=349, padx=0)
                frame.pack_propagate(0)
                tree = ttk.Treeview(frame, columns=nombre_columnas, show="headings", padding=-2)
                tree.pack(fill=BOTH, expand=1)
                tree.bind("<Return>", _descargar)
                tree.bind("<Double-1>", _descargar)
                vsb = Scrollbar(tree, orient="vertical")
                hsb = Scrollbar(tree, orient="horizontal")
                tree.configure(yscrollcommand=vsb.set)
                tree.configure(xscrollcommand=hsb.set)
                vsb.config(command=tree.yview)
                hsb.config(command=tree.xview)
                vsb.pack(fill=Y, anchor=E, expand=1)
                hsb.pack(fill=X, anchor=S, expand=0)
                for col in nombre_columnas:
                    if col != "":
                        tree.heading(col, text=col, command=lambda c=col: _sortby(tree, c, 0))
                        tree.column(col, width=tkFont.Font().measure(col.title()))
                cant = 0
                if filtro != "ver:busqueda":
                    for j in range(len(self.files)):
                        for k in range(len(self.files[j])):
                            data = []
                            for i in filtros:
                                data.append(str(self.files[j][k][i]).decode('utf-8', errors='ignore'))
                            data.append(self.files[j][k][9])  # se agrega el link
                            tree.insert('', 'end', values=data)
                            cant += 1
                else:
                    for elem in event:
                        data = []
                        for i in filtros: data.append(
                            str(self.files[elem[0]][elem[1]][i]).decode('utf-8', errors='ignore'))
                        data.append(self.files[elem[0]][elem[1]][9])  # se agrega el link
                        tree.insert('', 'end', values=data)
                        cant += 1
                for f in range(len(filtros)): tree.column(f, width=self.filesTitles[filtros[f]][1])
                self.background.create_window(470, 255, window=frame, width=560, tag='files')
                if 15 - cant >= 0:
                    for i in range(15 - cant): tree.insert('', 'end', values='')
                tree.insert('', 'end', values='')
                try:
                    item = tree.get_children()[0]
                    tree.selection_set(item)
                    tree.focus_set()
                    tree.focus(item)
                except:
                    pass

    def iniciar_sesion(self, event=None):  # Iniciar sesión
        if event == "box":
            pass  # si se inició sesión desde el box
        else:  # Si se inició sesión desde un atajo de teclado o desde el menú
            self.cerrar_sesion()
            return
        print lang(60), ;
        login = [self.loginUsername.get(), self.loginPassword.get()]
        if self.browser.abrirLink(HREF_UPASAPORTE) == BR_ERRORxNO_ACCESS_WEB:  # Si no se pudo cargar la web
            self.box_error(BR_ERRORxNO_ACCESS_WEB);
            print lang(61);
            return
        self.browser.selectFormById(0)
        self.browser.submitForm(LOGIN_FORM, login)  # se envian los datos
        estado = comprobarLogin(self.browser.getHtml())
        if estado is not True:
            self.box_error(estado); print lang(61); return  # si no se inició la sesión
        else:  # si la sesión se inició
            print lang(12)
            self.archivomenu.entryconfig(1, state=NORMAL)
            self.loaded = True  # indica que se ha iniciado la sesión
            self.loginPassword.destroy()
            self.loginUsername.destroy()
            self.box_main()
            self.root.config(cursor="arrow")

    def salir(self):  # Salir del programa
        self.browser.clearCookies()
        os.system("taskkill /PID " + str(os.getpid()) + " /F")


# Inicio del programa
if __name__ == '__main__':
    loadLang(True)  # se carga el idioma por defecto
    window = Ufiles()
    window.root.mainloop(0)
