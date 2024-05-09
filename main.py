import cv2
from pyzbar import pyzbar
from concurrent.futures  import ThreadPoolExecutor
from resources.web_srap import WebScrap
from resources.bar_code import Bar_code
import threading

#estas librerias son para el windows, para dejar fijas las vintanas
#import win32gui, win32con

executor = ThreadPoolExecutor(max_workers=1)
obj = WebScrap()
global driver
global ant_qr,qr_code
global cont
cont = 0
driver = None
ant_qr = qr_code = 0
#aqui se define un bloque, para que las variables anteriormente mencionadas, se puedan manejar
#entre hilos
global_lok = threading.Lock()
#este bloque se llama antes de inicializar cada seteo de variables o cada vez que se llame una 
def cam_start():
    cap = cv2.VideoCapture(0)
    return cap
def leer_codigo_qr():
    global driver
    cap = cam_start()
    global ant_qr,qr_code
    global cont


   # hwnd = win32gui.FindWindow(None, "Camera")
   # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    while cap.isOpened():
        ret, frame = cap.read()
        codigos_qr = pyzbar.decode(frame)
        for codigo_qr in codigos_qr:
            (x, y, w, h) = codigo_qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            qr_code = codigo_qr.data.decode("utf-8")
            cv2.putText(frame, qr_code, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
          #  print("Contenido decodificado del código QR:", qr_code)
            print(f"EL qr anteriror es: {ant_qr}")
            with global_lok:
                if ant_qr != qr_code and cont < 1:
                    driver_return = executor.submit(obj.web,qr_code)
                    driver =  driver_return.result()
                    cont += 1
                elif ant_qr != qr_code and cont > 0:
                    executor.submit(obj.web,qr_code,driver)
               
            ant_qr = qr_code
        cv2.imshow('Camara', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            try:
             obj.exit(driver=driver)
            except Exception as e:
                print(f"Excepcion controlada {e}")
            break
    cap.release()
    cv2.destroyAllWindows()
def leer_barras():
     global driver 
     global ant_qr,qr_code
     global cont
     obj_bar = Bar_code()
     while True:
        try:
             qr_code = obj_bar.main()  
             with global_lok: 
                if ant_qr != qr_code and driver == None:
                    driver_return =  executor.submit(obj.web,qr_code)
                    driver = driver_return.result()
                    
                    cont += 1
                elif ant_qr != qr_code:
                     print(f"el qr_anterior es: {ant_qr}")
                     executor.submit(obj.web,qr_code,driver) 
                ant_qr = qr_code 
        except Exception as e:
            print(f"error en la carga de barras {e}")

if __name__ == "__main__":
 
  thread_qr = threading.Thread(target=leer_codigo_qr)
  thread_qr.start()
  thread_bar = threading.Thread(target=leer_barras)
  thread_bar.start()

  thread_qr.join() 
  thread_bar.join()
  


  

