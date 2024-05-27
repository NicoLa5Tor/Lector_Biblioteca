import cv2
from pyzbar import pyzbar
from concurrent.futures  import ThreadPoolExecutor
from resources.web_srap import WebScrap
from resources.bar_code import Bar_code
import pyautogui
#estas librerias son para el windows, para dejar fijas las vintanas
#import win32gui, win32con

executor = ThreadPoolExecutor(max_workers=1)
obj = WebScrap()
global driver
global ant_qr,qr_code
global cont
global cap
#este codigo trae el tamaño de la pantalla ususario

cont = 0
ant_qr = qr_code = 0


#este bloque se llama antes de inicializar cada seteo de variables o cada vez que se llame una 
def cam_start():   
    global driver
    driver_return = executor.submit(obj.web,qr_code)
    driver =  driver_return.result()
   
def leer_codigo_qr():
    global driver
    global cap
    cam_start()
    global ant_qr,qr_code
    global cont
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,300)
    screen_width, screen_height = pyautogui.size()
   # hwnd = win32gui.FindWindow(None, "Camera")
   # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    while cap.isOpened():
        ret, frame = cap.read()
      #  cv2.namedWindow('Registro Biblioteca Facatativá',cv2.WINDOW_NORMAL)
        codigos_qr = pyzbar.decode(frame)
        for codigo_qr in codigos_qr:
            (x, y, w, h) = codigo_qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            qr_code = codigo_qr.data.decode("utf-8")
            cv2.putText(frame, qr_code, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
          #  print("Contenido decodificado del código QR:", qr_code)
            print(f"EL qr anteriror es: {ant_qr}")
            if ant_qr != qr_code:
                    executor.submit(obj.web,qr_code,driver)
            elif ant_qr != qr_code and cont > 0:
                    executor.submit(obj.web,qr_code,driver)    
            ant_qr = qr_code
        if ret == True:
             cv2.imshow('Universidad de Cundinamarca-Facatativa', frame)          
             cv2.moveWindow('Universidad de Cundinamarca-Facatativa',screen_width,screen_height)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            try:
             obj.exit(driver=driver)
            except Exception as e:
                print(f"Excepcion controlada {e}")
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
 leer_codigo_qr()

  


  

