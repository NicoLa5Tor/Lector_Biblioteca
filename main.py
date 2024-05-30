import cv2
from pyzbar import pyzbar
from concurrent.futures  import ThreadPoolExecutor
from resources.web_srap import WebScrap
import pyautogui
import threading,sys,keyboard


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
    global driver
    driver_return = executor.submit(obj.web,qr_code)
    with global_lok:
         driver =  driver_return.result()

def leer_codigo_qr():
    global driver
    global ant_qr,qr_code
    global cont
    cam_start()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,500)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,300)
    screen_width, screen_height = pyautogui.size()
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
            if ant_qr != qr_code:
                    executor.submit(obj.web,qr_code,driver)
            with global_lok:
              ant_qr = qr_code
        if ret:
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
def barcode_scanner():
    barcode = ""
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            char = event.name
            if char == "enter":
                # Procesar el código de barras si no está vacío
                if barcode:
                    print("Código de barras escaneado:", barcode)
                    barcode = ""  # Reiniciar el código de barras
            else:
                barcode += char

if __name__ == "__main__":
 
  thread_qr = threading.Thread(target=leer_codigo_qr)
  thread_qr.start()



  barcode_scanner()
  thread_qr.join() 
  


  

