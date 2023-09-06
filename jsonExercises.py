import cv2
import json
import ExercicesModule as em
from datetime import date
import os


class almacenamiento():

    partesCuerpo= {
        "Brazo derecho (11,13,15)": [11,13,15],
        "Brazo izquierdo (12,14,16)": [12, 14, 16],
        "Pierna derecha (23,25,27)": [23, 25, 27],
        "Pierna izquierda (24,26,28)": [24, 26, 28],
        "CaderaD (11,23,25)": [11, 23, 25],
        "CaderaI (12,24,26)": [12, 24, 26],
        "Hombro derecho (15,11,23)": [15, 11, 23],
        "Hombro izquierdo (16,12,24)": [16, 12, 24]
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
            ejercicios = {}
        
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

    def cargar_usuarios(self):
        try:
            with open("usuarios.json", 'r') as archivo:
                users = json.load(archivo)
        except FileNotFoundError:
            users = {"users":{}, "admins":{}}
        
        return users

    def crear_ejercicio(self, cuerpo, pos, angIni, angFin):
        ejercicio = {}

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


    def guardar_ejercicio(self, nombre, ejercicio):

        dicEjercicios = self.cargar_ejercicio()
        if nombre not in dicEjercicios:
            dicEjercicios[nombre] = ejercicio
            with open('ejercicios.json', 'w') as archivo:
                json.dump(dicEjercicios, archivo, indent=4)


    def guardar_resultados(self, nombreEj, nombreSesion, tiempo, total, F1, F2, F3, nomUsuario):
        res = {}
        res["nombre"] = nombreEj
        res["TiempoTotal"] = tiempo
        res["EjCompletos"] = total
        res["EjF1"] = F1
        res["EjF2"] = F2
        res["EjF3"] = F3

        nombreCarpeta = nomUsuario + "_Datos"
        rutaActual = os.path.dirname(os.path.abspath(__file__))
        carpetaDestino = os.path.join(rutaActual, "Datos", nombreCarpeta)
        fecha = date.today().strftime('%d-%m-%y')
        nombreArchivo = nomUsuario + "_" + "resultados_" + fecha + ".json"
        rutaFinal = os.path.join(carpetaDestino, nombreArchivo)

        os.makedirs(carpetaDestino, exist_ok=True)

        try:
            with open(rutaFinal, 'r') as archivo:
                resultados = json.load(archivo)
        except FileNotFoundError:
            resultados = {}
        
        nomS = nombreSesion
        if(nomS not in resultados):
            resultados[nomS] = [res]
        else:
            resultados[nomS].append(res)
     
        with open(rutaFinal, 'w') as archivo:
            json.dump(resultados, archivo, indent=4)


    def seleccionar_ejercicio(self, nombreEj=None):
        listaEjercicios = self.cargar_ejercicio()
        ej = listaEjercicios[nombreEj]
        return ej
    


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