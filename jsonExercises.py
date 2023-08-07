import cv2
import json
import ExercicesModule as em
from datetime import date


class almacenamiento():

    partesCuerpo= {
        "brazoderecho": [11,13,15],
        "brazoizquierdo": [12, 14, 16],
        "piernaderecha": [23, 25, 27],
        "piernaizquierda": [24, 26, 28],
        "caderaD": [11, 23, 25],
        "caderaI": [12, 24, 26]
    }

    

    def cargar_sesiones(self):
        try:
            with open('sesiones.json', 'r') as archivo:
                sesiones = json.load(archivo)
        except FileNotFoundError:
            sesiones = {}
        
        return sesiones

    def cargar_ejercicio(self):
        try:
            with open('ejercicios.json', 'r') as archivo:
                ejercicios = json.load(archivo)
        except FileNotFoundError:
            ejercicios = {"ejercicios" :[]}
        
        return ejercicios
    
    def cargar_soluciones(self):
        try:
            fecha = date.today().strftime('%d-%m-%y')
            nombreArchivo = "resultados_" + fecha + ".json"
            with open(nombreArchivo, 'r') as archivo:
                resultados = json.load(archivo)
        except FileNotFoundError:
            resultados = {}
        
        return resultados


    def crear_ejercicio(self, nombre, cuerpo, pos, angIni, angFin):
        ejercicio = {}

        ejercicio["nombre"] = nombre
        #ejercicio["descripcion"] = input('Ingrese una descripción del ejercicio: ')

        #ejercicio['TiempoMax'] = int(input('Ingrese el tiempo del ejercicio (segundos): '))

        #ejercicio["TiempoEjercicio"] = int(input('Ingrese el tiempo en el que tiene que mantener una posición (segundos): '))

        #ejercicio["series"] = int(input('Ingrese el numero de series: '))

        #ejercicio["repeticiones"] = int(input('Ingrese el numero de repeticiones: '))

        ejercicio["cuerpo"] = cuerpo

        ejercicio["posicion"] = pos

        ejercicio["anguloIni"] = angIni
        ejercicio["anguloFin"] = angFin

        return ejercicio
    
    def guardar_sesion(self, sesion, nomSesion):
        dicSesiones = self.cargar_sesiones()     
        if nomSesion not in dicSesiones:
            dicSesiones.update(sesion)
            with open('sesiones.json', 'w') as archivo:
                json.dump(dicSesiones, archivo, indent=4)
    

    def guardar_ejercicio(self, ejercicio):

        mismoNombre = False
        nomNuevoEj = ejercicio["nombre"]
        dicEjercicios = self.cargar_ejercicio()
        for dic in dicEjercicios["ejercicios"]:
            if  nomNuevoEj == dic["nombre"]: 
                mismoNombre = True
                break

        if not mismoNombre:
            dicEjercicios["ejercicios"].append(ejercicio)
            with open('ejercicios.json', 'w') as archivo:
                json.dump(dicEjercicios, archivo, indent=4)


    def guardar_resultados(self, nombreEj, nombreSesion, tiempo, total, F1, F2, F3):
        resultados = self.cargar_soluciones()
        res = {}
        res["nombre"] = nombreEj
        res["TiempoTotal"] = tiempo
        res["EjCompletos"] = total
        res["EjF1"] = F1
        res["EjF2"] = F2
        res["EjF3"] = F3

        nomS = nombreSesion
        if(nomS not in resultados):
            resultados[nomS] = [res]
        else:
            resultados[nomS].append(res)


        fecha = date.today().strftime('%d-%m-%y')
        nombreArchivo = "resultados_" + fecha + ".json"
        with open(nombreArchivo, 'w') as archivo:
            json.dump(resultados, archivo, indent=4)


    def seleccionar_ejercicio(self, nombreEj=None):
        listaEjercicios = self.cargar_ejercicio()
        
        for dic in listaEjercicios["ejercicios"]:
            if dic["nombre"] == nombreEj:
                return dic
        return None
    


def main():
    alm = almacenamiento()
    ejercicios = alm.cargar_ejercicio()
    # nuevo_ejercicio = alm.crear_ejercicio()
    # ejercicios["ejercicios"].append(nuevo_ejercicio)
    # alm.guardar_ejercicio(ejercicios)
    ej = alm.seleccionar_ejercicio()
    alm.ejecutar_ejercicio(ej)


if __name__ == "__main__":
    main()