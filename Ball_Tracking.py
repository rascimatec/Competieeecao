import numpy as np                              # Primeira tentativa, compatibilizar camera com o pc.
import cv2
import time
import keyboard
import imutils
from imutils.video import VideoStream

# Função para detectar robos aliados.
def MascRobos(frame):
    frame = imutils.resize(frame, width=600) #resize, redefine o tamanho da imagem, usamos esse pq é mais rapido que o cv2.
    blur = cv2.GaussianBlur(frame, (11, 11), 0) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = np.array([117, 225, 158]) #Shade maximo da bola (laranja), array em HSV.
    Corminima = np.array([106, 115, 68]) #Shade minimo da bola (laranja), array em HSV.
    mascara = cv2.inRange(hsv, Corminima, Cormaxima) #Procura cores no raio desejado.
    mascara = cv2.dilate(mascara, None,iterations=3) ##aplica efeitos de mascara.
    mascara = cv2.erode(mascara,None,iterations=3) #aplica efeitos de mascara.
    contorno = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #aplica contornos na area detectada.
    center = None
    if len(contorno) > 0: #só entra no if se o tamanho de contorno > 0
        c = max(contorno, key=cv2.contourArea)
        (xc, yc), raio = cv2.minEnclosingCircle(c) #pega valores para desenhar o circulo
        M = cv2.moments(c) #funcao foda para achar o centro de uma blob
        if M["m00"] != 0: #ocasionalmente m00 pode se tornar 0, assim verificamos.
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) #calculo doido
            if raio > 10: #condicao para  nao detectar falsos positivos.
                cv2.circle(frame, center, 5, (0, 0, 255), -1) #desenha o circulo no centro
        else:
            center = (0, 0) 


    return frame 

# Função para aplicar mascara nas imagens recebinas
def MascBola(frame):

    frame = imutils.resize(frame, width=600) #resize, redefine o tamanho da imagem, usamos esse pq é mais rapido que o cv2.
    blur = cv2.GaussianBlur(frame, (11, 11), 0) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = np.array([17, 255, 255]) #Shade maximo da bola (laranja), array em HSV.
    Corminima = np.array([0, 156, 120]) #Shade minimo da bola (laranja), array em HSV.
    mascara = cv2.inRange(hsv, Corminima, Cormaxima) #Procura cores no raio desejado.
    mascara = cv2.dilate(mascara, None,iterations=3) ##aplica efeitos de mascara.
    mascara = cv2.erode(mascara,None,iterations=3) #aplica efeitos de mascara.
    contorno = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #aplica contornos na area detectada.
    center = None
    if len(contorno) > 0: #só entra no if se o tamanho de contorno > 0
        c = max(contorno, key=cv2.contourArea)
        (xc, yc), raio = cv2.minEnclosingCircle(c) #pega valores para desenhar o circulo
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) #calculo doido
            if raio > 10: #condicao para  nao detectar falsos positivos.
                cv2.circle(frame, (int(xc), int(yc)), int(raio), (255,0,0), 3) #desenha o circulo na bola
                cv2.circle(frame, center, 5, (0, 0, 255), -1) #desenha o circulo no centro
        else:
            center = (0, 0)
    return frame





cap = VideoStream(src=0).start()
t00 = time.time()
while not keyboard.is_pressed('q'):   # Função de captura da imagem
    frame = cap.read() # Captura da imagem
    mascB = MascBola(frame)
    mascR = MascRobos(frame)
    cv2.imshow('mascBola', mascB) # Exibicao da imagem
    cv2.imshow('MascRobos', mascR)
    k = cv2.waitKey(5) & 0xFF
    t01 = time.time() # Frame t para calculo do FPS
    print("{} fps, size: {}".format(int(1./(t01 - t00)), frame.shape)) # Printa informacoes sobre a imagem no terminal.
    t00 = time.time() # Frame t0 para calculo do FPS
    if k == 27 :
        break

cv2.destroyAllWindows()