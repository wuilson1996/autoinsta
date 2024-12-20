from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
import time
import os
from random_name import *
import pyautogui

class BrowserYahoo:
    def __init__(self):
        self.driver:webdriver.Chrome = None
        self._email = None
        self._name = None
        self._last_name = None
        self._password = None

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    def create_browser_with_proxy(self, proxy_ip="", port="", proxy_uso=0):
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
        if proxy_uso == True:
            options.add_argument(f'--proxy-server={proxy_ip}:{port}')

        path_driver = os.path.abspath("chromedriver.exe")
        # Inicializar el navegador con el proxy
        self.driver = webdriver.Chrome(path_driver, options=options)
    
    def handle_proxy_auth(self, username, password):
        time.sleep(5)  # Espera a que aparezca el cuadro de autenticación
        pyautogui.write(username)
        pyautogui.press('tab')
        pyautogui.write(password)
        pyautogui.press('enter')

    def next_button(self):
        button = self.driver.find_elements_by_xpath("//button[@type='button']")
        for b in button:
            if str(b.text).strip() == "Next":
                b.click()
                break

    def create_yahoo(self, name, last_name, email, password):
        self._email = f"{email}@yahoo.com"
        self._name = name
        self._last_name = last_name
        self._password = password
        print(f"Starting create: {name}, {last_name}, {email}@yahoo.com, {password}")
        time.sleep(3)
        self.driver.find_element_by_xpath("//input[@name='firstName']").send_keys(name)
        self.driver.find_element_by_xpath("//input[@name='lastName']").send_keys(last_name)
        self.driver.find_element_by_xpath("//input[@name='userId']").send_keys(email)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        time.sleep(2)
        options = self.driver.find_element_by_xpath("//select[@id='usernamereg-month']").find_elements_by_tag_name("option")
        option = random.choice(options)
        option.click()
        self.driver.find_element_by_xpath("//input[@id='usernamereg-day']").send_keys(str(random.randint(1, 28)))
        self.driver.find_element_by_xpath("//input[@id='usernamereg-year']").send_keys(str(random.randint(1990, 2003)))
        time.sleep(2)
        self.driver.find_element_by_xpath("//button[@id='reg-submit-button']").click()
    #id="recaptcha-submit"
    def set_phone(self, phone):
        result = "Success" 
        try:
            element_input = self.driver.find_element_by_xpath("//input[@id='usernamereg-phone']")
            element_input.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
            element_input.send_keys(Keys.DELETE)  # Elimina el texto seleccionado
            time.sleep(2)
            self.driver.find_element_by_xpath("//input[@id='usernamereg-phone']").send_keys(phone)
            time.sleep(3)
            self.driver.find_element_by_xpath("//button[@id='reg-sms-button']").click()
            #time.sleep(5)
            # if "This phone number has been used too many times" in self.driver.page_source:
            #     result = "This phone number has been used too many times"
            
            # if "Sorry, we could not create your Google Account." in self.driver.page_source:
            #     result = "Sorry, we could not create your Google Account."
        except KeyboardInterrupt:
            result = "Detenido por el usuario"
        except Exception as e:
            result = "Error: "+str(e)
        return result
    
    def set_code(self, code):
        element_input = self.driver.find_element_by_xpath("//input[@id='verification-code-field']")
        element_input.send_keys(Keys.CONTROL + "a")  # Selecciona todo el texto
        element_input.send_keys(Keys.DELETE)  # Elimina el texto seleccionado
        time.sleep(2)
        for c in code:
            self.driver.find_element_by_xpath("//input[@id='verification-code-field']").send_keys(c)
            time.sleep(0.1)
        time.sleep(4)
        button = self.driver.find_element_by_xpath("//button[@id='verify-code-button']").click()
        time.sleep(4)
        button = self.driver.find_elements_by_xpath("//button[@type='submit']")
        for b in button:
            if str(b.text).strip() == "Listo":
                b.click()
                break
        time.sleep(4)
        self.driver.get("https://mail.yahoo.com/d/onboarding")
        self.driver.implicitly_wait(15)
        button = self.driver.find_elements_by_xpath("//button[@type='button']")
        for b in button:
            if str(b.text).strip() == "Finalizar más tarde":
                b.click()
                break

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

    def init_browser(self, username, password, proxy_password):
        time.sleep(5)
        self.driver.get("https://login.yahoo.com/account/create?.lang=es-CO&src=homepage&activity=ybar-signin&pspid=2142990676&.done=https%3A%2F%2Fespanol.yahoo.com%2F%3Fp%3Dus&specId=yidregsimplified&done=https%3A%2F%2Fespanol.yahoo.com%2F%3Fp%3Dus")
        self.driver.implicitly_wait(15)
        if proxy_password:
            self.handle_proxy_auth(username, password)
        full_name = random_names()
        self.create_yahoo(full_name[1], full_name[2], full_name[0], "colombia123*")
    
    def close(self):
        self.driver.close()
        self.__init__()


if __name__ == "__main__":
    #testing_signin("10008", "paulinarubioz02@servicio-tecnico-apple.shop")
    #testing_register("paulinarubioz02@servicio-tecnico-apple.shop")
    yahoo = BrowserYahoo()
    yahoo.create_browser_with_proxy("144.76.124.83", str(random.randint(10000, 20000)))
    yahoo.init_browser("84937b4537718abef992__cr.co", "8a08d42ec6cb5139")