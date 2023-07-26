import cv2
import json
import ExercicesModule as em

class almacenamiento():

    partesCuerpo= {
        "brazoderecho": [11,13,15],
        "brazoizquierdo": [12, 14, 16],
        "piernaderecha": [23, 25, 27],
        "piernaizquierda": [24, 26, 28],
        "caderaD": [11, 23, 25],
        "caderaI": [12, 24, 26]
    }

    def cargar_ejercicio(self):
        try:
            with open('ejercicios.json', 'r') as archivo:
                ejercicios = json.load(archivo)
        except FileNotFoundError:
            ejercicios = {"ejercicios" :[]}
        
        return ejercicios
    
    def cargar_soluciones(self):
        try:
            with open('resultados.json', 'r') as archivo:
                resultados = json.load(archivo)
        except FileNotFoundError:
            resultados = {"resultados" :[]}
        
        return resultados


    def crear_ejercicio(self):
        ejercicio = {}

        ejercicio["nombre"] = input('Ingrese el nombre del ejercicio: ')
        #ejercicio["descripcion"] = input('Ingrese una descripción del ejercicio: ')

        #ejercicio['TiempoMax'] = int(input('Ingrese el tiempo del ejercicio (segundos): '))

        ejercicio["TiempoEjercicio"] = int(input('Ingrese el tiempo en el que tiene que mantener una posición (segundos): '))

        ejercicio["series"] = int(input('Ingrese el numero de series: '))

        ejercicio["repeticiones"] = int(input('Ingrese el numero de repeticiones: '))

        ejercicio["cuerpo"] = input('Ingrese la parte del cuerpo que se ejercitará en el ejercicio:')

        ejercicio["posicion"] = int(input('Ingrese la posicion adecuada para el ejercicio:'))

        ejercicio["anguloIni"] = int(input('Ingrese el angulo inicial: '))
        ejercicio["anguloFin"] = int(input('Ingrese el angulo final: '))

        return ejercicio

    def guardar_ejercicio(self, ejercicio):
        with open('ejercicios.json', 'w') as archivo:
            json.dump(ejercicio, archivo, indent=4)


    def guardar_resultados(self, resultados, nombre, tiempo, total, F1, F2, F3):
        resultado = {}
        resultado["nombre"] = nombre
        resultado["TiempoTotal"] = tiempo
        resultado["EjCompletos"] = total
        resultado["EjF1"] = F1
        resultado["EjF2"] = F2
        resultado["EjF3"] = F3

        resultados["resultados"].append(resultado)

        with open('resultados.json', 'w') as archivo:
            json.dump(resultados, archivo, indent=4)


    def seleccionar_ejercicio(self, nombreEj=None):
        listaEjercicios = almacenamiento().cargar_ejercicio()
        
        for dic in listaEjercicios["ejercicios"]:
            if dic["nombre"] == nombreEj:
                return dic
        return None
    
    def ejecutar_ejercicio(self, nombre=None):
        exercise = em.ejercicios()
        if nombre == None:
            nombre = input("Ingrese el nombre del ejercicio a ejecutar: ")
        ejercicio = almacenamiento().seleccionar_ejercicio(nombre)
        listaCuerpo = self.partesCuerpo[ejercicio["cuerpo"]]
        exercise.ejercicio_generico(total_reps=ejercicio["repeticiones"], total_series=ejercicio["series"], cuerpo=listaCuerpo, posicion=ejercicio["posicion"],
                                    t_posicion=ejercicio["tiempoEjercicio"] ,anguloIni=ejercicio["anguloIni"], anguloFin=ejercicio["anguloFin"])
        


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