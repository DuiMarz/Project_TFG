from tkinter import ttk
import tkinter as tk
from tkinter import font as tkfont
import jsonExercises as je
import AITrainer as ait




class TrainerApp(tk.Tk):
     
     

     def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (StartPage):
        #     page_name = F.__name__
        #     frame = F(container, self) # **
        #     self.frames[page_name] = frame # **

        #     # put all of the pages in the same location;
        #     # the one on the top of the stacking order
        #     # will be the one that is visible.
        #     frame.grid(row=0, column=0, sticky="nsew")

        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["Sesion"] = Sesion(parent=container, controller=self)
        self.frames["Editor"] = Editor(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Sesion"].grid(row=0, column=0, sticky="nsew")
        self.frames["Editor"].grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

     def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise() 

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent) 
        self.controller = controller 
        label = tk.Label(self, text="This is the start page",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Organizar sesión",pady= 10,
                            command=lambda: controller.show_frame("Sesion"))
        button2 = tk.Button(self, text="Crear ejercicio", pady=10,
                            command=lambda: controller.show_frame("Editor"))
        button1.pack(side=tk.TOP)
        button2.pack(side=tk.TOP)

class Editor(tk.Frame):

    alm = je.almacenamiento()

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.nomEj = tk.StringVar()

        self.mediaPipeImagen = tk.PhotoImage(file="Mediapipe_Pose (2).gif")
        imagen_label = tk.Label(self, image=self.mediaPipeImagen)
        imagen_label.grid(row=0, column=0, rowspan=20, padx=10, pady=10, sticky= tk.NSEW)

        etiqueta_entry = tk.Label(self, text="Escribe el nombre del ejercicio:")
        etiqueta_entry.grid(row=0, column=1, columnspan=2, padx=10, sticky=tk.EW)
        nombre_ejercicio = tk.Entry(self, textvariable=self.nomEj)
        nombre_ejercicio.grid(row=1, column=1, columnspan=2)

        etiqueta_cuerpocb= tk.Label(self, text="Parte del cuerpo a ejercitar:")
        etiqueta_cuerpocb.grid(row=2, column=1, columnspan=2, padx=10, sticky=tk.EW)
        self.cuerpo_combobox = ttk.Combobox(self, state="readonly", values = [ "brazoderecho","brazoizquierdo", "piernaderecha", "piernaizquierda",
                                                                          "caderaD", "caderaI"])
        self.cuerpo_combobox.grid(row= 3, column=1, columnspan=2 )

        self.anguloIniVar = tk.IntVar()
        etiqueta_anguloIni = tk.Label(self, text="Ángulo inicial")
        etiqueta_anguloIni.grid(row=4, column=1, padx=10, sticky=tk.W)
        spinbox_anguloIni = tk.Spinbox(self,from_=0, to=180, textvariable= self.anguloIniVar, width=7, state="readonly", wrap=True)
        spinbox_anguloIni.grid(row=5, column=1, padx=10, sticky=tk.W)

        self.anguloFinVar = tk.IntVar()
        etiqueta_anguloFin = tk.Label(self, text="Ángulo final")
        etiqueta_anguloFin.grid(row=4, column=2, padx=10, sticky=tk.W)
        spinbox_anguloFin = tk.Spinbox(self,from_=0, to=180, textvariable= self.anguloFinVar, width=7, state="readonly", wrap=True)
        spinbox_anguloFin.grid(row=5, column=2, padx=10, sticky=tk.W)

        etiqueta_poscb= tk.Label(self, text="Posición para hacer el ejercicio:")
        etiqueta_poscb.grid(row=6, column=1, columnspan=2, padx=10, sticky=tk.EW)
        self.pos_combobox = ttk.Combobox(self, state="readonly", values = ["De perfil", "De frente", "Tumbado de perfil"])
        self.pos_combobox.grid(row= 7, column=1, columnspan=2 )

        boton_regresoE = tk.Button(self, text="Volver al inicio",
                           command=lambda: controller.show_frame("StartPage"))
        boton_regresoE.grid(row=8, column=1)

        boton_crear = tk.Button(self, text="Crear ejercicio",
                           command=self.guardar_ejercicio)
        boton_crear.grid(row=8, column=2)


    def guardar_ejercicio(self):
        nom = self.nomEj.get().strip()  #Aseguro que haya algo escrito
        cuerpo = self.cuerpo_combobox.get()
        angIni = self.anguloIniVar.get()
        angFin = self.anguloFinVar.get()
        pos = self.pos_combobox.current()
        if nom and cuerpo and angIni != angFin and pos != -1:
            NuevoEjercicio = self.alm.crear_ejercicio(nombre=nom, cuerpo=cuerpo, angIni=angIni, angFin=angFin, 
                                     pos=pos)
            self.alm.guardar_ejercicio(NuevoEjercicio)
            self.controller.show_frame("StartPage")

            



class Sesion(tk.Frame):


    opciones = []

    ejerciciosSesion = []

    alm = je.almacenamiento()


    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Crear sesión", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=0, columnspan=10, pady=20)

        self.canvas = tk.Canvas(self, width=250)
        self.canvas.grid(row=1, column=0, rowspan=10, columnspan=2)

        radio_frame = tk.Frame(self.canvas, padx=20)
        cb_scrollbar = tk.Scrollbar(radio_frame, command=self.canvas.yview)
        cb_scrollbar.pack(side=tk.RIGHT, fill='y', padx=15)
        self.canvas.configure(yscrollcommand=cb_scrollbar.set)

        self.canvas.create_window((0, 0), window=radio_frame, anchor='nw')

        # Marco para contener el listbox y la barra de desplazamiento.
        list_frame = tk.Frame(self, height=500 , padx=20)
        self.listbox = tk.Listbox(list_frame)
        # Crear una barra de deslizamiento con orientación vertical y horizontal.
        yscrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        hscrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        # Vincularla con la lista.
        self.listbox = tk.Listbox(list_frame, yscrollcommand=yscrollbar.set, xscrollcommand=hscrollbar.set)
        yscrollbar.config(command=self.listbox.yview)
        hscrollbar.config(command=self.listbox.xview)
        # Ubicarla a la derecha.
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)
        list_frame.grid(row=1, column=2, pady=10)

        dic = self.alm.cargar_ejercicio()

        for d in dic["ejercicios"]:
            self.opciones.append(d["nombre"])

        self.op_selec = tk.StringVar()
  
        for opcion in self.opciones:        
            radio_opcion = tk.Radiobutton(radio_frame, text=opcion, variable=self.op_selec, value=opcion)
            radio_opcion.pack(anchor='w')


        btn_imprimir = tk.Button(self, text="Empezar sesión", command=self.iniciar_sesion)
        btn_imprimir.grid(row=2, column=3)


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=4)

        boton_add_to_list = tk.Button(self, text="Añadir a la lista",
                           command=self.listaEjercicios)
        boton_add_to_list.grid(row=2, column=2)

        boton_subir = tk.Button(self, text="Subir elemento",
                           command=self.subir_elemento)
        boton_subir.grid(row=1, column=3)

        boton_bajar = tk.Button(self, text="Bajar elemento",
                           command=self.bajar_elemento)
        boton_bajar.grid(row=1, column=4)

        boton_eliminar = tk.Button(self,text="Eliminar elemento",
                           command=self.eliminar_elemento)
        boton_eliminar.grid(row=3, column=2)

        self.series = tk.IntVar()
        etiqueta_series = tk.Label(self, text="Nº de series")
        etiqueta_series.grid(row=2, column=1, padx=10, sticky=tk.W)
        spinbox_series = tk.Spinbox(self,from_=1, to=50, textvariable= self.series, width=7, state="readonly", wrap=True)
        spinbox_series.grid(row=3, column=1, padx=10, pady = 10, sticky=tk.W)

        self.repes = tk.IntVar()
        etiqueta_repes = tk.Label(self, text="Nº de repeticiones")
        etiqueta_repes.grid(row=2, column=0, padx=10, sticky=tk.W)
        spinbox_repes = tk.Spinbox(self,from_=1, to=50, textvariable= self.repes, width=7, state="readonly", wrap=True)
        spinbox_repes.grid(row=3, column=0, padx=10, pady = 10, sticky=tk.W)

        self.segundosDescanso = tk.IntVar()
        etiqueta_descanso = tk.Label(self, text="Tiempo de descanso (segundos)")
        etiqueta_descanso.grid(row=4, column=1, padx=10, sticky=tk.W)
        spinbox_descanso = tk.Spinbox(self,from_=1, to=60, textvariable= self.segundosDescanso, width=7, state="readonly", wrap=True)
        spinbox_descanso.grid(row=5, column=1, padx=10, pady = 10, sticky=tk.W)

        self.segundosHold = tk.IntVar()
        etiqueta_hold = tk.Label(self, text="Tiempo posición (segundos)")
        etiqueta_hold.grid(row=4, column=0, padx=10, sticky=tk.W)
        spinbox_hold = tk.Spinbox(self,from_=0, to=60, textvariable= self.segundosHold, width=7, state="readonly", wrap=True)
        spinbox_hold.grid(row=5, column=0, padx=10, pady = 10, sticky=tk.W)

        self.nomSesion = tk.StringVar()
        etiqueta_entry = tk.Label(self, text="Escribe el nombre de la sesión:")
        etiqueta_entry.grid(row=6, column=3, columnspan=2, padx=10, sticky=tk.EW)
        nombre_ejercicio = tk.Entry(self, textvariable=self.nomSesion)
        nombre_ejercicio.grid(row=7, column=3, columnspan=2)

       
        radio_frame.bind('<Configure>', self.on_configure)


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


    def listaEjercicios(self):
            nomSeleccionada = self.op_selec.get()
            if(nomSeleccionada):
                self.listbox.insert(tk.END, nomSeleccionada)
                repes = self.repes.get()
                series = self.series.get()
                hold = self.segundosHold.get()
                descanso = self.segundosDescanso.get()
                ejercicio = [nomSeleccionada, repes, series, hold, descanso]
                self.ejerciciosSesion.append(ejercicio)

    
    def iniciar_sesion(self):
        # listaEjercicios = []
        # for i, var in enumerate(self.variables):
        #     if(var.get()):
        #         listaEjercicios.append(self.opciones[i])
        # print(listaEjercicios)
        # ait.comenzar_sesion(listaEjercicios)
        print(self.ejerciciosSesion)




def main():
    app = TrainerApp()
    app.mainloop()

if __name__ == "__main__":
    main()

