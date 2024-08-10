import cv2
from pyzbar import pyzbar
from concurrent.futures  import ThreadPoolExecutor
from resources.web_srap import WebScrap
import pyautogui
import threading,keyboard
from resources.after_init import After
from resources.message import Message
from selenium.common.exceptions import WebDriverException, NoSuchWindowException, SessionNotCreatedException
import queue,time
import pygame
from resources.os.op import Operations_Os as os
import pyautogui

executor = ThreadPoolExecutor(max_workers=1)
add_executor = ThreadPoolExecutor(max_workers=3)
message = Message()
obj = WebScrap()
after = After()
global driver
global ant_qr
global program_exit
cola = queue.Queue()
driver = None
ant_qr = 0
program_exit = False
#se inicializa el mezcaldor de sonidos
pygame.mixer.init()
#se carga el sonido 
try:
    pygame.mixer.music.load(os.get_resource_path(relative_path='assets/qrcode.mp3',self=None))
except Exception:   
    pygame.mixer.music.load('./assets/qrcode.mp3')


#aqui se define un bloque, para que las variables anteriormente mencionadas, se puedan manejar
#entre hilos
global_lok = threading.Lock()
#este bloque se llama antes de inicializar cada seteo de variables o cada vez que se llame una 
def cam_start():
    global driver
    driver_return = executor.submit(obj.web,0)
    with global_lok:
         driver =  driver_return.result()

def leer_codigo_qr():
    global program_exit
    cam_start()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,300)
    screen_width, screen_height = pyautogui.size()
    message.show_message_op(message="Programa listo para ser ejecutado",title="Program Success",time=3)
    try:
     while cap.isOpened():
        pyautogui.moveTo((screen_height - ((screen_height/1.5)+5)),(screen_width - (screen_width/2)))
        ret, frame = cap.read()
        codigos_qr = pyzbar.decode(frame)
        if ret is False:
            break
        #zoom_factor = 2
        #zoomed_frame = apply_zoom(frame, zoom_factor)
        for codigo_qr in codigos_qr:
            (x, y, w, h) = codigo_qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            code = codigo_qr.data.decode("utf-8")
            cv2.putText(frame, code, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  
            add_executor.submit(add_to_cola,code)
        cv2.imshow('Universidad de Cundinamarca',frame)        
        cv2.moveWindow('Universidad de Cundinamarca',(0),(screen_height - 350))
        cv2.waitKey(1) 
        if program_exit == True:   
              break
    except Exception as e:   
      print(f"excepcion controlada en el while de camara: {e}")
    cap.release()
    cv2.destroyAllWindows()
def barcode_scanner():
    barcode = ""
    global program_exit
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            char = event.name
            if char == "t":
                add_executor.submit(add_to_cola,'1193602390')
            if char == "q":
                print("proceso termiando")
                try:   
                    with global_lok:
                         program_exit = True
                    message.show_message_info(message="El programa se cerrará en 5 segundos")
                    print("Termina la cola")
                    obj.exit(driver=driver)
                except Exception as e:
                     message.show_message_error(message="Ocurrio algo al tratar de cerrar el programa")
                     print(f"Excepcion controlada {e}")
                finally:
                    break
            if char == "enter":
                # Procesar el código de barras si no está vacío
                if barcode:
                    print("Código de barras escaneado:", barcode)
                    add_executor.submit(add_to_cola,barcode)
                    barcode = ""  # Reiniciar el código de barra
                    
            else:
                if char.isdigit():
                  barcode += char
#funciones filtro
def add_to_cola(qr):
    global ant_qr
    if ant_qr != qr:
        with global_lok:
            cola.put(qr)
            ant_qr = qr
        pygame.mixer.music.play()

def insert_to_while():
    global program_exit
    print("entra al insert")
    while program_exit == False:
        print("sigue en el while")
        if not cola.empty():
            print("la cola noe sta vacia")
            with global_lok:
                work = cola.get()
                cola.task_done()
            insert_user(work)
        time.sleep(1)
    print("El program exit arrojo verdadero")
def insert_user(qr):
    global ant_qr
    global driver
    window_is_open(driv=driver)
    obj.web(qr_decode=qr,original_driver=driver)
     
       
   
def window_is_open(driv):
    try:
        if len(driv.window_handles) > 0:
            return True
        else:
            print("LA ventana se cerro")
            cam_start()
            return False
    except (WebDriverException, NoSuchWindowException, SessionNotCreatedException,Exception):
            print("Excepcion del driver controlado en la main")
            cam_start()
            return False

def apply_zoom(frame, zoom_factor=1.2):
    height, width = frame.shape[:2]
    new_height, new_width = int(height / zoom_factor), int(width / zoom_factor)
    top = (height - new_height) // 2
    left = (width - new_width) // 2
    cropped_frame = frame[top:top + new_height, left:left + new_width]
    zoomed_frame = cv2.resize(cropped_frame, (width, height))
    return zoomed_frame
      

if __name__ == "__main__":
  after.valid_reserve()
  thread_qr = threading.Thread(target=leer_codigo_qr)
  insert = threading.Thread(target=barcode_scanner)
  thread_qr.start()
  insert.start()
  insert_to_while()
  thread_qr.join() 
  insert.join()
  

  

