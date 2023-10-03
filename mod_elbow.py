import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def get_angle_records():
    return angle_records

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return int(angle)

def main():
    global angle_records

    cap = cv2.VideoCapture(0)

    counter_d, counter_e = 0, 0
    count_d, count_e = False, False

    angle_start, angle_end = 0, 0  
    angle_records = [0, 0, 0, 0]
    
    # Imprime captura angulos inicio e fim.
    # True = Imprime valor no console.
    debug = False 

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        nome_arquivo = "projeteee.txt"
        arquivo = open(nome_arquivo, "w+")
        menor_numero = float("inf")  # Inicializado com infinito positivo
        maior_numero = float("-inf")

        while cap.isOpened():

            ret, frame = cap.read()

            frame = cv2.flip(frame, 1)  # inverte imagem

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

                # Obtem as cordenadas. 
                # NOTA: devido ao flip da camera, o que é esquerdo fica direito e vice-versa.
                shoulder_e = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                ]
                elbow_e = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                ]
                wrist_e = [
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                ]

                shoulder_d = [
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                ]
                elbow_d = [
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                ]
                wrist_d = [
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                ]

                # Calcula angulo braco direito
                angle_d = calculate_angle(shoulder_d, elbow_d, wrist_d)

                # Calcula angulo braco esquerdo
                angle_e = calculate_angle(shoulder_e, elbow_e, wrist_e)

                # Mostra angulos na tela - Esquerda
                cv2.putText(
                    image,
                    f"ESQ: {str(angle_e)}",
                    tuple(np.multiply(elbow_e, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                
                # Mostra angulos na tela - Direita
                cv2.putText(
                    image,
                    f"DIR: {str(angle_d)}",
                    tuple(np.multiply(elbow_d, [640, 480]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                # Capturar a tecla pressionada pelo usuário
                key = cv2.waitKey(60) & 0xFF

                # Pressione q para sair
                if key == ord("q"):
                    #
                    # Ao sair imprime no console a angulação no formato: 
                    #   [inicio-braco-direito, fim-braco-direito, inicio-braco-esquerdo, fim-braco-esquerdo]
                    #
                    # print(f"Angulacao: {angle_records}")
                    break

                # Registra angulo inicial braco direito
                if key == ord("a"):
                    angle_start = angle_d
                    angle_records[0] = angle_start
                    if debug:
                        print(f"Angulo inicial (DIR): {angle_start}")

                # Registra angulo final braco direito
                if key == ord("s"):
                    angle_end = angle_d
                    angle_records[1] = angle_end
                    if debug:
                        print(f"Angulo final (DIR): {angle_end}")

                # Registra angulo inicial braco esquerdo
                if key == ord("k"):
                    angle_start = angle_e
                    angle_records[2] = angle_start
                    if debug:
                        print(f"Angulo inicial (ESQ): {angle_start}")

                # Registra angulo final braco esquerdo
                if key == ord("l"):
                    angle_end = angle_e
                    angle_records[3] = angle_end
                    if debug:
                        print(f"Angulo final (ESQ): {angle_end}")

                # Habilita contador de repeticao braco direito e esquerdo (tecla d e e)
                if key == ord("d"):
                    count_d, count_e = True, False
                    counter_e = 0 # zera contador esquerdo
                elif key == ord("e"):
                    count_d, count_e = False, True
                    counter_d = 0 # zera contador direito

                # Desabilita contador de repeticoes
                if key == 32:
                    count_d, count_e = False, False
                    counter_d, counter_e = 0, 0

                # Contador braco direito
                if count_d:
                    if angle_d > 160:
                        stage_d = "down"
                    if angle_d < 60 and stage_d == "down":
                        stage_d = "up"
                        counter_d += 1
                        print(f"Repeticao (DIR): {counter_d}")

                # # Contador braco esquerdo
                if count_e:
                    if angle_e > 160:
                        stage_e = "down"
                    if angle_e < 60 and stage_e == "down":
                        stage_e = "up"
                        counter_e += 1
                        print(f"Repeticao (ESQ): {counter_e}")
            except:
                pass

            #Imprime box para contadores na tela
            cv2.rectangle(image, (0, 0), (95, 83), (0, 0, 0), -1)
            cv2.rectangle(image, (540, 0), (640, 83), (0, 0, 0), -1)

            # Imprime texto e contador para repeticoes - Braco direito
            cv2.putText(
                image,
                "REP (DIR)",
                (560, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                str(counter_d),
                (570, 60),
                cv2.FONT_HERSHEY_DUPLEX,
                1.2,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            #Imprime informacao angulos na tela - Braco Direito
            cv2.putText(
                image,
                f"ANGULO INICIAL (DIR): {angle_records[0]}",
                (670, 30),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                f"ANGULO FINAL (DIR): {angle_records[1]}",
                (670, 50),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            #Imprime estado do contador repeticao direito
            cv2.putText(
                image,
                f"CONTADOR DE REPETICAO (DIR): {'LIGADO' if count_d else 'DESLIGADO'}",
                (670, 70),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            # Imprime texto e contador para repeticoes - Braco esquerdo
            cv2.putText(
                image,
                "REP (ESQ)",
                (10, 20),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                str(counter_e),
                (20, 60),
                cv2.FONT_HERSHEY_DUPLEX,
                1.2,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )

            #Imprime informacao angulos na tela - Braco Esquerdo
            cv2.putText(
                image,
                f"ANGULO INICIAL (ESQ): {angle_records[2]}",
                (120, 30),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                image,
                f"ANGULO FINAL (ESQ): {angle_records[3]}",
                (120, 50),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            #Imprime estado do contador repeticao esquerdo
            cv2.putText(
                image,
                f"CONTADOR DE REPETICAO (ESQ): {'LIGADO' if count_e else 'DESLIGADO'}",
                (120, 70),
                cv2.FONT_HERSHEY_DUPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

            # Render detections
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            )

            cv2.imshow("Flexao e extencao de cotovelo", image)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    print(f"Angulacao: {angle_records}")