import cv2
import numpy as np
import time
import PoseModule as pm
import ExercicesModule as em
import jsonExercises as je






ejercicios = em.ejercicios()
alm = je.almacenamiento()




#ejercicios.pesas_brazoIzquierdo(5)

#ejercicios.estiramiento(5)

#ejercicios.pesas_cadaBrazo(5)

#ejercicios.estiramiento_brazo(5)

def crear_sesion():
    listaEj = []
    seguir = True
    while seguir:
        nombreEjercicio = input("Ingrese el nombre del ejercicio a ejecutar: ")
        if nombreEjercicio == "exit":
            seguir = False
            break       
        listaEj.append(nombreEjercicio)
    return listaEj

def comenzar_sesion(listaEj):

    _ = input("Dale a ENTER para continuar")
    if(listaEj != []):
        for ejercicio in listaEj:
            alm.ejecutar_ejercicio(nombre=ejercicio)
            print("Descansemos 10 segunditos")
            time.sleep(10)
    else: 
        print("Lista vacia")


def main():
    # lista = crear_sesion()
    # comenzar_sesion(listaEj=lista)
    alm.ejecutar_ejercicio("Pesas del brazo derecho")


if __name__ == "__main__":
    main()


