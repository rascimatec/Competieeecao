import numpy as np                              # Primeira tentativa, compatibilizar camera com o pc.
import cv2
import time
import keyboard
import imutils
from imutils.video import VideoStream

def calc_distancia(frame, xcentR, ycentR, xcentB, ycentB):
    cv2.line(frame, (xcentR, ycentR), (xcentB, ycentB), (0,0,255), 3, 8)
    centerR = ((xcentR + 1), (ycentR + 1))
    euclid = np.sqrt((xcentB - xcentR)**2 + (ycentB - ycentR)**2)
    num = round(euclid, 2)
    dis = str(num)
    cv2.putText(frame, dis, centerR, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
    return frame

# Função para detectar robos aliados.
def MascRobos(frame):
    frame = imutils.resize(frame, width=600, height=600) #resize, redefine o tamanho da imagem, usamos esse pq é mais rapido que o cv2.
    blur = cv2.GaussianBlur(frame, (11, 11), 0) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = np.array([117, 225, 158]) #Shade maximo da bola (laranja), array em HSV.
    Corminima = np.array([106, 115, 68]) #Shade minimo da bola (laranja), array em HSV.
    mascara = cv2.inRange(hsv, Corminima, Cormaxima) #Procura cores no raio desejado.
    mascara = cv2.dilate(mascara, None,iterations=3) ##aplica efeitos de mascara.
    mascara = cv2.erode(mascara,None,iterations=3) #aplica efeitos de mascara.
    contorno = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #aplica contornos na area detectada.
    xcentro, ycentro = 0 , 0
    if len(contorno) > 0: #só entra no if se o tamanho de contorno > 0
        c = max(contorno, key=cv2.contourArea)
        (xc, yc), raio = cv2.minEnclosingCircle(c) #pega valores para desenhar o circulo
        M = cv2.moments(c) #funcao foda para achar o centro de uma blob
        if M["m00"] != 0: #ocasionalmente m00 pode se tornar 0, assim verificamos.
            xcentro, ycentro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if raio > 10: #condicao para  nao detectar falsos positivos.
                cv2.circle(frame, (xcentro, ycentro), 5, (0, 0, 255), -1) #desenha o circulo no centro
                cv2.putText(frame, "Robo aliado", (int(xc), int(yc)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
        else: 
            xcentro, ycentro = 0, 0

    return frame, xcentro, ycentro 

# Função para aplicar mascara nas imagens recebinas
def MascBola(frame):

    frame = imutils.resize(frame, width=600, height=600) #resize, redefine o tamanho da imagem, usamos esse pq é mais rapido que o cv2.
    blur = cv2.GaussianBlur(frame, (11, 11), 0) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = np.array([17, 255, 255]) #Shade maximo da bola (laranja), array em HSV.
    Corminima = np.array([0, 156, 120]) #Shade minimo da bola (laranja), array em HSV.
    mascara = cv2.inRange(hsv, Corminima, Cormaxima) #Procura cores no raio desejado.
    mascara = cv2.dilate(mascara, None,iterations=3) ##aplica efeitos de mascara.
    mascara = cv2.erode(mascara,None,iterations=3) #aplica efeitos de mascara.
    contorno = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #aplica contornos na area detectada.
    xcentro, ycentro = 0 , 0
    if len(contorno) > 0: #só entra no if se o tamanho de contorno > 0
        c = max(contorno, key=cv2.contourArea)
        (xc, yc), raio = cv2.minEnclosingCircle(c) #pega valores para desenhar o circulo
        M = cv2.moments(c)
        if M["m00"] != 0:
            xcentro, ycentro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if raio > 10: #condicao para  nao detectar falsos positivos.
                cv2.circle(frame, (int(xc), int(yc)), int(raio), (255,0,0), 3) #desenha o circulo na bola
                cv2.circle(frame, (xcentro, ycentro), 5, (0, 0, 255), -1) #desenha o circulo no centro
                cv2.putText(frame, "bola", (int(xc), int(yc)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))
        else:
            xcentro, ycentro = 0 , 0
    return frame, xcentro, ycentro





cap = VideoStream(src=0).start()
t00 = time.time()
while not keyboard.is_pressed('q'):   # Função de captura da imagem
    frame = cap.read() # Captura da imagem
    mascB, xcentB, ycentB = MascBola(frame)
    mascR, xcentR, ycentR = MascRobos(mascB)
    dist = calc_distancia(mascR, xcentR, ycentR, xcentB, ycentB)
    cv2.imshow('mascBola', dist) # Exibicao da imagem
    #cv2.imshow('MascRobos', mascR)
    k = cv2.waitKey(5) & 0xFF
    t01 = time.time() # Frame t para calculo do FPS
    print("{} fps, size: {}".format(int(1./(t01 - t00)), frame.shape)) # Printa informacoes sobre a imagem no terminal.
    t00 = time.time() # Frame t0 para calculo do FPS
    if k == 27 :
        break

cv2.destroyAllWindows()



