import cv2
import mediapipe as mp
import numpy as np
import time
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

#VIDEO FEED
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Mediapipe Feed', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=1), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=1) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            print(landmarks)
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=1), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=1) 
                                 )          

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

len(landmarks)
for lndmrk in mp_pose.PoseLandmark:
    print(lndmrk)
landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180/np.pi)
    
    if angle >180:
        angle = 360-angle
        
    return int(angle) 

shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
shoulder, elbow, wrist
calculate_angle(shoulder, elbow, wrist)
tuple(np.multiply(elbow, [640, 480]).astype(int))

#nois que fez
shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
shoulder2, elbow2, wrist2
calculate_angle(shoulder2, elbow2, wrist2)
tuple(np.multiply(elbow, [640, 480]).astype(int))

cap = cv2.VideoCapture(0)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            angle2 = calculate_angle(shoulder2, elbow2, wrist2)
            
            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA 
                                )
            
            cv2.putText(image, str(angle2), 
                           tuple(np.multiply(elbow2, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA 
                                )            

        except:
                  pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=1), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=1) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0 
stage = None

counter2 = 0
stage2 = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    nome_arquivo = "projeteee.txt"
    arquivo = open(nome_arquivo, "w+")
    menor_numero = float('inf')  # Inicializado com infinito positivo
    maior_numero = float('-inf')
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]            
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)

            angle2 = calculate_angle(shoulder2, elbow2, wrist2)

            # Visualize angle
            cv2.putText(image, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, str(angle2), 
                           tuple(np.multiply(elbow2, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )            
            
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 50 and stage =='down':
                stage="up"
                counter +=1
                print(counter)

            if angle2 > 160:
                stage2 = "down"
            if angle2 < 50 and stage2 =='down':
                stage2="up"
                counter2 +=1
                print(counter2)                
                       
        except:
            pass
        
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (95,73), (0,0,0), -1)

        cv2.rectangle(image, (540,0), (640,73), (0,0,0), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (20,20), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter2), 
                    (20,60), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (255,255,255), 1, cv2.LINE_AA)

        # Stage data
        #cv2.putText(image, 'STAGE', (90,20), 
        #           cv2.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
        #cv2.putText(image, stage2, 
        #            (60,60), 
        #            cv2.FONT_HERSHEY_DUPLEX, 1.2, (255,255,255), 1, cv2.LINE_AA)
        
        
        # Rep data
        cv2.putText(image, 'REPS', (570,20), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (570,60), 
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (255,255,255), 1, cv2.LINE_AA)

        # Stage data
        #cv2.putText(image, 'STAGE', (560,20), 
        #            cv2.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1, cv2.LINE_AA)
        #cv2.putText(image, stage, 
        #            (515,60), 
        #            cv2.FONT_HERSHEY_DUPLEX, 1.2, (255,255,255), 1, cv2.LINE_AA)
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=1, circle_radius=1), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=1, circle_radius=1) 
                                 )       
       
        print(angle, file = arquivo)

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):   
            break

    with open(nome_arquivo, 'r') as arquivo:
      linhas = arquivo.readlines()
      for linha in linhas:
        numero = int(linha.strip())  # Converte a linha para int

        # Atualize o menor e o maior números, se necessário
        if numero < menor_numero:
            menor_numero = numero
        if numero > maior_numero:
            maior_numero = numero

      # Verifique se foram encontrados números válidos (caso o arquivo esteja vazio)
      if menor_numero == float('inf') or maior_numero == float('-inf'):
       print("O arquivo está vazio ou não contém números.")
      else:
       print(f"O menor número na lista é: {menor_numero}")
       print(f"O maior número na lista é: {maior_numero}")

    cap.release()
    cv2.destroyAllWindows()