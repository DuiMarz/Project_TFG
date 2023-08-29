import cv2
import mediapipe as mp
import time
import math
import numpy as np



class poseDetector():

    def __init__(self, mode = False, modelComplexity = 1, smooth = True,
                 detectionConf = 0.5, trackConf = 0.5):
        
        self.mode = mode
        self.modelComplexity = modelComplexity    ## 0(BlazePose GHUM Heavy), 1(BlazePose GHUM Full), 2(BlazePose GHUM Lite)
        self.smooth = smooth
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose= mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode = self.mode, model_complexity = self.modelComplexity,                   ## Pasar argumentos por nombre para asegurarse que funciona
                                     smooth_landmarks = self.smooth, min_detection_confidence = self.detectionConf, 
                                     min_tracking_confidence = self.trackConf)

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #Transformamos la imagen obtenida por opencv(BGR) a RGB para trabajar con mediapipe
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS)
        return img
        

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id,lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy, lm.z])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                
                
        return self.lmList
    
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        x3, y3 = self.lmList[p3][1:3]

        p1_vec = np.array(self.lmList[p1][1:3]) - np.array(self.lmList[p2][1:3])
        p3_vec = np.array(self.lmList[p3][1:3]) - np.array(self.lmList[p2][1:3])

        cos_theta = (np.dot(p1_vec, p3_vec)) / (1.0 * np.linalg.norm(p1_vec) * np.linalg.norm(p3_vec))
        theta = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        degree = int(180 / np.pi) * theta
        
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(degree)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)         
        return int(degree)

    def persona_de_frente(self, angulo):
        angleCara = self.findAngle(None, 11, 0, 12, False)
        if angleCara >= (angulo - 10) and angleCara <= (angulo + 10):             
            return True                                      
        else:
            return False
        
    def persona_tumbada(self):
        y1 = self.lmList[11][2]
        y2 = self.lmList[12][2]
        y3 = self.lmList[23][2]
        y4 = self.lmList[24][2]

        media = (y1 + y2 + y3 + y4) / 4

        lista = [y1, y2, y3 , y4]

        for y in lista:
            if abs(media - y) > 100:
                return False
        
        return True
    

    def posicion_correcta(self, posicion):
        pos = False
        if posicion == 0:                                   # Persona de lado (0)
            pos = not (self.persona_de_frente(85))
        elif posicion == 1:                                 # Persona de frente (1)
            pos = self.persona_de_frente(85)
        elif posicion == 2:                                 # Persona tumbada (2)
            pos = self.persona_tumbada()
        return pos

    


def main():
    cap = cv2.VideoCapture(0)
    success, img = cap.read()
    # scale_percent = 70 # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)

    # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    salida = cv2.VideoWriter('Prueba.avi',cv2.VideoWriter_fourcc(*'XVID'),15.0,(1280, 720))
    sTime = 0
    detector = poseDetector()
   
    while success:
        success, img = cap.read()
        if not success:
                break

       
        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)
        # dim = (width, height)

        # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        img = cv2.flip(img,1)
        img = cv2.resize(img, (1280, 720))

        
        img = detector.findPose(img, True)
        lmList = detector.findPosition(img, False)
        if len(lmList) != 0:
            
            ### Muestra por pantalla la coordenada z de una landmark ##########
            # Se considera a la cadera el origen de coordenadas. La coordenada será negativa si está entre la coordenada 0 y la cámara,
            # y positiva si se encuentra destrás del origen.

            # cv2.putText(img, "Coord Z: " + str(round(lmList[0][3], 3)), (0, 400), cv2.FONT_HERSHEY_PLAIN,
            #             2, (255, 0, 0), 3)
            # cv2.circle(img, (lmList[0][1], lmList[0][2]), 15, (0, 255, 0), cv2.FILLED)
            ###################################################################

            ####### Comprueba en qué posición está la persona ##############################
            #detector.findAngle(img, 11, 0, 12)
            # if detector.persona_tumbada():
            #     cv2.putText(img, "Persona tumbada", (0, 500), cv2.FONT_HERSHEY_PLAIN,
            #                     2, (0, 255, 0), 3)
            # else:
            #     if detector.persona_de_frente(80):
            #         if lmList[0][-1] < 0:
            #             cv2.putText(img, "Persona de frente", (0, 500), cv2.FONT_HERSHEY_PLAIN,
            #                     2, (0, 255, 0), 3)
            #         elif lmList[0][-1] > 0:
            #             cv2.putText(img, "Persona de espaldas", (0, 500), cv2.FONT_HERSHEY_PLAIN,
            #                     2, (0, 0, 255), 3)
            #     else:
            #         cv2.putText(img, "Persona de lado", (0, 500), cv2.FONT_HERSHEY_PLAIN,
            #                 2, (255, 0, 0), 3)
            ############################################################################
            left_arm_angle = detector.findAngle(img, 12, 14, 16)
            #print(lmList)
        cTime = time.time()
        fps = 1 / (cTime - sTime)
        sTime = cTime
        
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
        
        cv2.imshow("Ejemplo", img)
        salida.write(img)
        if cv2.waitKey(1)== ord('q'):
            break

    cap.release()
    salida.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()