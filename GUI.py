from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont
import jsonExercises as je
import AITrainer as ait
from datetime import datetime
import json
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2




class TrainerApp(tk.Tk):
     
     

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["Inicio_Registro"] = Inicio_Registro(parent=container, controller=self)
        self.frames["IniciarSesion"] = IniciarSesion(parent=container, controller=self)
        self.frames["Registro"] = Registro(parent=container, controller=self)
        self.frames["StartPageUser"] = StartPageUser(parent=container, controller=self)
        self.frames["StartPageAdmin"] = StartPageAdmin(parent=container, controller=self)
        self.frames["GraficasResultadosUser"] = GraficasResultadosUser(parent=container, controller=self)
        self.frames["GraficasResultadosAdmin"] = GraficasResultadosAdmin(parent=container, controller=self)
        self.frames["Sesion"] = Sesion(parent=container, controller=self)
        self.frames["Editor"] = Editor(parent=container, controller=self)
        self.frames["InicioSesionEj"] = InicioSesionEj(parent=container, controller=self)

        self.frames["Inicio_Registro"].grid(row=0, column=0, sticky="nsew")
        self.frames["IniciarSesion"].grid(row=0, column=0, sticky="nsew")
        self.frames["Registro"].grid(row=0, column=0, sticky="nsew")
        self.frames["StartPageUser"].grid(row=0, column=0, sticky="nsew")
        self.frames["StartPageAdmin"].grid(row=0, column=0, sticky="nsew")
        self.frames["GraficasResultadosUser"].grid(row=0, column=0, sticky="nsew")
        self.frames["GraficasResultadosAdmin"].grid(row=0, column=0, sticky="nsew")
        self.frames["Sesion"].grid(row=0, column=0, sticky="nsew")
        self.frames["Editor"].grid(row=0, column=0, sticky="nsew")
        self.frames["InicioSesionEj"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("Inicio_Registro")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise() 

    def set_sesionActual(self, nombreUsuario):
        self.nomSesionActual = nombreUsuario
    
    def get_sesionActual(self):
        return self.nomSesionActual

    def actualizarUser(self):
        ini = self.frames["GraficasResultadosUser"]
        ini.actu_lista()

    def actualizarAdmin(self):
        ini = self.frames["GraficasResultadosAdmin"]
        ini.actu_lista()

    def list_ports(self):
    # """
    # Test the ports and returns a tuple with the available ports and the ones that are working.
    # """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        available_ports = []
        while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
            camera = cv2.VideoCapture(dev_port)
            if not camera.isOpened():
                non_working_ports.append(dev_port)
                print("Port %s is not working." %dev_port)
            else:
                is_reading, img = camera.read()
                w = camera.get(3)
                h = camera.get(4)
                if is_reading:
                    print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                    working_ports.append((dev_port,h,w))
                else:
                    print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                    available_ports.append(dev_port)
            dev_port +=1
        return available_ports,working_ports,non_working_ports


class Inicio_Registro(tk.Frame): 
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent) 
        self.controller = controller 

        labelIR = tk.Label(self, text="Aplicación interactiva para rehabilitación y fisioterapia",
                         font=controller.title_font, pady=20, width=55)
        labelIR.grid(row=0, column=0)

        button_inicioS = tk.Button(self, text="Iniciar sesión", pady= 20,
                            command=lambda: controller.show_frame("IniciarSesion"), width=20, font=tkfont.BOLD, border=3)
        button_registro = tk.Button(self, text="Registrarse", pady=20,
                            command=lambda: controller.show_frame("Registro"), width=20, font=tkfont.BOLD, border=3)

        button_inicioS.grid(row=1, column=0, pady=30)
        button_registro.grid(row=2, column=0, pady=30)

class IniciarSesion(tk.Frame):

    alm = je.almacenamiento()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller = controller 

        self.nomUsuario = tk.StringVar()
        self.password = tk.StringVar()

        label = tk.Label(self, text="Iniciar sesión",
                         font=controller.title_font, pady=20, width=55)
        label.place(x=0, y=0)

        etiqueta_usu = tk.Label(self, text="Usuario", font=tkfont.NORMAL)
        etiqueta_usu.place(x=375, y=100)
        self.nombre_usuario = tk.Entry(self, textvariable=self.nomUsuario, width=30)
        self.nombre_usuario.place(x=320, y=140)

        etiqueta_psw = tk.Label(self, text="Contraseña", font=tkfont.NORMAL)
        etiqueta_psw.place(x=360, y=200)
        self.nombre_contrasenya = tk.Entry(self, textvariable=self.password, width=30)
        self.nombre_contrasenya.place(x=320, y=240)


        button_atras = tk.Button(self, text="Volver atrás", command=lambda: controller.show_frame("Inicio_Registro"), 
                                 font=tkfont.ITALIC, border=3)
        button_atras.place(x=70, y=400)

        button_paciente = tk.Button(self, text="Iniciar sesión como paciente", command=self.IniSesionUser, 
                                 font=tkfont.ITALIC, border=3)
        button_paciente.place(x=500, y=350)

        button_admin = tk.Button(self, text="Iniciar sesión como administrador", command=self.IniSesionAdmin, 
                                 font=tkfont.ITALIC, border=3)
        button_admin.place(x=500, y=400)

    def IniSesionUser(self):
        usuarios = self.alm.cargar_usuarios()
        
        nombreUsuario = self.nomUsuario.get().strip()
        passwordUsuario = self.password.get().strip()
        users = usuarios["users"]
       
        if nombreUsuario in users and nombreUsuario and passwordUsuario:
            aux = users[nombreUsuario]
            if aux == passwordUsuario:
                self.controller.set_sesionActual(nombreUsuario)
                self.nombre_usuario.delete(0,tk.END)
                self.nombre_contrasenya.delete(0, tk.END)
                self.controller.show_frame("StartPageUser")

    
    def IniSesionAdmin(self):
        usuarios = self.alm.cargar_usuarios()
        
        nombreUsuario = self.nomUsuario.get().strip()
        passwordUsuario = self.password.get().strip()
        admins = usuarios["admins"]
       
        if nombreUsuario in admins and nombreUsuario and passwordUsuario:
            aux = admins[nombreUsuario]
            if aux == passwordUsuario:
                
                self.nombre_usuario.delete(0,tk.END)
                self.nombre_contrasenya.delete(0, tk.END)
                self.controller.show_frame("StartPageAdmin")


class Registro(tk.Frame):

    alm = je.almacenamiento()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.controller = controller 

        self.newUsuario = tk.StringVar()
        self.newPassword = tk.StringVar()

        label = tk.Label(self, text="Registrarse",
                         font=controller.title_font, pady=20, width=55)
        label.place(x=0, y=0)

        etiqueta_usu = tk.Label(self, text="Usuario", font=tkfont.NORMAL)
        etiqueta_usu.place(x=375, y=100)
        self.nombre_usuario = tk.Entry(self, textvariable=self.newUsuario, width=30)
        self.nombre_usuario.place(x=320, y=140)

        etiqueta_psw = tk.Label(self, text="Contraseña", font=tkfont.NORMAL)
        etiqueta_psw.place(x=360, y=200)
        self.nombre_contrasenya = tk.Entry(self, textvariable=self.newPassword, width=30)
        self.nombre_contrasenya.place(x=320, y=240)

        button_atras = tk.Button(self, text="Volver atrás", command=lambda: controller.show_frame("Inicio_Registro"), 
                                 font=tkfont.ITALIC, border=3)
        button_atras.place(x=70, y=400)

        button_paciente = tk.Button(self, text="Registrarse como paciente", command=self.registroUser, 
                                 font=tkfont.ITALIC, border=3)
        button_paciente.place(x=500, y=350)

        button_admin = tk.Button(self, text="Registrarse como administrador", command=self.registroAdmin, 
                                 font=tkfont.ITALIC, border=3)
        button_admin.place(x=500, y=400)

    def registroUser(self):
        usuarios = self.alm.cargar_usuarios()
        
        nombreUsuario = self.newUsuario.get().strip()
        passwordUsuario = self.newPassword.get().strip()
        users = usuarios["users"]
       
        if nombreUsuario not in users and nombreUsuario and passwordUsuario:
            users[nombreUsuario] = passwordUsuario
            usuarios["users"] = users
            with open('usuarios.json', 'w') as archivo:
                json.dump(usuarios, archivo, indent=4)
                self.nombre_usuario.delete(0,tk.END)
                self.nombre_contrasenya.delete(0, tk.END)
                self.controller.show_frame("Inicio_Registro")

    def registroAdmin(self):
        usuarios = self.alm.cargar_usuarios()
      
        nombreAdmin = self.newUsuario.get().strip()
        passwordAdmin = self.newPassword.get().strip()
        admins = usuarios["admins"]   

        if nombreAdmin not in admins and nombreAdmin and passwordAdmin:
            admins[nombreAdmin] = passwordAdmin
            usuarios["admins"] = admins
            with open('usuarios.json', 'w') as archivo:
                json.dump(usuarios, archivo, indent=4)
                self.nombre_usuario.delete(0,tk.END)
                self.nombre_contrasenya.delete(0, tk.END)
                self.controller.show_frame("Inicio_Registro")


class StartPageUser(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent) 
        self.controller = controller 

        label = tk.Label(self, text="Aplicación interactiva para rehabilitación y fisioterapia",
                         font=controller.title_font, pady=20, width=55)
        label.grid(row=0, column=0)

        # button_sesion = tk.Button(self, text="Crear sesión", pady= 10,
        #                     command=lambda: controller.show_frame("Sesion"), font=tkfont.NORMAL, border=3)
        # button_ejercicio = tk.Button(self, text="Crear ejercicio", pady=10,
        #                     command=lambda: controller.show_frame("Editor"), font=tkfont.NORMAL, border=3)
        button_listaSesiones = tk.Button(self, text="Elegir sesión de ejercicios", pady=10,
                            command=lambda: controller.show_frame("InicioSesionEj"), font=tkfont.NORMAL, border=3)
        button_grafica = tk.Button(self, text="Consultar gráficas de resultados", pady=10,
                            command=self.iniciarGraficas, font=tkfont.NORMAL, border=3)
        button_salir = tk.Button(self, text="Cerrar sesión", pady=10,
                            command=lambda: controller.show_frame("Inicio_Registro"), font=tkfont.BOLD, border=3)

        # button_ejercicio.grid(row=1, column=0, pady=20)
        # button_sesion.grid(row=2, column=0, pady=20)
        button_listaSesiones.grid(row=1, column=0, pady=20 )
        button_grafica.grid(row=2, column=0, pady=20)
        button_salir.grid(row=3, column=0, pady= 50)

    def iniciarGraficas(self):
        self.controller.actualizarUser()
        self.controller.show_frame("GraficasResultadosUser")



class StartPageAdmin(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent) 
        self.controller = controller 

        label = tk.Label(self, text="Aplicación interactiva para rehabilitación y fisioterapia",
                         font=controller.title_font, pady=20, width=55)
        label.grid(row=0, column=0)

        button_sesion = tk.Button(self, text="Crear sesión", pady= 10,
                            command=lambda: controller.show_frame("Sesion"), font=tkfont.NORMAL, border=3)
        button_ejercicio = tk.Button(self, text="Crear ejercicio", pady=10,
                            command=lambda: controller.show_frame("Editor"), font=tkfont.NORMAL, border=3)
        button_grafica = tk.Button(self, text="Consultar gráficas de resultados", pady=10,
                            command=self.iniciarGraficas, font=tkfont.NORMAL, border=3)
        button_salir = tk.Button(self, text="Cerrar sesión", pady=10,
                            command=lambda: controller.show_frame("Inicio_Registro"), font=tkfont.BOLD, border=3)
        # button_listaSesiones = tk.Button(self, text="Elegir sesión de ejercicios", pady=10,
        #                     command=lambda: controller.show_frame("InicioSesionEj"), font=tkfont.NORMAL, border=3)

        button_ejercicio.grid(row=1, column=0, pady=20)
        button_sesion.grid(row=2, column=0, pady=20)
        button_grafica.grid(row=3, column=0, pady=20)
        button_salir.grid(row=4, column=0, pady=30)
        # button_listaSesiones.grid(row=3, column=0, pady=20)


    def iniciarGraficas(self):
        self.controller.actualizarAdmin()
        self.controller.show_frame("GraficasResultadosAdmin")

class GraficasResultadosUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  

        titulo = tk.Label(self, text="Consultar datos", font=controller.title_font, width=55)
        titulo.grid(row=0, column=0, columnspan=10, pady=20)

        # Marco para contener el listbox y la barra de desplazamiento.
        list_frame = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        hscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(list_frame, yscrollcommand=yscrollbar.set, xscrollcommand=hscrollbar.set, width=37, height=15)
        yscrollbar.config(command=self.listbox.yview)
        hscrollbar.config(command=self.listbox.xview)
        # Ubicarla a la derecha.
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame.grid(row=1, column=0, pady=10, columnspan=2, rowspan=5)

        list_frame2 = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar2 = tk.Scrollbar(list_frame2, orient=tk.VERTICAL)
        hscrollbar2 = tk.Scrollbar(list_frame2, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listboxSesiones = tk.Listbox(list_frame2, yscrollcommand=yscrollbar2.set, xscrollcommand=hscrollbar2.set, width=37, height=15)
        yscrollbar2.config(command=self.listboxSesiones.yview)
        hscrollbar2.config(command=self.listboxSesiones.xview)
        # Ubicarla a la derecha.
        yscrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.listboxSesiones.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame2.grid(row=1, column=2, pady=10, columnspan=2, rowspan=5)

        button_mostrarSesiones = tk.Button(self, text="Elegir archivo", command=self.mostrarSesiones, 
                                  font=tkfont.NORMAL, border=3)
        button_mostrarSesiones.grid(row=7, column=0, pady=5)

        button_volver = tk.Button(self, text="Volver al inicio", command=self.volver, 
                                  font=tkfont.NORMAL, border=3)
        button_volver.grid(row=8, column=0, pady=10)

        button_graficaTiempo = tk.Button(self, text="Mostrar tiempos", command=self.graficaTiempos, 
                                  font=tkfont.NORMAL, border=3)
        button_graficaTiempo.grid(row=2, column=4, pady=5)

        button_graficaFases = tk.Button(self, text="Mostrar intentos", command=self.graficaFases, 
                                  font=tkfont.NORMAL, border=3)
        button_graficaFases.grid(row=3, column=4, pady=5)

    def autolabel(self, rects, ax):
    #"""Funcion para agregar una etiqueta con el valor en cada barra"""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
            
    def graficaTiempos(self):
        selected_index = self.listboxSesiones.curselection()
        listaSegundos = []
        listaNombres = []
        if selected_index:
            nombreSesion = self.listboxSesiones.get(selected_index)
            sesion = self.resultados[nombreSesion]
            for ej in sesion:
                listaSegundos.append(ej["TiempoTotal"])
                listaNombres.append(ej["nombre"])
            fig, ax = plt.subplots()
            #Colocamos una etiqueta en el eje Y
            ax.set_ylabel('Segundos')
            #Colocamos una etiqueta en el eje X
            ax.set_title('Tiempo total por ejercicio')
            #Creamos la grafica de barras utilizando ejercicios como eje X y segundos como eje y.
            rects = plt.bar(listaNombres, listaSegundos)

            self.autolabel(rects, ax)
            fig.tight_layout()
            #Finalmente mostramos la grafica con el metodo show()
            plt.show()

    def graficaFases(self):
        selected_index = self.listboxSesiones.curselection()
        listaF1 = []
        listaF2 = []
        listaF3 = []
        listaNombres = []
        if selected_index:
            nombreSesion = self.listboxSesiones.get(selected_index)
            sesion = self.resultados[nombreSesion]
            for ej in sesion:
                listaF1.append(ej["EjF1"])
                listaF2.append(ej["EjF2"])
                listaF3.append(ej["EjF3"])
                listaNombres.append(ej["nombre"])
            fig, ax = plt.subplots()

            x = np.arange(len(listaNombres))
            width = 0.25

            plt.bar(x - width, listaF1, width=width, label='(0,30]')
            plt.bar(x, listaF2, width=width, label='(30,60]')
            plt.bar(x + width, listaF3, width=width, label='(60, 100)')
            #Colocamos una etiqueta en el eje Y
            ax.set_ylabel('Intentos fallidos')
            #Colocamos una etiqueta en el eje X
            ax.set_title('Niveles alcanzados por ejercicio')
            ax.legend()
            ax.set_xticks(x)
            ax.set_xticklabels(listaNombres)
            #Finalmente mostramos la grafica con el metodo show()
            plt.show()

    def mostrarSesiones(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            nombreArchivo = self.listbox.get(selected_index)
            rutaActual = os.path.dirname(os.path.abspath(__file__))
            rutaCarpeta = self.controller.get_sesionActual() + "_Datos"
            archivoFinal = os.path.join(rutaActual, "Datos", rutaCarpeta, nombreArchivo)
            with open(archivoFinal, 'r') as archivo:
                self.resultados = json.load(archivo)
            self.listboxSesiones.delete(0, tk.END)
            for sesion in self.resultados.keys():
                self.listboxSesiones.insert(tk.END, sesion)

    def volver(self):
        self.listboxSesiones.delete(0,tk.END)
        self.resultados={}
        self.controller.show_frame("StartPageUser")


    def actu_lista(self):
        rutaActual = os.path.dirname(os.path.abspath(__file__))
        rutaCarpeta = self.controller.get_sesionActual() + "_Datos"
        carpeta = os.path.join(rutaActual, "Datos", rutaCarpeta)
        listaArchivados = self.listbox.get(0,tk.END)
        self.listbox.delete(0, tk.END)
        archivos = [archivo for archivo in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, archivo))]
        for arch in archivos:
            self.listbox.insert(tk.END, arch)
            


class GraficasResultadosAdmin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  

        titulo = tk.Label(self, text="Consultar datos", font=controller.title_font, width=55)
        titulo.grid(row=0, column=0, columnspan=10, pady=20)

        # Marco para contener el listbox y la barra de desplazamiento.
        list_frame = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        hscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(list_frame, yscrollcommand=yscrollbar.set, xscrollcommand=hscrollbar.set, width=37, height=15)
        yscrollbar.config(command=self.listbox.yview)
        hscrollbar.config(command=self.listbox.xview)
        # Ubicarla a la derecha.
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame.grid(row=1, column=0, pady=10, rowspan=5)

        list_frame2 = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar2 = tk.Scrollbar(list_frame2, orient=tk.VERTICAL)
        hscrollbar2 = tk.Scrollbar(list_frame2, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listboxArchivos = tk.Listbox(list_frame2, yscrollcommand=yscrollbar2.set, xscrollcommand=hscrollbar2.set, width=37, height=15)
        yscrollbar2.config(command=self.listboxArchivos.yview)
        hscrollbar2.config(command=self.listboxArchivos.xview)
        # Ubicarla a la derecha.
        yscrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar2.pack(side=tk.BOTTOM, fill=tk.X)
        self.listboxArchivos.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame2.grid(row=1, column=1, pady=10, rowspan=5)

        list_frame3 = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar3 = tk.Scrollbar(list_frame3, orient=tk.VERTICAL)
        hscrollbar3 = tk.Scrollbar(list_frame3, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listboxSesiones = tk.Listbox(list_frame3, yscrollcommand=yscrollbar3.set, xscrollcommand=hscrollbar3.set, width=37, height=15)
        yscrollbar3.config(command=self.listboxSesiones.yview)
        hscrollbar3.config(command=self.listboxSesiones.xview)
        # Ubicarla a la derecha.
        yscrollbar3.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar3.pack(side=tk.BOTTOM, fill=tk.X)
        self.listboxSesiones.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame3.grid(row=1, column=3, pady=10, rowspan=5)

        button_mostrarDias = tk.Button(self, text="Elegir carpeta", command=self.mostrarDias, 
                                  font=tkfont.NORMAL, border=3)
        button_mostrarDias.grid(row=6, column=0, pady=5)

        button_mostrarSesiones = tk.Button(self, text="Elegir archivo", command=self.mostrarSesiones, 
                                  font=tkfont.NORMAL, border=3)
        button_mostrarSesiones.grid(row=6, column=1, pady=5)

        button_volver = tk.Button(self, text="Volver al inicio", command=self.volver, 
                                  font=tkfont.NORMAL, border=3)
        button_volver.grid(row=8, column=0, pady=5)

        button_graficaTiempo = tk.Button(self, text="Mostrar tiempos", command=self.graficaTiempos, 
                                  font=tkfont.NORMAL, border=3)
        button_graficaTiempo.grid(row=6, column=3, pady=5)

        button_graficaFases = tk.Button(self, text="Mostrar intentos", command=self.graficaFases, 
                                  font=tkfont.NORMAL, border=3)
        button_graficaFases.grid(row=7, column=3, pady=5)


    def autolabel(self, rects, ax):
    #"""Funcion para agregar una etiqueta con el valor en cada barra"""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')



    def graficaTiempos(self):
        selected_index = self.listboxSesiones.curselection()
        listaSegundos = []
        listaNombres = []
        if selected_index:
            nombreSesion = self.listboxSesiones.get(selected_index)
            sesion = self.resultados[nombreSesion]
            for ej in sesion:
                listaSegundos.append(ej["TiempoTotal"])
                listaNombres.append(ej["nombre"])
            fig, ax = plt.subplots()
            #Colocamos una etiqueta en el eje Y
            ax.set_ylabel('Segundos')
            #Colocamos una etiqueta en el eje X
            ax.set_title('Tiempo total por ejercicio')
            #Creamos la grafica de barras utilizando ejercicios como eje X y segundos como eje y.
            rects = plt.bar(listaNombres, listaSegundos)

            self.autolabel(rects, ax)
            fig.tight_layout()
            #Finalmente mostramos la grafica con el metodo show()
            plt.show()

    def graficaFases(self):
        selected_index = self.listboxSesiones.curselection()
        listaF1 = []
        listaF2 = []
        listaF3 = []
        listaNombres = []
        if selected_index:
            nombreSesion = self.listboxSesiones.get(selected_index)
            sesion = self.resultados[nombreSesion]
            for ej in sesion:
                listaF1.append(ej["EjF1"])
                listaF2.append(ej["EjF2"])
                listaF3.append(ej["EjF3"])
                listaNombres.append(ej["nombre"])
            fig, ax = plt.subplots()

            x = np.arange(len(listaNombres))
            width = 0.25

            plt.bar(x - width, listaF1, width=width, label='N1 (0,30]')
            plt.bar(x, listaF2, width=width, label='N2 (30,60]')
            plt.bar(x + width, listaF3, width=width, label='N3 (60, 100)')
            #Colocamos una etiqueta en el eje Y
            ax.set_ylabel('Intentos fallidos')
            #Colocamos una etiqueta en el eje X
            ax.set_title('Niveles alcanzados por ejercicio')
            ax.legend()
            ax.set_xticks(x)
            ax.set_xticklabels(listaNombres)
            #Finalmente mostramos la grafica con el metodo show()
            plt.show()


    def mostrarSesiones(self):
        selected_index = self.listboxArchivos.curselection()
        if selected_index:
            nombreArchivo = self.listboxArchivos.get(selected_index)
            rutaActual = os.path.dirname(os.path.abspath(__file__))
            rutaCarpeta = self.nombreCarpeta
            archivoFinal = os.path.join(rutaActual, "Datos", rutaCarpeta, nombreArchivo)
            with open(archivoFinal, 'r') as archivo:
                self.resultados = json.load(archivo)
            self.listboxSesiones.delete(0, tk.END)
            for sesion in self.resultados.keys():
                self.listboxSesiones.insert(tk.END, sesion)


    def mostrarDias(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.nombreCarpeta = self.listbox.get(selected_index)
            rutaActual = os.path.dirname(os.path.abspath(__file__))
            carpetaFinal = os.path.join(rutaActual, "Datos", self.nombreCarpeta)
            archivos = [archivo for archivo in os.listdir(carpetaFinal) if os.path.isfile(os.path.join(carpetaFinal, archivo))]
            self.listboxArchivos.delete(0, tk.END)
            for arch in archivos:
                self.listboxArchivos.insert(tk.END, arch)


    def volver(self):
        self.listboxArchivos.delete(0, tk.END)
        self.listboxSesiones.delete(0,tk.END)
        self.resultados={}
        self.nombreCarpeta=""
        self.controller.show_frame("StartPageAdmin")


    def actu_lista(self):
        rutaActual = os.path.dirname(os.path.abspath(__file__))
        carpeta = os.path.join(rutaActual, "Datos")
        listaCarpetas = self.listbox.get(0,tk.END)
        carpetas = [nombre for nombre in os.listdir(carpeta) if os.path.isdir(os.path.join(carpeta, nombre))
                    and nombre not in listaCarpetas]

        for carp in carpetas:
            self.listbox.insert(tk.END, carp)

class InicioSesionEj(tk.Frame):


    alm = je.almacenamiento()
    camaras=[]
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  

        titulo = tk.Label(self, text="Empezar sesión de ejercicios", font=controller.title_font, width=55)
        titulo.grid(row=0, column=0, columnspan=10, pady=20)

        list_frame = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        hscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(list_frame, yscrollcommand=yscrollbar.set, xscrollcommand=hscrollbar.set, width=37, height=15
                                  , exportselection=False)
        yscrollbar.config(command=self.listbox.yview)
        hscrollbar.config(command=self.listbox.xview)
        # Ubicarla a la derecha.
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame.grid(row=1, column=4, pady=10, columnspan=2, rowspan=5)

        dic = self.alm.cargar_sesiones()

        for d in dic.keys():
            self.listbox.insert(tk.END, d)

        av,self.work,nwork = self.controller.list_ports()

        for w in self.work:
            cam= str(w[0]) + " (" + str(w[1]) + " x " + str(w[2]) +")"
            self.camaras.append(cam)

        etiqueta_camara= tk.Label(self, text="Elegir cámara:", font=tkfont.NORMAL, width=10)
        etiqueta_camara.grid(row=1, column=6, columnspan=3, padx=10, sticky=tk.EW)
        self.camara_combobox = ttk.Combobox(self, state="readonly", values = self.camaras, font=tkfont.NORMAL)
        self.camara_combobox.grid(row=2, column=6, columnspan=3, padx=10, sticky=tk.EW)

        button_comenzar = tk.Button(self, text="Comenzar sesión de ejercicios", command=self.iniciarSesionEj, 
                                    font=tkfont.NORMAL, border=3)
        button_comenzar.grid(row = 11, column=4)

        button_volver = tk.Button(self, text="Volver al inicio", command=lambda: controller.show_frame("StartPageUser"), 
                                  font=tkfont.NORMAL, border=3)
        button_volver.grid(row=12, column=4, pady=20)



    def iniciarSesionEj(self):
        aux = self.listbox.curselection()
        sesion = self.listbox.get(aux)
        nombreUsuario = self.controller.get_sesionActual()
        index = self.camara_combobox.current()

        if(aux and index != -1):
            dicSesiones = self.alm.cargar_sesiones()
            listaEjercicios = dicSesiones[sesion]
            now = datetime.now()
            horaActual = now.strftime('%H:%M')
            nombreSesionActual = sesion + "-" + horaActual
            indexCam = self.work[index][0]
            ait.comenzar_sesion(listaEjercicios, nombreSesionActual, nombreUsuario, indexCam)
                 

class Editor(tk.Frame):

    alm = je.almacenamiento()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.nomEj = tk.StringVar()

        self.mediaPipeImagen = tk.PhotoImage(file="Mediapipe_Pose (2).gif")
        imagen_label = tk.Label(self, image=self.mediaPipeImagen)
        imagen_label.grid(row=0, column=0, rowspan=20, padx=10, pady=10, sticky= tk.NSEW)

        etiqueta_entry = tk.Label(self, text="Escribe el nombre del ejercicio:" , font=tkfont.NORMAL)
        etiqueta_entry.grid(row=0, column=1, columnspan=2, padx=10, sticky=tk.EW)
        nombre_ejercicio = tk.Entry(self, textvariable=self.nomEj, font=tkfont.NORMAL)
        nombre_ejercicio.grid(row=1, column=1, columnspan=2)

        etiqueta_cuerpocb= tk.Label(self, text="Parte del cuerpo a ejercitar:", font=tkfont.NORMAL)
        etiqueta_cuerpocb.grid(row=2, column=1, columnspan=2, padx=10, sticky=tk.EW)
        self.cuerpo_combobox = ttk.Combobox(self, state="readonly", values = [ "Brazo derecho (11,13,15)","Brazo izquierdo (12,14,16)", 
                                                                              "Pierna derecha (23,25,27)", "Pierna izquierda (24,26,28)",
                                                                              "CaderaD (11,23,25)", "CaderaI (12,24,26)"], font=tkfont.NORMAL)
        self.cuerpo_combobox.grid(row= 3, column=1, columnspan=2 )

        self.anguloIniVar = tk.IntVar()
        etiqueta_anguloIni = tk.Label(self, text="Ángulo inicial", font=tkfont.NORMAL)
        etiqueta_anguloIni.grid(row=4, column=1, padx=10, sticky=tk.W)
        spinbox_anguloIni = tk.Spinbox(self,from_=0, to=180, textvariable= self.anguloIniVar, width=7, state="readonly", 
                                       wrap=True, font=tkfont.NORMAL)
        spinbox_anguloIni.grid(row=5, column=1, padx=10, sticky=tk.W)

        self.anguloFinVar = tk.IntVar()
        etiqueta_anguloFin = tk.Label(self, text="Ángulo final", font=tkfont.NORMAL)
        etiqueta_anguloFin.grid(row=4, column=2, padx=10, sticky=tk.W)
        spinbox_anguloFin = tk.Spinbox(self,from_=0, to=180, textvariable= self.anguloFinVar, width=7, state="readonly", 
                                       wrap=True, font=tkfont.NORMAL)
        spinbox_anguloFin.grid(row=5, column=2, padx=10, sticky=tk.W)

        etiqueta_poscb= tk.Label(self, text="Posición para hacer el ejercicio:", font=tkfont.NORMAL)
        etiqueta_poscb.grid(row=6, column=1, columnspan=2, padx=10, sticky=tk.EW)
        self.pos_combobox = ttk.Combobox(self, state="readonly", values = ["De perfil", "De frente", "Tumbado de perfil"], font=tkfont.NORMAL)
        self.pos_combobox.grid(row= 7, column=1, columnspan=2 )

        boton_regresoE = tk.Button(self, text="Volver al inicio",
                           command=lambda: controller.show_frame("StartPageAdmin"), font=tkfont.NORMAL, border=3)
        boton_regresoE.grid(row=11, column=1, columnspan=2)

        boton_crear = tk.Button(self, text="Crear ejercicio",
                           command=self.guardar_ejercicio, font=tkfont.NORMAL, border=3)
        boton_crear.grid(row=10, column=1, columnspan=2)


    def guardar_ejercicio(self):
        nom = self.nomEj.get().strip()  #Aseguro que haya algo escrito
        cuerpo = self.cuerpo_combobox.get()
        angIni = self.anguloIniVar.get()
        angFin = self.anguloFinVar.get()
        pos = self.pos_combobox.current()
        if nom and cuerpo and angIni != angFin and pos != -1:
            NuevoEjercicio = self.alm.crear_ejercicio(cuerpo=cuerpo, angIni=angIni, angFin=angFin, 
                                     pos=pos)
            self.alm.guardar_ejercicio(nombre=nom, ejercicio=NuevoEjercicio)
            self.controller.show_frame("StartPageAdmin")


class Sesion(tk.Frame):

    ejerciciosSesion = []

    alm = je.almacenamiento()


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Crear sesión", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=0, columnspan=10, pady=20)

        list_frame = tk.Frame(self, padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        hscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listboxOpciones = tk.Listbox(list_frame, yscrollcommand=yscrollbar.set, xscrollcommand=hscrollbar.set, width=30, height=15)
        yscrollbar.config(command=self.listboxOpciones.yview)
        hscrollbar.config(command=self.listboxOpciones.xview)
        # Ubicarla a la derecha.
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listboxOpciones.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame.grid(row=1, column=0, pady=10, columnspan=2, rowspan=10)

        # Marco para contener el listbox y la barra de desplazamiento.
        list_frame1 = tk.Frame(self, height=500 , padx=20)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar1 = tk.Scrollbar(list_frame1, orient=tk.VERTICAL)
        hscrollbar1 = tk.Scrollbar(list_frame1, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(list_frame1, yscrollcommand=yscrollbar1.set, xscrollcommand=hscrollbar1.set, width=30, height=15)
        yscrollbar1.config(command=self.listbox.yview)
        hscrollbar1.config(command=self.listbox.xview)
        # Ubicarla a la derecha.
        yscrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar1.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame1.grid(row=1, column=2, pady=10, rowspan=10)

        dic = self.alm.cargar_ejercicio()

        for d in dic.keys():
            self.listboxOpciones.insert(tk.END, d)

        btn_sesion = tk.Button(self, text="Guardar sesión", command=self.guardar_sesion, font=tkfont.BOLD)
        btn_sesion.grid(row=10, column=3, columnspan=2)


        button = tk.Button(self, text="Volver al inicio",
                           command=lambda: controller.show_frame("StartPageAdmin"), font= tkfont.NORMAL)
        button.grid(row=14, column=3, padx=20)

        boton_add_to_list = tk.Button(self, text="Añadir a la lista",
                           command=self.listaEjercicios, width=20, border=3)
        boton_add_to_list.grid(row=15, column=0, columnspan=2)

        boton_subir = tk.Button(self, text="Subir elemento",
                           command=self.subir_elemento)
        boton_subir.grid(row=4, column=3)

        boton_bajar = tk.Button(self, text="Bajar elemento",
                           command=self.bajar_elemento)
        boton_bajar.grid(row=5, column=3)

        boton_eliminar = tk.Button(self,text="Eliminar elemento",
                           command=self.eliminar_elemento)
        boton_eliminar.grid(row=11, column=2)

        self.series = tk.IntVar()
        etiqueta_series = tk.Label(self, text="Nº de series")
        etiqueta_series.grid(row=11, column=1, padx=10, sticky=tk.W)
        spinbox_series = tk.Spinbox(self,from_=1, to=50, textvariable= self.series, width=7, state="readonly", wrap=True)
        spinbox_series.grid(row=12, column=1, padx=10, pady = 10, sticky=tk.W)

        self.repes = tk.IntVar()
        etiqueta_repes = tk.Label(self, text="Nº de repeticiones")
        etiqueta_repes.grid(row=11, column=0, padx=10, sticky=tk.W)
        spinbox_repes = tk.Spinbox(self,from_=1, to=50, textvariable= self.repes, width=7, state="readonly", wrap=True)
        spinbox_repes.grid(row=12, column=0, padx=10, pady = 10, sticky=tk.W)

        self.segundosDescanso = tk.IntVar()
        etiqueta_descanso = tk.Label(self, text="Tiempo de descanso (segundos)")
        etiqueta_descanso.grid(row=13, column=1, padx=10, sticky=tk.W)
        spinbox_descanso = tk.Spinbox(self,from_=1, to=60, textvariable= self.segundosDescanso, width=7, state="readonly", wrap=True)
        spinbox_descanso.grid(row=14, column=1, padx=10, pady = 10, sticky=tk.W)

        self.segundosHold = tk.IntVar()
        etiqueta_hold = tk.Label(self, text="Tiempo posición (segundos)")
        etiqueta_hold.grid(row=13, column=0, padx=10, sticky=tk.W)
        spinbox_hold = tk.Spinbox(self,from_=0, to=60, textvariable= self.segundosHold, width=7, state="readonly", wrap=True)
        spinbox_hold.grid(row=14, column=0, padx=10, pady = 10, sticky=tk.W)

        self.nomSesion = tk.StringVar()
        etiqueta_entry = tk.Label(self, text="Escribe el nombre de la sesión:")
        etiqueta_entry.grid(row=8, column=3, columnspan=2, padx=10, sticky=tk.EW)
        nombre_ejercicio = tk.Entry(self, textvariable=self.nomSesion)
        nombre_ejercicio.grid(row=9, column=3, columnspan=2)



    def eliminar_elemento(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.listbox.delete(selected_index)
            self.ejerciciosSesion.pop(selected_index[0])

    def subir_elemento(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index > 0:
                item = self.listbox.get(selected_index)
                self.listbox.delete(selected_index)
                self.listbox.insert(selected_index - 1, item)
                self.listbox.selection_clear(0, tk.END)
                self.listbox.select_set(selected_index - 1)

                aux = self.ejerciciosSesion[selected_index-1]
                self.ejerciciosSesion[selected_index-1] = self.ejerciciosSesion[selected_index]
                self.ejerciciosSesion[selected_index] = aux

    def bajar_elemento(self): 
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < self.listbox.size() - 1:
                item = self.listbox.get(selected_index)
                self.listbox.delete(selected_index)
                self.listbox.insert(selected_index + 1, item)
                self.listbox.selection_clear(0, tk.END)
                self.listbox.select_set(selected_index + 1)

                aux = self.ejerciciosSesion[selected_index+1]
                self.ejerciciosSesion[selected_index+1] = self.ejerciciosSesion[selected_index]
                self.ejerciciosSesion[selected_index] = aux

#La sesión se guarda como una lista compuesta por el nombre (0), las repeticiones (1), las series (2), el tiempo en el que 
#mantener la posición (3) y el tiempo de desacnso tras la actividad (4)
    def listaEjercicios(self):
            nomSeleccionada = self.listboxOpciones.curselection()
            if(nomSeleccionada):
                ejercicio = self.listboxOpciones.get(nomSeleccionada)
                self.listbox.insert(tk.END, ejercicio)
                repes = self.repes.get()
                series = self.series.get()
                hold = self.segundosHold.get()
                descanso = self.segundosDescanso.get()
                ejercicio = [ejercicio, repes, series, hold, descanso]
                self.ejerciciosSesion.append(ejercicio)

    
    def guardar_sesion(self):

        nomSesion = self.nomSesion.get().strip()
        listaSesion = self.ejerciciosSesion
        if nomSesion and listaSesion:
            sesion = {nomSesion: listaSesion}
            self.alm.guardar_sesion(sesion, nomSesion)
            self.controller.show_frame("StartPageAdmin")




def main():
    app = TrainerApp()
    app.title("TFG")
    app.mainloop()

if __name__ == "__main__":
    main()

