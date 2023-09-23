import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Inicialize o MediaPipe Hands
hands = mp_hands.Hands()

# Variáveis para controlar o estado da mão
hand_open = True
hand_state_changed = False
count = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        continue

    # Converta a imagem para tons de cinza
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Rastreie as mãos
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Pegue as coordenadas dos landmarks dos dedos indicador e médio
            index_finger_tip = landmarks.landmark[8]
            middle_finger_tip = landmarks.landmark[12]

            # Calcule a distância entre os dois landmarks
            distance = ((index_finger_tip.x - middle_finger_tip.x)**2 + (index_finger_tip.y - middle_finger_tip.y)**2)**0.5

            # Ajuste este valor conforme necessário
            if distance < 0.05:
                if hand_open:
                    hand_open = False
                    hand_state_changed = True
            else:
                if not hand_open:
                    hand_open = True
                    hand_state_changed = True

            # Desenhe os landmarks na imagem
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    if hand_state_changed:
        if not hand_open:
            print("Mão fechada.")
            count += 1
            print("Número de repetições:", count)
        else:
            print("Mão aberta.")
    

        hand_state_changed = False

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(60) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
