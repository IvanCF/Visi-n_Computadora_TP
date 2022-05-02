
import cv2

cap = cv2.VideoCapture("video_demo_720p.mp4")
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# se usa el modelo para detectar solo ojos abiertos
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

bandera = 0  # contador para detecciones ojos cerrados
factor=3

while True:

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    scaleFactor = 1.3
    minNeigbors = 5
    faces = faceClassif.detectMultiScale(gray, scaleFactor, minNeigbors)

    k = cv2.waitKey(1)
    if k == 27:
        break

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (34, 220, 220), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        al, an, c = frame.shape
        num_ojos = len(eyes)
        if num_ojos == 0 or num_ojos == 1:
            bandera = bandera + 1
            print(bandera)
        else:
            bandera = 0

        ##################################
        index = 0
        ex_temp = 0;
        ey_temp = 0
        for (ex, ey, ew, eh) in eyes:
            ymitad = (y + (h / 2))  # los ojos solo pueden estar en la primera mitad del rostro
            # es el primer ojo a dibujar y esta en la primera mitad del rostro?
            if index == 0 and (ey < ymitad):
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                index = index + 1
                ex_temp = ex
                ey_temp = ey
                # SE MUESTRA LA ALERTA
                cv2.rectangle(frame, (10, 150), (250, 200), (255, 255, 255), -1)
                cv2.putText(frame, 'DESPIERTO', (20, 180), 3, 0.5, (220, 181, 34), 1, cv2.LINE_AA)
                print("DESPIERTO", bandera)
            else:

                altura = abs(ey - ey_temp)  # la altura del segundo ojo no debe ser muy abajo
                # print(altura)
                if altura < 20 and (ey < ymitad):
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                    index = index + 1
                    ex_temp = ex
                    ey_temp = ey
                    cv2.rectangle(frame, (10, 150), (250, 200), (255, 255, 255), -1)
                    cv2.putText(frame, 'DESPIERTO', (20, 180), 3, 0.5, (220, 181, 34), 1, cv2.LINE_AA)
                    print("DESPIERTO", bandera)
            # else:
            # index = index + 1
            #	ex_temp = ex
            #	ey_temp = ey

        if bandera >= factor:
            # Si el contador es mayor al factor se durmió
            print("DURMIENDO", bandera)
            cv2.rectangle(frame, (10, 150), (250, 200), (255, 255, 255), -1)
            cv2.putText(frame, 'DURMIENDO', (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 59, 220), 2)

    ########Información para terminar el programa #############################################
    cv2.rectangle(frame, (10, 5), (450, 25), (255, 255, 255), -1)
    cv2.putText(frame, 'Presione Esc, para salir', (10, 20), 2, 0.5, (220, 51, 34), 1, cv2.LINE_AA)
    cv2.imshow('frame', frame)

cap.release()
cv2.destroyAllWindows()
