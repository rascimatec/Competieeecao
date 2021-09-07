import numpy as np                              # Primeira tentativa, compatibilizar camera com o pc.
import cv2
import time
import keyboard



# Função para aplicar mascara nas imagens recebinas
def MascBola(frame):
#    x, y, _ = frame.shape #pega x, e y da imagem
#    frame = cv2.resize(frame, int(y/2), int(x/2)) #redefinea resolucao da imagem, metade.
    blur = cv2.medianBlur(frame, 9) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = np.array([8, 233, 147]) #Shade maximo da bola (laranja), array em HSV ou sla.
    Corminima = np.array([0, 165, 62]) #Shade minimo da bola (laranja), array em HSV ou sla.
   
    mascara = cv2.inRange(hsv, Corminima, Cormaxima) #Procura cores no raio desejado.
    mascara = cv2.dilate(mascara, None,iterations=2)
    #mascara = cv2.erode(mascara,None,iterations=2)
    contorno = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.drawContours(frame, contorno, -1, (0,255,0,),3)
    (xc, yc), raio = cv2.minEnclosingCircle(contorno[0])
    #cv2.circle(frame, (int(xc), int(yc)), int(raio), (255,0,0), 3)
    return frame



cap = cv2.VideoCapture(0)
t00 = time.time()
while not keyboard.is_pressed('q'):   # Função de captura da imagem
    _, frame = cap.read() # Captura da imagem
    frame = MascBola(frame)
    cv2.imshow('frame', frame) # Exibicao da imagem
    k = cv2.waitKey(5) & 0xFF
    t01 = time.time() # Frame t para calculo do FPS
    print("{} fps, size: {}".format(int(1./(t01 - t00)), frame.shape)) # Printa informacoes sobre a imagem no terminal.
    t00 = time.time() # Frame t0 para calculo do FPS
    if k == 27 :
        break




