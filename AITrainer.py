import cv2
import numpy as np
import time
import PoseModule as pm
import ExercicesModule as exercise
import jsonExercises as alma



ejercicios = exercise.ejercicios()
alm = alma.almacenamiento()


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

def comenzar_sesion(listaEj, nomSesion, nomUsuario, camara):

    _ = input("Dale a ENTER para continuar")
    if(listaEj != []):
        for ejercicio in listaEj:                   #Cada ejercicio es una lista con el nombre del ejercicio y otro parametros
            nomEj = ejercicio[0]
            repes = ejercicio[1]
            series = ejercicio[2]
            t_pos = ejercicio[3]
            descanso = ejercicio[4]
            ejecutar_ejercicio(nombre=nomEj, repes=repes, series=series, tiempo_pos=t_pos, 
                               nomSesion=nomSesion, nomUsuario=nomUsuario, camara=camara)
            print(f"Descansemos {descanso} segunditos")
            time.sleep(descanso)
    else: 
        print("Lista vacia")

def ejecutar_ejercicio(nombre=None, repes=1, series=1, tiempo_pos=0, nomSesion="default", nomUsuario="usuario", camara=0):
    #exercise = em.ejercicios()
    
    if nombre == None:
        nombre = input("Ingrese el nombre del ejercicio a ejecutar: ")
    ejercicio = alm.seleccionar_ejercicio(nombre)
    listaCuerpo = alm.partesCuerpo[ejercicio["cuerpo"]]
    ejercicios.ejercicio_generico(total_reps=repes, total_series=series, cuerpo=listaCuerpo, posicion=ejercicio["posicion"],
                                t_posicion=tiempo_pos ,anguloIni=ejercicio["anguloIni"], anguloFin=ejercicio["anguloFin"],
                                nombreEj=nombre, nombreSesion=nomSesion, nomUsuario=nomUsuario,camara=camara)
        


def main():
    # lista = crear_sesion()
    # comenzar_sesion(listaEj=lista)
    alm.ejecutar_ejercicio("Pesas del brazo derecho")
    #ejercicios.pesas_brazoIzquierdo(5)


if __name__ == "__main__":
    main()


