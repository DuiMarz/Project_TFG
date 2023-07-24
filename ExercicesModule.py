import cv2
import numpy as np
import time
import jsonExercises as je

import PoseModule as pm


class utilities():

    def repitition_counter(self, count, fase1, fase2, fase3, listSeq, state):  ## Al llegar al estado 0, comprueba el estado de la secuencia
                                                                               ## y actualiza el contador correspondiente

        if state == "S0" and len(listSeq) > 1:
            if len(listSeq)==2:  #[S0, S1]
                fase1 += 1
            elif len(listSeq)==3: #[S0, S1, S2]
                fase2 += 1
            elif len(listSeq)==4:   #[S0, S1, S2, S3]
                fase3 += 1
            elif len(listSeq)==5:   #[S0, S1, S2, S3, S4]
                count += 1

            listSeq.clear()

        return {"count": count, "fase1": fase1, "fase2": fase2, "fase3": fase3 }
    
    def display_rep_count(self, img, count, total_reps, nseries, total_series):            #Dibujo en pantalla en contador de repeticiones
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)) + "/" + str(total_reps), (35, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)
        cv2.putText(img, str(int(nseries)) + "/" + str(total_series), (35, 530), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)
        
    def display_rep_count_movil(self, img, count, total_reps):      #Versión para videos en formato vertical
        cv2.rectangle(img, (0, 550), (250, 820), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)) + "/" + str(total_reps), (35, 730), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 10)
        

    def draw_performance_bar(self, img, per, bar, color, count):    #Dibujo en pantalla la barra de progreso
        cv2.rectangle(img, (1050, 100), (1125, 650), color, 3)
        cv2.rectangle(img, (1050, int(bar)), (1125, 650), color, cv2.FILLED)
        cv2.putText(
            img, f"{int(per)} %", (1030, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
        )

    def draw_performance_bar_movil(self, img, per, bar, color, count):  #Versión para videos en formato vertical
        cv2.rectangle(img, (350, 100), (425, 650), color, 3)
        cv2.rectangle(img, (350, int(bar)), (425, 650), color, cv2.FILLED)
        cv2.putText(
            img, f"{int(per)} %", (325, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
        )
        
    #get_performance_bar_color: Depende del porcentaje de progreso, no solo cambio el color de la barra si no que aprovecho
    # para actualizar el estado en el que estamos en el automata
    def get_performance_bar_color(self, per):   
        color = (0, 205, 205)
        state = "S0"
        if 0 < per <= 30:
            color = (51, 51, 255)
            state = "S1"
        if 30 < per <= 60:
            color = (0, 165, 255)
            state = "S2"
        if 60 <= per <= 100:
            color = (0, 255, 255)
            if per == 100:
                state = "S4"
            else:
                state = "S3"
        return color, state
    

    #update_sequence: actualizo la lista de estados con el estado actual si corresponde (la lista crece de forma ascendente)
    def update_sequence(self, listSeq, currentState):
        if currentState == "S0":
            if currentState not in listSeq and len(listSeq) == 0:
                listSeq.append(currentState)
        elif currentState == "S1":
            if currentState not in listSeq and listSeq.count("S0") == 1:
                listSeq.append(currentState)
        elif currentState == "S2":
            if currentState not in listSeq and listSeq.count("S1") == 1:
                listSeq.append(currentState)
        elif currentState == "S3": 
            if currentState not in listSeq and listSeq.count("S2") == 1:
                listSeq.append(currentState)
        elif currentState == "S4":
            if currentState not in listSeq and listSeq.count("S3") == 1:
                listSeq.append(currentState)
        
    
class ejercicios():

    listaSeq = []

    def ejercicio_generico(self, total_reps, total_series, cuerpo, t_posicion, anguloIni, anguloFin):
        cap = cv2.VideoCapture("pexels-michelangelo-buonarroti.mp4")
        #salida = cv2.VideoWriter('ejercicio_generico.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
        detector = pm.poseDetector()
        success = True

        nseries = 0
        count = 0
        ejCompleto = 0
        countF1 = 0
        countF2 = 0
        countF3 = 0
    
        start = time.process_time()
        while nseries < total_series:
            while count < total_reps:
                success, img = cap.read()
                if not success:
                    break
                img = cv2.resize(img, (1280, 720))
        
                is_person_facing_foward = False
                img = detector.findPose(img, False)
                landmark_list = detector.findPosition(img, False)
                if len(landmark_list) != 0:

                    is_person_facing_foward = detector.persona_de_frente(90)
                    ##Si posicion=tumbado, añadir método para comprobar que la persona esté tumbada
                    if not is_person_facing_foward:
                        angle = detector.findAngle(img, cuerpo[0], cuerpo[1], cuerpo[2])            ## Parte del cuerpo

                        per = np.interp(angle, (anguloIni, anguloFin), (0, 99), period = 360)           ## Angulo inicial y final (205, 335)
                        bar = np.interp(angle, (anguloIni, anguloFin), (650, 100), period = 360)

                        if angle > anguloIni:     #Si anguloIni > anguloFin (e.j. 170 > 60)
                            per = 0
                            bar = 650
                        elif angle < anguloFin:
                            per = 99
                            bar = 100

                        if per >= 99: 
                            if contando == False:
                                tiempoEjercicio = time.process_time()
                                contando = True
                            elif contando == True:
                                t = int(time.process_time() - tiempoEjercicio)
                                if t >= t_posicion:
                                    per = 100
                                if per != 100:    
                                    cv2.putText(img, str(t), (1150, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                                    (255, 0, 0), 10)
                                else:
                                    cv2.putText(img, str(t_posicion), (1150, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                                    (255, 0, 0), 10)      
                        elif per < 99:
                            contando = False

                        

                        color, current_state = utilities().get_performance_bar_color(per)
                        utilities().update_sequence(listSeq= self.listaSeq, currentState= current_state)
                            
                            
                        
                        # When exercise is in start state
                        if per == 0:
                            color = (0, 255, 0)
                            rep = utilities().repitition_counter(count= count,fase1=countF1, fase2=countF2, fase3=countF3, 
                                                                    listSeq=self.listaSeq, state=current_state )
                            #self.listaSeq = []
                            count = rep["count"]
                            countF1 = rep["fase1"]
                            countF2 = rep["fase2"]
                            countF3 = rep["fase3"]



                        utilities().draw_performance_bar(img, per, bar, color, count)

                        utilities().display_rep_count(img, count, total_reps, nseries, total_series)
                    else:
                        print("Ponte de lado, por favor")
                        detector.findAngle(img, 11, 0, 12, True)

                cv2.imshow("Image", img)
                #salida.write(img)
                if cv2.waitKey(1)== ord('q'):
                    break

            nseries += 1
            ejCompleto += count
            count = 0

        time_elapsed = int(time.process_time() - start)
        print(time_elapsed , '\n')
        print('Ejercicio hecho al 100%', ejCompleto, '\n')
        print('Fase1: ', countF1 , '\n')
        print('Fase2: ', countF2 , '\n')
        print('Fase3: ', countF3 , '\n')


        cap.release()
        #salida.release()
        cv2.destroyAllWindows()


    ### EJERCICIO ÚNICAMENTE DE UN BRAZO
    def pesas_brazoIzquierdo(self, total_reps):                                 
        cap = cv2.VideoCapture("pexels-michelangelo-buonarroti.mp4")
        
        salida = cv2.VideoWriter('pesas_brazoIzquierdo.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
        detector = pm.poseDetector()
        success = True
        count = 0
        countF1 = 0
        countF2 = 0
        countF3 = 0
    
        start = time.process_time()

        while count < total_reps:
            success, img = cap.read()
            if not success:
                break
            img = cv2.resize(img, (1280, 720))
 
            is_person_facing_foward = False
            #img = cv2.flip(img,1)
            img = detector.findPose(img, False)
            landmark_list = detector.findPosition(img, False)
            if len(landmark_list) != 0:
                
      
                is_person_facing_foward = detector.persona_de_frente(90)
               
                if not is_person_facing_foward:
                    left_arm_angle = detector.findAngle(img, 11, 13, 15)            ## Parte del cuerpo

                    per = np.interp(left_arm_angle, (155, 20), (0, 100), period = 360)           ## Angulo inicial y final (205, 335)
                    bar = np.interp(left_arm_angle, (155, 20), (650, 100), period = 360)

                    if left_arm_angle > 155:
                        per = 0
                        bar = 650
                    elif left_arm_angle < 20:
                        per = 100
                        bar = 100

                    color, current_state = utilities().get_performance_bar_color(per)
                    utilities().update_sequence(listSeq= self.listaSeq, currentState= current_state)
                    
                
                    # When exercise is in start state
                    if per == 0:
                        color = (0, 255, 0)
                        rep = utilities().repitition_counter(count= count,fase1=countF1, fase2=countF2, fase3=countF3, 
                                                             listSeq=self.listaSeq, state=current_state )
                        #self.listaSeq = []
                        count = rep["count"]
                        countF1 = rep["fase1"]
                        countF2 = rep["fase2"]
                        countF3 = rep["fase3"]

                    utilities().draw_performance_bar(img, per, bar, color, count)

                    utilities().display_rep_count(img, count, total_reps)
                else:
                    print("Ponte de lado, por favor")
                    detector.findAngle(img, 11, 0, 12, True)

            cv2.imshow("Image", img)
            salida.write(img)
            if cv2.waitKey(1)== ord('q'):
                break

        time_elapsed = int(time.process_time() - start)
        nombre = "Ejercicio_Brazo_Izquierdo"
        alm = je.almacenamiento()

        sol = alm.cargar_soluciones()
        alm.guardar_resultados(sol, nombre, time_elapsed, count, countF1, countF2, countF3)
        print(time_elapsed , '\n')
        
        print('Fase1: ', countF1 , '\n')
        print('Fase2: ', countF2 , '\n')
        print('Fase3: ', countF3 , '\n')

        cap.release()
        salida.release()
        cv2.destroyAllWindows()


    ### EJERCICIO DE ESTIRAMIENTO DE UN BRAZO X SEGUNDOS
    def estiramiento_brazo(self, total_reps):                                
        cap = cv2.VideoCapture("pexels-los-muertos-crew-7260756-1920x1080-24fps.mp4")
        
        salida = cv2.VideoWriter('estiramiento_brazo_10segundos.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
        detector = pm.poseDetector()
        success = True
        contando = False
        tiempoEjercicio = 0
        count = 0
        countF1 = 0
        countF2 = 0
        countF3 = 0
    
        start = time.process_time()

        while count < total_reps:
            success, img = cap.read()
            if not success:
                break
            img = cv2.resize(img, (1280, 720))
 
            is_person_facing_foward = False
            #img = cv2.flip(img,1)
            img = detector.findPose(img, False)
            landmark_list = detector.findPosition(img, False)
            if len(landmark_list) != 0:
                
      
                is_person_facing_foward = detector.persona_de_frente(90)
               
                if not is_person_facing_foward:
                    right_arm_angle = detector.findAngle(img, 16, 12, 24)            ## Parte del cuerpo

                    per = np.interp(right_arm_angle, (65, 175), (0, 99))           ## Angulo inicial y final (205, 335)
                    bar = np.interp(right_arm_angle, (65, 175), (650, 100))

                    if per >= 99: 
                        if contando == False:
                            tiempoEjercicio = time.process_time()
                            contando = True
                        elif contando == True:
                            t = int(time.process_time() - tiempoEjercicio)
                            if t >= 5:
                                per = 100
                            if per != 100:    
                                cv2.putText(img, str(t), (1150, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                                (255, 0, 0), 10)
                            else:
                                cv2.putText(img, str(5), (1150, 630), cv2.FONT_HERSHEY_PLAIN, 5,
                                (255, 0, 0), 10)
                            
                    elif per < 99:
                        contando = False     
                    


                    color, current_state = utilities().get_performance_bar_color(per)
                    utilities().update_sequence(listSeq= self.listaSeq, currentState= current_state)
                    
                
                    # When exercise is in start state
                    if per == 0:
                        color = (0, 255, 0)
                        rep = utilities().repitition_counter(count= count,fase1=countF1, fase2=countF2, fase3=countF3, 
                                                             listSeq=self.listaSeq, state=current_state )
                        #self.listaSeq = []
                        count = rep["count"]
                        countF1 = rep["fase1"]
                        countF2 = rep["fase2"]
                        countF3 = rep["fase3"]

                    utilities().draw_performance_bar(img, per, bar, color, count)

                    utilities().display_rep_count(img, count, total_reps)
                else:
                    print("Ponte de lado, por favor")
                    detector.findAngle(img, 11, 0, 12, True)

            cv2.imshow("Image", img)
            salida.write(img)
            if cv2.waitKey(1)== ord('q'):
                break

        time_elapsed = int(time.process_time() - start)
        print(time_elapsed , '\n')
        
        print('Fase1: ', countF1 , '\n')
        print('Fase2: ', countF2 , '\n')
        print('Fase3: ', countF3 , '\n')


        cap.release()
        salida.release()
        cv2.destroyAllWindows()


    ### EJERCICIO DONDE VA CAMBIANDO EL BRAZO A EJERCITAR
    def pesas_cadaBrazo(self, total_reps):                                
        #cap = cv2.VideoCapture("pexels-michelangelo-buonarroti-4159061-1080x1920-24fps.mp4")
        
        cap = cv2.VideoCapture(0)
        salida = cv2.VideoWriter('pesas_cadaBrazo.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
        detector = pm.poseDetector()
        success = True
        count = 0
        countF1 = 0
        countF2 = 0
        countF3 = 0
        cambio = True
    
        start = time.process_time()

        while count < total_reps:
            success, img = cap.read()
            if not success:
                break

            # scale_percent = 40 # percent of original size
            # width = int(img.shape[1] * scale_percent / 100)
            # height = int(img.shape[0] * scale_percent / 100)
            # dim = (width, height)

            # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
            img = cv2.resize(img, (1280, 720))
 
            is_person_facing_foward = False

            img = cv2.flip(img,1)
            img = detector.findPose(img, False)
            landmark_list = detector.findPosition(img, False)
            if len(landmark_list) != 0:

                is_person_facing_foward = detector.persona_de_frente(90)
               
                if not is_person_facing_foward:

                    if cambio:
                        left_arm_angle = detector.findAngle(img, 12, 14, 16)
                        per = np.interp(left_arm_angle, (140, 60), (0, 100), period=360)           ## Angulo inicial y final (205, 335)
                        bar = np.interp(left_arm_angle, (140, 60), (650, 100), period=360)            ## Parte del cuerpo

                        if left_arm_angle > 140:
                            per = 0
                            bar = 650
                        elif left_arm_angle < 60:
                            per = 100
                            bar = 100
                        
                    else:
                        right_arm_angle = detector.findAngle(img, 11, 13, 15)
                        per = np.interp(right_arm_angle, (200, 300), (0, 100))         ## Angulo inicial y final (205, 335)
                        bar = np.interp(right_arm_angle, (200, 300), (650, 100))

                       

                    per = round(per)
                    bar = round(bar)
                        
                    print(left_arm_angle, "\n")
                    #print(per, "\n")
                    color, current_state = utilities().get_performance_bar_color(per)
                    utilities().update_sequence(listSeq= self.listaSeq, currentState= current_state)
                    
                    #print(self.listaSeq, "\n")
                    count_aux = count
                    # When exercise is in start state
                    if per == 0:
                        color = (0, 255, 0)
                        rep = utilities().repitition_counter(count= count,fase1=countF1, fase2=countF2, fase3=countF3, 
                                                             listSeq=self.listaSeq, state=current_state)
                        
                        count = rep["count"]
                        if count_aux is not count:
                            cambio = not cambio
                        countF1 = rep["fase1"]
                        countF2 = rep["fase2"]
                        countF3 = rep["fase3"]

                    utilities().draw_performance_bar(img, per, bar, color, count)

                    utilities().display_rep_count(img, count, total_reps)
                else:
                    print("Ponte de lado, por favor")
                    detector.findAngle(img, 11, 0, 12, True)

            cv2.imshow("Image", img)
            salida.write(img)
            if cv2.waitKey(1)== ord('q'):
                break

        time_elapsed = int(time.process_time() - start)
        print(time_elapsed , '\n')
        
        print('Fase1: ', countF1 , '\n')
        print('Fase2: ', countF2 , '\n')
        print('Fase3: ', countF3 , '\n')


        cap.release()
        salida.release()
        cv2.destroyAllWindows()


    ### EJERCICIO DONDE SE EJERCITAN DOS MIEMBROS DEL CUERPO A LA VEZ
    def estiramiento(self, total_reps):                                
        cap = cv2.VideoCapture("pexels-los-muertos-crew-7260756-1920x1080-24fps.mp4")
        #cap = cv2.VideoCapture(0)
        
        salida = cv2.VideoWriter('ejercicio_estiramiento_dosmiembros.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
        detector = pm.poseDetector()
        success = True
        count = 0
        countF1 = 0
        countF2 = 0
        countF3 = 0
    
        start = time.process_time()

        while count < total_reps:
            success, img = cap.read()
            if not success:
                break
            img = cv2.resize(img, (1280, 720))
 
            
            persona_tumbada = False
            #img = cv2.flip(img,1)
            img = detector.findPose(img, False)
            landmark_list = detector.findPosition(img, False)
            if len(landmark_list) != 0:

                persona_tumbada = detector.persona_tumbada()
               
                if persona_tumbada:
                    right_arm_angle = detector.findAngle(img, 16, 12, 24)            ## Parte del cuerpo
                    right_leg_angle = detector.findAngle(img, 24, 26, 28) 

                    #right_leg_angle = -(right_leg_angle -360)
                    #print('right_leg_angle: ',right_leg_angle, '\n')
                    per1 = np.interp(right_arm_angle, (65, 175), (0, 50))           ## Angulo inicial y final 

                    #print('per1: ',per1, '\n')
                    bar1 = np.interp(right_arm_angle, (65, 175), (650, 375))
                    

                    per2 = np.interp(right_leg_angle, (275, 185), (0, 50), period = 360)   #(90, 175)
                    #print('per2: ', per2, '\n')
                    bar2 = np.interp(right_leg_angle, (275, 185), (0, 275), period= 360)


                    if right_leg_angle < 185:
                        per2 = 50
                        bar2 = 275
                    elif right_leg_angle > 275:
                        per2 = 0
                        bar2 = 0

                    per = round(per1+per2)
                    bar = bar1-bar2

                    color, current_state = utilities().get_performance_bar_color(per)
                    utilities().update_sequence(listSeq= self.listaSeq, currentState= current_state)
                    
                
                    # When exercise is in start state
                    if per == 0:
                        color = (0, 255, 0)
                        rep = utilities().repitition_counter(count= count,fase1=countF1, fase2=countF2, fase3=countF3, 
                                                             listSeq=self.listaSeq, state=current_state )
                        #self.listaSeq = []
                        count = rep["count"]
                        countF1 = rep["fase1"]
                        countF2 = rep["fase2"]
                        countF3 = rep["fase3"]

                    utilities().draw_performance_bar(img, per, bar, color, count)

                    utilities().display_rep_count(img, count, total_reps)
                else:
                    print("Túmbate, por favor")
                    #detector.findAngle(img, 11, 0, 12, True)

            cv2.imshow("Image", img)
            salida.write(img)
            if cv2.waitKey(1)== ord('q'):
                break

        time_elapsed = int(time.process_time() - start)
        print(time_elapsed , '\n')
        
        print('Fase1: ', countF1 , '\n')
        print('Fase2: ', countF2 , '\n')
        print('Fase3: ', countF3 , '\n')


        cap.release()
        salida.release()
        cv2.destroyAllWindows()

    