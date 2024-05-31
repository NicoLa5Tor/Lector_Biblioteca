from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .message import Message as me
import json,time,re,sys,os

class WebScrap:
    def __init__(self):
        self.data = self.config()
    def web(self,qr_decode,original_driver = None):
        driver = None
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
                time.sleep(1)
        # panel_class = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div/div[3]/form/div/fielset/div/input')
            iframe = driver.find_element(By.XPATH,'/html/body/iframe')
            #por la mala estructura de la pargina, se tuvo que cambiar el contexto del ifram primero, 
            #porque este iba dirigido hacia otro lugar
            #llamdas de los elementos
            driver.switch_to.frame(iframe)
            driver.execute_script("document.body.style.pointerEvents = 'auto';")
            if original_driver is not None:
                input_txt = driver.find_element(By.XPATH,'//*[@id="pegeDocumento"]')
                buton = driver.find_element(By.XPATH,'//*[@id="btnEnviar"]')
                input_txt.clear()
                input_txt.send_keys(qr_decode)
        #  print(f"input encontrado")
                buton.click()
                time.sleep(1)
            #script para el caret de la caja de texto y para el eventos del body bloqueados
            element_xpath = "/html/body/div/div[2]/div"
            style_by_input = f"""
            var element = document.evaluate('{element_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            var body = document.body;
            body.style.pointerEvents = 'none';
            element.style.backgroundImage = "url('data:image/jpg;base64,{self.data['logo']}')";
            element.style.backgroundRepeat = 'no-repeat';
            element.style.backgroundPosition = "left center"; 
            var input = document.getElementById('pegeDocumento');
            input.style.caretColor = 'transparent';
            """
            title = driver.find_element(By.XPATH,'/html/body/div/nav/div/div[1]/span')
            original_title = title.text
            #print(f"El titulo original es: {original_title}")
            new_title = f"{original_title}: POR NICOLÁS RODRÍGUEZ TORRES"
            driver.execute_script("arguments[0].textContent = arguments[1];",title,new_title)
            if original_driver is not None:
                description = self.facultad(driver=driver)
                if description == None:
                    print("ususario erroneo, o descripcion no encontrada")
                    return driver
                else:
                    print(description)
            driver.execute_script(style_by_input)
            #print("Titulo cambiado")
        except Exception as e:
            me.show_message_error(message="Ocurrio algo al tratar de abrir el navegador, espere un momento e intentelo de nuevo")
            print(f"Excepcion controlada, posible falla de conexion al tratar de acceder a la pagina o a un item de la misma, {e}")
        finally:
            return driver
    def config(self):
        with open('config.json','r') as data:
            dat = json.load(data)
        return dat
    def facultad(self, driver,cont = 0):
        try:
            if cont >= 5:
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
            time.sleep(1)
            self.facultad(driver=driver,cont=cont+1)

    def exit(self,driver):
        try:
            driver.quit()
            print("se termina el proceso web")
            sys.exit()
        except Exception as e:
            print("proceso terminado")
            

        



