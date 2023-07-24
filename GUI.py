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

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Sesion"].grid(row=0, column=0, sticky="nsew")
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

        button1 = tk.Button(self, text="Organizar sesión",
                            command=lambda: controller.show_frame("Sesion"))
        button2 = tk.Button(self, text="Crear ejercicio",
                            command=lambda: controller.show_frame("Editor"))
        button1.pack()
        button2.pack()

class Sesion(tk.Frame):

    variables = []
    opciones = []

    alm = je.almacenamiento()


    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Crear sesión", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        checkbox_frame = tk.Frame(self.canvas, padx=20)
        scrollbar = tk.Scrollbar(checkbox_frame, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y', padx=15)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.create_window((0, 0), window=checkbox_frame, anchor='nw')

        dic = self.alm.cargar_ejercicio()

        for d in dic["ejercicios"]:
            self.opciones.append(d["nombre"])
  
        for opcion in self.opciones:
            var = tk.BooleanVar()
            self.variables.append(var)
            
            checkbox = tk.Checkbutton(checkbox_frame, text=opcion, variable=var)
            checkbox.pack(anchor='w')

        btn_imprimir = tk.Button(self, text="Imprimir selección", command=self.comenzar_sesion)
        btn_imprimir.pack(pady=10)


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

       
        checkbox_frame.bind('<Configure>', self.on_configure)

    
    def comenzar_sesion(self):
        listaEjercicios = []
        for i, var in enumerate(self.variables):
            if(var.get()):
                listaEjercicios.append(self.opciones[i])
        print(listaEjercicios)
        ait.comenzar_sesion(listaEjercicios)


# root = tk.Tk()

# root.geometry("400x100")


# boton_sesion = tk.Button(root, text="Organizar sesión ejercicios", width=25, height=4)
# #boton_sesion.grid(row=0, column=0, padx=10, pady=10)
# boton_sesion.pack(side=tk.LEFT, padx=20)

# boton_ejercicio = tk.Button(root, text="Crear nuevo ejercicio", width=20, height=4)
# #boton_sesion.grid(row=0, column=1, padx=10, pady=10)
# boton_ejercicio.pack(side=tk.RIGHT, padx=20)


# botonSesion = Button(root, text="Btono")

# botonSesion.grid(row=2, column=1)

#root.mainloop()

def main():
    app = TrainerApp()
    app.mainloop()

if __name__ == "__main__":
    main()

