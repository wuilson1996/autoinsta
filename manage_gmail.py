from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import time
import os
from random_name import *

class Browser:
    def __init__(self):
        self.driver:webdriver.Chrome = None

    def create_browser_with_proxy(self, proxy_ip="", port=""):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("no-sandbox")
        options.add_argument("--lang=en")  # Cambia el idioma a inglés
        path_extention = os.path.abspath("autobot.py").replace("autobot.py", "captchaSolver")
        options.add_argument(f"--load-extension={path_extention}")

        # Configurar el proxy
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = f"{proxy_ip}:{port}"
        proxy.ssl_proxy = f"{proxy_ip}:{port}"

        # Aplicar el proxy a las opciones de Chrome
        options.add_argument(f'--proxy-server={proxy_ip}:{port}')

        path_driver = os.path.abspath("chromedriver.exe")
        # Inicializar el navegador con el proxy
        self.driver = webdriver.Chrome(path_driver, options=options)

    def next_button(self):
        button = self.driver.find_elements_by_xpath("//button[@type='button']")
        for b in button:
            if str(b.text).strip() == "Next":
                b.click()
                break

    def create_gmail(self, name, last_name, email, password):
        time.sleep(2)
        button = self.driver.find_elements_by_xpath("//button[@type='button']")
        for b in button:
            if str(b.text).strip() == "Create account":
                b.click()
                break
        time.sleep(2)
        menu = self.driver.find_elements_by_xpath("//li[@role='menuitem']")
        for m in menu:
            if str(m.text).strip() == "For my personal use":
                m.click()
                break
        
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@name='firstName']").send_keys(name)
        self.driver.find_element_by_xpath("//input[@name='lastName']").send_keys(last_name)
        time.sleep(1)
        self.next_button()

        time.sleep(2)
        self.driver.find_element_by_xpath("//select[@id='month']").send_keys("February")
        self.driver.find_element_by_xpath("//input[@id='day']").send_keys(str(random.randint(1, 28)))
        self.driver.find_element_by_xpath("//input[@id='year']").send_keys(str(random.randint(1990, 2003)))
        self.driver.find_element_by_xpath("//select[@id='gender']").send_keys("Male")
        time.sleep(1)
        self.next_button()
        
        time.sleep(6)
        checks = self.driver.find_elements_by_xpath("//div[@jsname='wQNmvb']")
        for ch in checks:
            print(ch.text)
            if "Create your own Gmail address" == str(ch.text).strip():
                ch.click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//input[@name='Username']").send_keys(email)
        time.sleep(3)
        self.next_button()

        time.sleep(3)
        self.driver.find_element_by_xpath("//input[@name='Passwd']").send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@name='PasswdAgain']").send_keys(password)
        time.sleep(2)
        self.next_button()
        time.sleep(3)

    def set_phone(self, phone):
        result = "Success" 
        try:
            element_input = self.driver.find_element_by_xpath("//input[@id='phoneNumberId']")
            element_input.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
            element_input.send_keys(Keys.DELETE)  # Elimina el texto seleccionado
            time.sleep(2)
            self.driver.find_element_by_xpath("//input[@id='phoneNumberId']").send_keys(phone)
            time.sleep(3)
            self.next_button()
            time.sleep(5)
            if "This phone number has been used too many times" in self.driver.page_source:
                result = "This phone number has been used too many times"
            
            if "Sorry, we could not create your Google Account." in self.driver.page_source:
                result = "Sorry, we could not create your Google Account."
        except KeyboardInterrupt:
            result = "Detenido por el usuario"
        except Exception as e:
            result = "Error: "+str(e)
        return result

    def main(self, _driver):
        try:
            full_name = random_names()
            self.create_gmail(_driver, full_name[1], full_name[2], full_name[0], "colombia123*")
            result = self.set_phone(_driver, "+573023089137")
            print(result)
        except Exception as e:
            print("Error: "+str(e))

    def test_gmail(self, _driver):
        _driver = self.create_browser_with_proxy(proxy_ip="148.251.5.30", port=str(random.randint(10000, 20000)))
        _driver.get("https://gmail.com/")
        _driver.implicitly_wait(15)
        self.main(_driver)
        time.sleep(120)

    def init_browser(self):
        time.sleep(5)
        self.driver.get("https://gmail.com/")
        self.driver.implicitly_wait(15)
        full_name = random_names()
        self.create_gmail(full_name[1], full_name[2], full_name[0], "colombia123*")
    
    def close(self):
        self.driver.close()


if __name__ == "__main__":
    #testing_signin("10008", "paulinarubioz02@servicio-tecnico-apple.shop")
    #testing_register("paulinarubioz02@servicio-tecnico-apple.shop")
    #test_gmail()
    pass