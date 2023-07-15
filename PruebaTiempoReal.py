
import cv2
import mediapipe as mp

#Inicializar "pose estimator"
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)


cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    try:
        #frame = cv2.resize(frame,(300,600))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pose_results = pose.process(frame_rgb)

        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Output', frame)  
        
    except:
        break

    if cv2.waitKey(1)== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

    


    