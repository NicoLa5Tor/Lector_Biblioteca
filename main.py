import cv2
from pyzbar import pyzbar
from concurrent.futures  import ThreadPoolExecutor
from resources.web_srap import WebScrap
import pyautogui
import threading,sys,keyboard,time
from resources.message import Message


#estas librerias son para el windows, para dejar fijas las vintanas
#import win32gui, win32con

executor = ThreadPoolExecutor(max_workers=1)
obj = WebScrap()
message = Message()
global driver
global ant_qr,qr_code
global program_exit
global cont
cont = 0
driver = None
ant_qr = qr_code = 0
program_exit = False

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
    global program_exit
    global ant_qr,qr_code
    global cont
    cam_start()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,300)
    screen_width, screen_height = pyautogui.size()
    message.show_message_info(message="Programa en ejecucion, precion aceptar para comenzar")


   
       # hwnd = win32gui.FindWindow(None, "Camera")
   # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    try:
     while cap.isOpened():
        ret, frame = cap.read()
        codigos_qr = pyzbar.decode(frame)
        if ret is False:
            break
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
            
        cv2.imshow('Universidad de Cundinamarca-Facatativa', frame)        
        cv2.moveWindow('Universidad de Cundinamarca-Facatativa',(screen_width - 350),(screen_height - 350))
        cv2.waitKey(1) 

        if program_exit:
              obj.exit(driver=driver)
              break
    except Exception as e:   
      print(f"excepcion controlada en el while de camara: {e}")
    cap.release()
    cv2.destroyAllWindows()
def barcode_scanner():
    barcode = ""
    global driver
    global program_exit
    global ant_qr,qr_code 
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            char = event.name
            if char == "q":
                print("proceso termiando")
                try:   
                    with global_lok:
                         program_exit = True
                    message.show_message_info(message="El programa se cerrará en 5 segundos")
                    time.sleep(1) 
                    sys.exit()  
                except Exception as e:
                     message.show_message_error(message="Ocurrio algo al tratar de cerrar el programa, suelva a intentarlo o cierre la tarea")
                     print(f"Excepcion controlada {e}")
                finally:
                    break
            if char == "enter":
                # Procesar el código de barras si no está vacío
                if barcode:
                    print("Código de barras escaneado:", barcode)
                    qr_code = barcode
                    barcode = ""  # Reiniciar el código de barra
                    if ant_qr != qr_code:
                         executor.submit(obj.web,qr_code,driver)
                         with global_lok:
                              ant_qr = qr_code
            else:
                if char.isdigit():
                  barcode += char
    
      

if __name__ == "__main__":
 
  thread_qr = threading.Thread(target=leer_codigo_qr)
  thread_qr.start()
  barcode_scanner()
  thread_qr.join() 
  


  

