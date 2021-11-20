from tkinter import *
from PIL import ImageTk, Image
import numpy as np                              
import cv2
import time
import imutils
from imutils.video import VideoStream

def cantos_arena(frame):
    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    Cormaxima = np.array([0, 0, 100])
    Corminima = np.array([0, 0, 100])
    mascara = cv2.inRange(hsv, Corminima, Cormaxima)
    #branco = cv2.bitwise_and(frame, frame, mask=mascara)
    return mascara


# Função para calcular a distancia entre robôs aliados e a bola 
def calc_distancia(frame, xcentR, ycentR, xcentB, ycentB):
    cv2.line(frame, (xcentR, ycentR), (xcentB, ycentB), (0,0,255), 3, 8)
    centerR = ((xcentR + 1), (ycentR + 1))
    euclid = np.sqrt((xcentB - xcentR)**2 + (ycentB - ycentR)**2)
    num = round(euclid, 2)
    dis = str(num)
    cv2.putText(frame, dis, centerR, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0))
    return frame

# Função para detectar robos aliados.
def MascRobos(frame, num, cmin, cmax):
    
    blur = cv2.GaussianBlur(frame, (11, 11), 0) #Transforma a imagem para borrada. (Só ímpares)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Aplica na imagem borrada um filtro HSV.
    Cormaxima = cmin #Shade maximo da bola (laranja), array em HSV.
    Corminima = cmax #Shade minimo da bola (laranja), array em HSV.
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
                cv2.rectangle(frame, ((xcentro-1, ycentro+1)), ((xcentro+1, ycentro-1)), (0, 0, 255), 5, -1)#desenha o contorno na imagem 
                cv2.putText(frame, "Robo aliado", (int(xc), int(yc)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
        else: 
            xcentro, ycentro = 0, 0

    return frame, xcentro, ycentro 

# Função para aplicar mascara nas imagens recebinas
def MascBola(frame):

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


def tela_calibracao():
    
    hsv = show_frame()
    imagem = Image.fromarray(hsv)
    imgtk = ImageTk.PhotoImage(image=imagem)
    picker.imgtk = imgtk
    #picker.after(calibrar)
    Label(picker, image=imgtk).pack()
    
    
    

def show_frame():
    global imgtk
    global frame
    cmin = np.array([hmin.get(), smin.get(), vmin.get()])
    cmax = np.array([hmax.get(), smax.get(), vmax.get()])
    frame = cap.read()
    frame = imutils.resize(frame, width=600, height=600)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #frame = cv2.inRange(frame, cmin, cmax)
    imagem = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=imagem)
    picker.imgtk = imgtk
    foto = Label(picker, image=imgtk)
    foto.pack()
    Label(picker, text="imagem aqui").pack()
    
   
    
def iniciar():
    root.destroy()
    

def cancelar():
    exit()

def old_values():
    hmax.set(17)
    smax.set(255)
    vmax.set(255)
    hmin.set(0)
    smin.set(156)
    vmin.set(10)


#interface de seleção e calibração
root = Tk()
h = IntVar()
hmin = IntVar()
smin = IntVar()
vmin = IntVar()
hmax = IntVar()
smax = IntVar()
vmax = IntVar()
root.iconphoto(False, PhotoImage(file='logo_ieee_icone.png'))
root.title("calibração")
root.geometry('650x400') 
Label(root, text="Numero de Robôs aliados").place(x=20, y=0)
Label(root, text="H MIN:").place(x=200, y=15)
Label(root, text="S MIN:").place(x=200, y=55)
Label(root, text="V MIN:").place(x=200, y=95)
Label(root, text="Valores minimos da mascara").place(x=250, y=0)
Scale(root, from_= 0, to= 255, variable= hmin, orient= HORIZONTAL).place(x=250, y=15)
Scale(root, from_= 0, to= 255, variable= smin, orient= HORIZONTAL).place(x=250, y=55)
Scale(root, from_= 0, to= 255, variable= vmin, orient= HORIZONTAL).place(x=250, y=95)
Label(root, text="Valores maximos da mascara").place(x=470, y=0)
Label(root, text="H MAX:").place(x=420, y=15)
Label(root, text="S MAX:").place(x=420, y=55)
Label(root, text="V MAX:").place(x=420, y=95)
Scale(root, from_= 0, to= 255, variable= hmax, orient= HORIZONTAL).place(x=470, y=15)
Scale(root, from_= 0, to= 255, variable= smax, orient= HORIZONTAL).place(x=470, y=55)
Scale(root, from_= 0, to= 255, variable= vmax, orient= HORIZONTAL).place(x=470, y=95)
Button(root, text="Restaurar",width= 15 , command= old_values).place(x=350, y=150)
Button(root, text="1",width= 15 , command= lambda: h.set('1')).place(x=20, y=20)
Button(root, text="2",width= 15, command= lambda: h.set('2')).place(x=20, y=45)
Button(root, text="3",width= 15, command= lambda: h.set('3')).place(x=20, y=70)
Button(root, text="Iniciar",width= 15, command= iniciar).place(x=325, y=275, anchor= S)
Button(root, text="cancelar",width= 15, command= cancelar).place(x=325, y=325,anchor= S)


#interface do color picker

picker = Toplevel()
picker.geometry("650x600")
picker.title("Color Picker")
picker.iconphoto(False, PhotoImage(file='logo_ieee_icone.png'))
Scale(picker, from_= 0, to= 255,command= show_frame, variable= hmin, orient= HORIZONTAL).place(x=250, y=15)
Scale(picker, from_= 0, to= 255,command= show_frame, variable= smin, orient= HORIZONTAL).place(x=250, y=55)
Scale(picker, from_= 0, to= 255,command= show_frame, variable= vmin, orient= HORIZONTAL).place(x=250, y=95)
Scale(picker, from_= 0, to= 255, variable= hmax, orient= HORIZONTAL).place(x=470, y=15)
Scale(picker, from_= 0, to= 255, variable= smax, orient= HORIZONTAL).place(x=470, y=55)
Scale(picker, from_= 0, to= 255, variable= vmax, orient= HORIZONTAL).place(x=470, y=95)
show_frame()

mainloop()




cmin = np.array([hmin.get(), smin.get(), vmin.get()])
cmax = np.array([hmax.get(), smax.get(), vmax.get()])




while h.get() == 1 or h.get() == 2 or h.get() == 3  :   # Função de captura da imagem
    cont = h.get()
    frame = cap.read() # Captura da imagem
    frame = imutils.resize(frame, width=600, height=600)#resize, redefine o tamanho da imagem, usamos esse pq é mais rapido que o cv2.
    mascA = cantos_arena(frame)
    mascB, xcentB, ycentB = MascBola(frame)
    mascR, xcentR, ycentR = MascRobos(mascB, cont, cmin, cmax)
    dist = calc_distancia(mascR, xcentR, ycentR, xcentB, ycentB)
    cv2.imshow('cantos', mascA)
    cv2.imshow('mascBola', dist) # Exibicao da imagem
    #cv2.imshow('MascRobos', mascR)
    k = cv2.waitKey(5) & 0xFF
    t01 = time.time() # Frame t para calculo do FPS
    #print("{} fps, size: {}".format(int(1./(t01 - t00)), frame.shape)) # Printa informacoes sobre a imagem no terminal.
    t00 = time.time() # Frame t0 para calculo do FPS
    if k == 27 :
        break

cv2.destroyAllWindows()



