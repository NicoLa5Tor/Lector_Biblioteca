from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json,time,re,sys



class WebScrap:
    def __init__(self):
        self.url = self.config()
    def web(self,qr_decode,original_driver = None):
        try:
            #print(f"url es: {self.url}")
            if original_driver == None:
                driver = webdriver.Firefox()
                driver.get(self.url)
                time.sleep(2)
            else:
                original = original_driver.current_window_handle
                original_driver.switch_to.window(original)
                driver = original_driver
                time.sleep(1)
           
                
            
            #//div[@id="pegeDocumento"]
            #input_text = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div/div/div[3]/form/div/fielset')
        # panel_class = driver.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div/div[3]/form/div/fielset/div/input')
            iframe = driver.find_element(By.XPATH,'/html/body/iframe')
            #por la mala estructura de la pargina, se tuvo que cambiar el contexto del ifram primero, 
            #porque este iba dirigido hacia otro lugar
            #llamdas de los elementos
            driver.switch_to.frame(iframe)
            driver.execute_script("document.body.style.pointerEvents = 'auto';")
            input_txt = driver.find_element(By.XPATH,'//*[@id="pegeDocumento"]')
            buton = driver.find_element(By.XPATH,'//*[@id="btnEnviar"]')
            input_txt.clear()
            input_txt.send_keys(qr_decode)
        #  print(f"input encontrado")
            buton.click()
            time.sleep(1)
            title = driver.find_element(By.XPATH,'/html/body/div/nav/div/div[1]/span')
            
            original_title = title.text
            #print(f"El titulo original es: {original_title}")
            new_title = f"{original_title} POR NICOLÁS RODRÍGUEZ TORRES"
            driver.execute_script("arguments[0].textContent = arguments[1];",title,new_title)
            description = self.facultad(driver=driver)
            if description == None:
                print("ususario erroneo, o descripcion no encontrada")
                return driver
            else:
                print(description)
            driver.execute_script("document.body.style.pointerEvents = 'none';")
            #print("Titulo cambiado")
        except Exception as e:
            print(f"Excepcion controlada, posible falla de conexion al tratar de acceder a la pagina o a un item de la misma")
        finally:
            return driver
    def config(self):
        with open('config.json','r') as data:
            dat = json.load(data)
        return dat['url']
    def facultad(self, driver,cont = 0):
        try:
            if cont >= 5:
                return None
            time.sleep(1)
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
            sys.exit()
        except Exception as e:
            print("proceso terminado")
            

        



