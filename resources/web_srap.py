from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .message import Message as me
from concurrent.futures import ThreadPoolExecutor
import json,time,re,sys,os

class WebScrap:
    def __init__(self):
        self.data = self.config()
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        self.dictionary = {}
    def web(self,qr_decode,original_driver = None,refresh = False):
        driver = None
        element_xpath = "/html/body/div/div[2]/div"
        script_hab = """
        let inp = document.getElementById('pegeDocumento');
        let butt = document.getElementById('btnEnviar');
        inp.disabled = false;
        butt.disabled = false;
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
            element.style.backgroundPosition = "left center"; 
            """
        try:

            print("entra al try")
            #print(f"url es: {self.url}")
            if original_driver == None:
                print("entra el if de original driver")
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
                time.sleep(0.5)
                input_txt = driver.find_element(By.XPATH,'//*[@id="pegeDocumento"]')
                buton = driver.find_element(By.XPATH,'//*[@id="btnEnviar"]')
                input_txt.send_keys(qr_decode)
        #  print(f"input encontrado")
                print("Da click en el boton")
                buton.click()
            if original_driver is not None and refresh == False:
                self.executor.submit(self.init_facultad,driver)
                time.sleep(1)      
            if refresh == True:
                time.sleep(3)     
            title = driver.find_element(By.XPATH,'/html/body/div/nav/div/div[1]/span')
            #print(f"El titulo original es: {original_title}")
            #if ":"  not in original_title:
            new_title = "UNIDAD REGIONAL, EXTENSIÓN FACATATIVÁ - AUDITORIO : POR NICOLÁS RODRÍGUEZ TORRES"
            driver.execute_script("arguments[0].textContent = arguments[1];",title,new_title)
            print("Termina el try con exito")
            driver.execute_script(script_disabled)
            driver.execute_script(style_by_input)
        except Exception as e:
            me.show_message_error(message="Ocurrio algo al tratar de abrir el navegador, espere un momento e intentelo de nuevo")
            print(f"Excepcion controlada, posible falla de conexion al tratar de acceder a la pagina o a un item de la misma, {e}")
        finally:
            return driver
    def config(self):
        with open('config.json','r') as data:
            dat = json.load(data)
        return dat
    def init_facultad(self,driver):
        description = self.facultad(driver=driver)
        if description is None:
                 print("ususario erroneo, o descripcion no encontrada")
        else:
                 print(description)
                 self.concat_concurrent(facultad=description)
                 time.sleep(1)
                 self.web(qr_decode=0,driver=driver,refresh=True)

    def facultad(self, driver,cont = 0):
        try:
            if cont >= 4:
                return None
            time.sleep(2)
            descriptions = driver.find_element(By.XPATH,'//*[@id="div_informacion"]//table/tbody/tr[4]/td')
            #print(descriptions.get_attribute('innerHTML'))
            description_of_facultad = descriptions.text
            #dado que esto se separa por facultad y periodo de inicio, se separa la cadena usando 
            #expresiones reculares
            #con la expresion \d y r de regualr antes de empezar, se busca el primer dato numerico
            dat = re.search(r'\d', description_of_facultad)
            #se valida si esxite de verdad un nummero en la cadea, de ser asi
            if dat:
                return description_of_facultad[:dat.start()]
            else:
                return description_of_facultad
        except NoSuchElementException as e:
            print("No se encontro el elemento de descripcion, probablemente no ha cargado")
            time.sleep(0.5)
            self.facultad(driver=driver,cont=cont+1)
    def concat_concurrent(self,facultad):
        
        if facultad not in self.dictionary:
            self.dictionary[facultad] = 1
        else:
            self.dictionary[facultad] += 1


    def exit(self,driver):
        try:
            driver.quit()
            print("se termina el proceso web")
            print(f"El diccionario es: {self.dictionary}")
            sys.exit()
        except Exception as e:
            print("proceso terminado")
            

        



