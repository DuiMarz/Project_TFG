import cv2
import numpy as np
import time
import PoseModule as pm
import ExercicesModule as em



ejercicios = em.ejercicios()


ejercicios.pesas_brazoIzquierdo(5)

#ejercicios.estiramiento(5)

#ejercicios.pesas_cadaBrazo(5)

#ejercicios.estiramiento_brazo(5)



##################################################################3
#cap = cv2.VideoCapture("pexels-michelangelo-buonarroti.mp4")
# salida = cv2.VideoWriter('videoSalida2.avi',cv2.VideoWriter_fourcc(*'XVID'),20.0,(1280, 720))
# cap = cv2.VideoCapture(0)

# detector = pm.poseDetector()
# utilidades = em.utilities()
# count = 0
# dir1 = 0
# dir2 = 0
# pTime = 0
# while cap.isOpened():
#     _, img = cap.read()
#     img = cv2.resize(img, (1280, 720))
 
#     img = detector.findPose(img, False)
#     lmList = detector.findPosition(img, False)
   
#     if len(lmList) != 0:
#         # Right Arm
#         #angleRA = detector.findAngle(img, 12, 14, 16, True)
#         # Left Arm
#         angleLA = detector.findAngle(img, 11, 0, 12, True)

#         per1 = np.interp(angleLA, (200, 340), (0, 100))
#         #per2 = np.interp(angleRA, (210, 310), (0, 100))

#         bar1 = np.interp(angleLA, (200, 340), (650, 100))
#         #bar2 = np.interp(angleRA, (220, 310), (650, 100))
#         # print(angle, per)

#         # #Check for the dumbbell curls
#         color = utilidades.get_performance_bar_color(per1)
#         if per1 == 100 or per1 == 0:
#             color = (0, 255, 0)
#             rep = utilidades.repitition_counter(per1, count, dir1)
#             count = rep["count"]
#             dir1 = rep["direction"]

#         utilidades.draw_performance_bar(img, per1, bar1, color, count)

#         # if per1 == 100: #and per2 == 100:
#         #     color = (0, 255, 0)
#         #     if dir1 == 0: #and dir2 ==0:
#         #         count += 0.5
#         #         dir1 = 1
#         # if per1 == 0: #and per2 == 0:
#         #     color = (0, 255, 0)
#         #     if dir1 == 1: #and dir2 == 1:
#         #         count += 0.5
#         #         dir1 = 0


     

#         # Draw Bar
#         # cv2.rectangle(img, (1050, 100), (1125, 650), color, 3)
#         # cv2.rectangle(img, (1050, int(bar1)), (1125, 650), color, cv2.FILLED)
#         # cv2.putText(img, f'{int(per1)}', (1030, 75), cv2.FONT_HERSHEY_PLAIN, 4,
#         #             color, 4)
        
#         # cv2.rectangle(img, (1200, 100), (1275, 650), color, 3)
#         # cv2.rectangle(img, (1200, int(bar2)), (1275, 650), color, cv2.FILLED)
#         # cv2.putText(img, f'{int(per2)}', (1180, 75), cv2.FONT_HERSHEY_PLAIN, 4,
#         #             color, 4)
        


#         # # # Draw Curl Count
#         utilidades.display_rep_count(img, count, 10)
#         # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
#         # cv2.putText(img, str(int(count)) + "/" + str(10), (20, 630), cv2.FONT_HERSHEY_PLAIN, 5,
#         #             (255, 0, 0), 15)

#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
#                 (255, 0, 0), 5)

#     cv2.imshow("Image", img)
#     salida.write(img)
#     if cv2.waitKey(1)== ord('q'):
#         break

# cap.release()
# salida.release()
# cv2.destroyAllWindows()