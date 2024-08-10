from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .message import Message
from .base import Operations_Database
from concurrent.futures import ThreadPoolExecutor
from .os.op import Operations_Os
import json,time,re,sys,os,socket


class WebScrap:
    def __init__(self):  
        self.executor = ThreadPoolExecutor(max_workers=3)  
        self.dictionary = {}
        self.connection = True
        self.os = Operations_Os()
        self.data = self.os.config()
        self.me = Message()
    def web(self,qr_decode,original_driver = None,refresh = False):
        driver = None
        element_xpath = "/html/body/div/div[2]/div"
        message = 'Script preparado para un nuevo usuario'
        script_hab = """
        let inp = document.getElementById('pegeDocumento');
        let butt = document.getElementById('btnEnviar');
        butt.disabled = false;
        inp.disabled = false;
        inp.readOnly = true;
        """
        script_insert = f"""
        let text = document.getElementById('pegeDocumento');
        text.value = {qr_decode}
           """

        script_disabled = """
        let input = document.getElementById('pegeDocumento');
        let button = document.getElementById('btnEnviar');
        input.value = '';
        input.disabled = true;
        button.disabled = true;
        """
        style_by_input = f"""
            var element = document.evaluate('{element_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            element.style.backgroundImage = "url('data:image/jpg;base64,{self.data['logo']}')";
            element.style.backgroundRepeat = 'no-repeat';
            element.style.backgroundPosition = "right center"; 
            """
        notify = f"""
            alertify.success('{message}');
        """
        try:
            if original_driver == None:
                print("entra acrear el driver")
                driver = webdriver.Firefox()
                driver.get(self.data['url'])
                time.sleep(2)
            else:
                    original = original_driver.current_window_handle
                    original_driver.switch_to.window(original)
                    driver = original_driver
            iframe = driver.find_element(By.XPATH,'/html/body/iframe')
           
            #por la mala estructura de la pargina, se tuvo que cambiar el contexto del ifram primero, 
            #porque este iba dirigido hacia otro lugar
            #llamdas de los elementos
            driver.switch_to.frame(iframe)
            driver.execute_script(script_disabled)
        # panel_class = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div/div[3]/form/div/fielset/div/input')
            if original_driver is not None and refresh == False :
                driver.execute_script(script_hab)
                driver.execute_script(script_insert)
                time.sleep(0.5)
                buton = driver.find_element(By.XPATH,'//*[@id="btnEnviar"]')
                buton.click()
            if original_driver is not None and refresh == False:
                driver.execute_script(script_disabled)
                time.sleep(1)
                self.init_facultad(driver=driver)        
            title = driver.find_element(By.XPATH,'/html/body/div/nav/div/div[1]/span')
            #print(f"El titulo original es: {original_title}")
            #if ":"  not in original_title:
            new_title = "UNIDAD REGIONAL, EXTENSIÓN FACATATIVÁ - AUDITORIO : POR NICOLÁS RODRÍGUEZ TORRES"
            driver.execute_script("arguments[0].textContent = arguments[1];",title,new_title)
            driver.execute_script(script_disabled)
            driver.execute_script(style_by_input)
            
        except Exception as e:
            self.me.show_message_op(message="Ocurrió algo al tratar de abrir el navegador",
                                    time=2,
                                    title="Connection Error")
            driver.quit()

         #   print(f"Excepcion controlada, posible falla de conexion al tratar de acceder a la pagina o a un item de la misma, {e}")
        finally:
            return driver
    def init_facultad(self,driver):
        description = self.facultad(driver=driver)
        if description is None:
                 print("usuario erroneo, o descripcion no encontrada")
        else:
                print(description)
                dat = re.search(r'\d', description)
                if dat:
                    description =  description[:dat.start()]
                self.concat_concurrent(facultad=description)
        self.connection = True
    def check_connection(self):
        try:
            print("hace el ping")
            socket.create_connection(("www.google.com",80),timeout=15)
            self.connection = True
        except OSError as e:
            print(f"Error {e}")
            self.connection = False
    def facultad(self, driver,cont = 0):
        error = None
        description_of_facultad = None
        last_ciclo = False
        img_log = False
        img_loading = driver.find_element(By.XPATH,'/html/body/div/div[1]')
        while True:
            try:
                #print("entra al while")
                descriptions = driver.find_elements(By.XPATH,'//*[@id="div_informacion"]//table/tbody/tr[4]/td')
                if cont > 1:
                    error = driver.find_elements(By.XPATH,'/html/body/section[2]/article')
                    if len(error) > 0:
                        #    print(f"Se encontro error: {error[0].text}")
                        if   error[0].text == "Error Valide el documento o codigo digitado" :
                            print("retorna")
                            break
                   # print("no retorna")
                if self.connection == False:
                    print("retorna por conexion")
                    break
                if len(descriptions) > 0 and cont > 0:
                    print("encuentra descripcion")
                    description_of_facultad = descriptions[0].text
                
                    break
                if last_ciclo == True:
                    print("termino de cargar y no se encontro nada")
                    break
                #esta validacion, valida si existe una coneccion a internet fija, o fuerte,
                #intermamente hace un pool de thread que ejecuta una funcion que envia un ping con un socket a www.google.com, 
                #si el ping es correcto devuelve verdadero, si ocurre algun error cambia el valor de una variable global llamada connection
                #esta se valida más abajo
                if cont % 10 == 0 and cont > 0:
                    self.executor.submit(self.check_connection)
                    img_log = True
                if img_log == True:
                    display  = img_loading.value_of_css_property("display")
                    if display == 'none':
                      last_ciclo = True
                    else:
                      print("si hay")
                      last_ciclo = False
                time.sleep(2)
                print("No se encontro el elemento de descripcion, probablemente no ha cargado")
                cont += 1
            except NoSuchElementException as e:
                print(f"error {e}")
        return description_of_facultad
           
    def concat_concurrent(self,facultad):
        
        if facultad not in self.dictionary:
            self.dictionary[facultad] = 1
        else:
            self.dictionary[facultad] += 1

    #opciones de base de datos
             
    def save_database(self,y=None,m=None,item=None,p=None,name_p=None):
        try:
            data = self.data
            obj = Operations_Database(data=data,facults=self.dictionary)
            if y is not None and m is not None and item is not None:
                print(f"Entra al save con item {y}-{m}")
                obj.update_const(facults=item)
                obj.database_main(m=m,y=y)
                os.remove(path=p)
                print("Reserva eliminada")
            else:
                obj.database_main()
        except Exception as e:
            option = self.me.show_asokandnot(header="¡ERROR!, Lea con atención, cualquier opción guardará los datos. \n",
                                        message="\n~ Si da aceptar el programa intentará conectarse de nuevo a la base de datos \n~ Si da cancelar, el programa se cerrará, pero se tardará un poco más en abrir la próxima vez \n\n El try padre detectó un error: \n {}".format(e))
            try:
                if option:
                    if y is not None and m is not None and item is not None:
                        self.save_database(name_p=name_p,item=item,m=m,y=y,p=p)
                    else:
                        obj.database_main()
                else:
                    obj_op = self.os
                    if item is None:
                        ret = obj_op.main_operations(facult_today=self.dictionary)
                    else:
                        ret = 'none'
                    if ret == "Create":
                        self.me.show_message_op(message="Documento creado con éxito en la base de datos de reserva",
                                        title="Create Reserve",
                                        
                                        time=5)       
                    else:
                        if ret == 'none':
                            self.me.show_message_op(message="No se pudo guardar la base de datos  de treserva",
                                            title="No save Reserve",
                                            
                                            time=5)  
                        elif ret=='Update':
                            self.me.show_message_op(message="El documento de la base de datos de reserva fue actualizado",
                                            title="Update Reserve",
                                            
                                            time=5) 
            except Exception as e:
                print(f"Error en el guardado en reserva {e}")
                time.sleep(120)
    def exit(self,driver):
        try:
            driver.quit()
            print("se termina el proceso web")
            print(f"El diccionario es: {self.dictionary}")
            self.save_database()
            sys.exit()
        except Exception as e:
            print(f"error en exit {e}")
                   

            
            

        



