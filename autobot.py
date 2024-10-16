# websockets
import asyncio
from asgiref.sync import sync_to_async
import websockets
import base64
#import cv2

# instagram
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
import json
import threading
import os
from PIL import Image
import random
from colorama import init, Fore, Back, Style
import logging
import platform

# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
import re
import time
from time import sleep
import argparse

_logging = logging.basicConfig(filename="logger.log", level=logging.INFO)


def chat_with_gpt(prompt):
    url = "http://127.0.0.1:8000/api/connetToAI/"
    payload = {'text': prompt}
    files=[]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return json.loads(response.text)

class ReCapchat:
    def __init__(self, driver=None, language="en-US") -> None:
        self._driver = driver
        self.language = language

    def run(self, name_file = "audio"):
        soup = BeautifulSoup(self._driver.page_source, "html.parser")
        iframe = soup.find("iframe", {"id": "recaptcha-iframe"})
        #logging.info(iframe)
        #for i in iframe:
        #    print(i.get("title"))
        result = False
        if iframe is not None:
            logging.info("[-] ReCapchat in current process, solver in progress")
            try:
                WebDriverWait(self._driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='recaptcha-iframe']")))
                WebDriverWait(self._driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='reCAPTCHA']")))
            except Exception as e:
                logging.info("[-] ReCapchat not Found")
            while True:
                if iframe is None:
                    break
                else:
                    try:
                        checkbox = WebDriverWait(self._driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']")))
                        is_checked = checkbox.get_attribute("aria-checked")
                        soup = BeautifulSoup(checkbox.get_attribute("innerHTML"), "html.parser")
                        if is_checked == "true" and "recaptcha-checkbox-checked" in checkbox.get_attribute("class"):
                            result = True
                            logging.info("[+] Checkmark reCapcha Verification success")
                            self._driver.switch_to.default_content()
                            sleep(2)
                            for b in self._driver.find_elements_by_xpath("//button[@type='button']"):
                                if "Siguiente" == str(b.text).strip() or "Next" in str(b.text).strip():
                                    b.click()
                                    break
                            break
                    except Exception as error:
                        logging.info("[-] ReCapchat not Found")
        else:
            logging.info("[-] ReCapchat not Found")
            result = True
        return result

class ServiceEmail:
    def __init__(self, username, password, to) -> None:
        # Configuración del servidor
        self.smtp_server = "mail.fixco.co"#"smtp.office365.com"
        self.puerto_imap = 993
        self.smtp_port = 587
        self.username = username
        self.password = password
        # settings server received
        #self.imap_server = "mail.fixco.co"#"outlook.office365.com"
        self.to = to

    def received(self, _server):
        self.smtp_server = "mail." + _server
        # Conectar al servidor
        mail = imaplib.IMAP4_SSL(self.smtp_server, self.puerto_imap)
        mail.login(self.username, self.password)

        # Seleccionar la bandeja de entrada
        mail.select("inbox")

        confirmation_code = None

        try:
            # Buscar correos no leídos
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = list(messages[0].split())
            #print("Email IDs encontrados:", email_ids)
            status_received = False
            email_ids.reverse()
            for e_id in email_ids:
                status, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        from_ = msg.get("From")
                        logging.info("Subject:"+ subject)
                        logging.info("From:"+ from_)

                        # Obtener el cuerpo del correo
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode()
                                    break  # Salir una vez que encuentres el texto plano
                                elif content_type == "text/html":
                                    body = part.get_payload(decode=True).decode()
                        else:
                            body = msg.get_payload(decode=True).decode()

                        #print("Cuerpo del correo:", body)

                        # Procesar el cuerpo con BeautifulSoup
                        try:
                            soup = BeautifulSoup(body, 'html.parser')
                            prompt = str(soup) + ". Dame el código de verificación en JSON. con la key 'code' y en otra key 'check' true o false si el código es de 'instagram'."
                            resp = chat_with_gpt(prompt)
                            if resp["code"] == 200:
                                logging.info("----------------------------------------")
                                logging.info("Respuesta de GPT:"+ resp)
                                logging.info("----------------------------------------")
                                resp = json.loads(resp["data"])
                                if resp["check"]:
                                    confirmation_code = resp["code"]
                                    logging.info(f"Código de confirmación: {confirmation_code}")
                                    status_received = True
                                    break
                            else:
                                logging.info(f"Error in consult code with api: {resp}")
                        except Exception as e:
                            logging.info("Error procesando el cuerpo: " + str(e))

        except Exception as e:
            logging.info("Error general al recibir correos: " + str(e))
        finally:
            mail.logout()

        return confirmation_code

    def received_v1(self, _server):
        self.smtp_server = "mail."+_server
        # Conectar al servidor
        mail = imaplib.IMAP4_SSL(self.smtp_server, self.puerto_imap)
        mail.login(self.username, self.password)

        # Seleccionar la bandeja de entrada
        mail.select("inbox")

        # Ejecutar el bucle de verificación por 1 minuto
        confirmation_code = None
        #start_time = time.time()
        #while time.time() - start_time < 60:
        try:
            # Buscar correos no leídos
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = list(messages[0].split())
            #print("Check message: "+str(time.time() - start_time))
            status_received = False
            email_ids.reverse()
            for e_id in email_ids:
                status, msg_data = mail.fetch(e_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        from_ = msg.get("From")
                        print("Subject:", subject)
                        print("From:", from_)

                        # Obtener el cuerpo del correo
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    print("Body:", body)
                                #    pass
                        else:
                            body = msg.get_payload(decode=True).decode()
                            print("Body:", body)

                        try:
                            soup = BeautifulSoup(body, 'html.parser')
                            prompt = soup+".dame el codigo de verificacion de 6 digitos en json. con la key 'code' y en otra key 'check' true o false si el codigo es de 'instagram'."
                            resp = chat_with_gpt(prompt)
                            print(resp)
                            if resp["check"]:
                                confirmation_code = resp["code"]
                                try:
                                    # Extraer el código de confirmación (asumiendo que el formato es consistente)
                                    print(f"Código de confirmación: {confirmation_code}")
                                    status_received = True
                                    break
                                except Exception as e:
                                    logging.info("Error message email: "+str(e))
                        except Exception as e2:
                            logging.info("Error exception body: "+str(e2))
                
        except Exception as e3:
            logging.info("Error general while: "+str(e3))
        mail.logout()

        return confirmation_code
    
    # Verificar que el correo proviene de Instagram y contiene el texto esperado
    def is_instagram(self, soup):
        # Verificar que el título contiene "Facebook" o "Instagram"
        title = soup.title.string if soup.title else ""
        if "Instagram" not in title and "Facebook" not in title:
            return False

        # Verificar que el cuerpo contiene el texto esperado
        expected_text = "Someone tried to sign up for an Instagram account"
        body_text = soup.get_text()
        if expected_text not in body_text:
            return False

        return True

    def send(self, text):
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = self.to
        msg['Subject'] = "Instagram"

        # Cuerpo del correo en HTML
        body = text  # `text` debería contener el HTML que deseas enviar
        msg.attach(MIMEText(body, 'html'))  # Cambia 'plain' a 'html'

        # Enviar el correo
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            text = msg.as_string()
            server.sendmail(self.username, msg['To'], text)
            print("Correo enviado exitosamente")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()

class WebActions:
    def __init__(self, driver):
        self.driver = driver

    def save_session(self, _driver):
        status = False
        logging.info(f"Check button save session")
        if "¿Guardar tu información de inicio de sesión?" in str(_driver.page_source) or "Save your login info?" in str(_driver.page_source):
            status = True
            for b in _driver.find_elements_by_xpath("//div[@role='button']"):
                if "Ahora no" == str(b.text).strip() or "Not now" == str(b.text).strip():
                    b.click()
        return status

    def notification(self, _driver):
        logging.info(f"Check button notifications")
        if "Activar notificaciones" in str(_driver.page_source) or "Turn on Notifications" in str(_driver.page_source):
            for b in _driver.find_elements_by_tag_name("button"):
                #print(b.text)
                if "Ahora no" == str(b.text).strip() or "Not Now" in str(b.text).strip() or "Not now" in str(b.text).strip():
                    b.click()
                    break

    def perform_button_click_and_input(self, max_timeout=120):
        print("Check buton Send message")
        start_time = time.time()  # Captura el tiempo de inicio
        status = False
        while True:
            try:
                # Busca todos los botones con el rol "button"
                buttons = self.driver.find_elements_by_xpath("//div[@role='button']")
                for button in buttons:
                    # Verifica si el texto del botón contiene las frases deseadas
                    if 'Enviar mensaje' in button.text or 'Message' in button.text or 'Send Message' in button.text or 'Send message' in button.text:
                        button.click()  # Haz clic en el botón encontrado
                        print("Clic realizado en el botón 'Enviar mensaje' o 'Message'.")
                        status = True  # Regresa True si se hizo clic
                        break
                if status:
                    break
                # Verifica si ha pasado el tiempo máximo permitido
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_timeout:
                    print("Timeout: No se pudo hacer clic en el botón en {} segundos.".format(max_timeout))
                    status = False
                    break

                time.sleep(1)  # Espera 1 segundo antes de intentar de nuevo
            except NoSuchElementException:
                print("No se encontró el botón 'Enviar mensaje' o 'Message'. Intentando de nuevo...")
                continue
            except Exception as e01:
                print("Error in search button follow: "+str(e01))
        print("Finish Check buton Send message")
        return status

    def click_on_input_field(self, max_timeout=120, follow=""):
        print("Check send message")
        start_time = time.time()  # Captura el tiempo de inicio
        status = False
        while True:
            try:
                # Busca el campo de entrada por su nombre
                input_field = self.driver.find_elements_by_xpath("//input[@name='queryBox']")
                if input_field:
                    try:
                        for t in follow:
                            input_field[0].send_keys(t)  # Ingresa el texto del seguidor
                        status = True
                    except Exception as e:
                        logging.info(f"Error in textbox {e}")
                    print("Texto ingresado en el campo de entrada: '{}'".format(follow))
                    if status:
                        break
                # Verifica si ha pasado el tiempo máximo permitido
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_timeout:
                    print("Timeout: No se pudo hacer clic en el campo de entrada en {} segundos.".format(max_timeout))
                    break

                time.sleep(1)  # Espera 1 segundo antes de intentar de nuevo
            except NoSuchElementException:
                print("No se encontró el campo de entrada. Intentando de nuevo...")
                continue
            except Exception as e01:
                print("Error in search button follow: "+str(e01))
        print("Finish Check send message")
        return status

    def perform_button_click_with_checkbox(self, max_timeout=120):
        print("Check click item in search")
        start_time = time.time()  # Captura el tiempo de inicio
        status = False
        while True:
            try:
                self.save_session(self.driver)
                self.notification(self.driver)
                if "No account found." in str(self.driver.page_source):
                    print("Check click item. No account found.")
                    break
                # Busca todos los botones con el rol "button"
                buttons = self.driver.find_elements_by_xpath('//div[@role="button"]')
                #print(buttons)
                for button in buttons:
                    # Busca el checkbox dentro del botón
                    checkbox = button.find_elements_by_xpath('//input[@name="ContactSearchResultCheckbox"]')
                    #print(checkbox)
                    if checkbox and checkbox[0].get_attribute('aria-checked') == 'false':
                        checkbox[0].click()
                        print("Clic realizado en un botón con checkbox no seleccionado.")
                        status = True  # Regresa True si se hizo clic
                        break
                
                if status:
                    break

                # Verifica si ha pasado el tiempo máximo permitido
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_timeout:
                    print("Timeout: No se pudo hacer clic en un botón con checkbox en {} segundos.".format(max_timeout))
                    break

                time.sleep(1)  # Espera 1 segundo antes de intentar de nuevo
            except NoSuchElementException:
                print("No se encontró ningún botón con checkbox. Intentando de nuevo...")
                continue
            except Exception as e01:
                print("Error in search button follow: "+str(e01))
                if "No account found." in str(self.driver.page_source):
                    print("Check click item. No account found.")
                    break

        print("Finish Check click item in search")
        return status

    def perform_button_click_chat(self, max_timeout=120):
        print("Check click button Chat")
        start_time = time.time()  # Captura el tiempo de inicio
        status = False
        while True:
            try:
                # Busca todos los botones con el rol "button"
                buttons = self.driver.find_elements_by_xpath('//div[@role="button"]')
                for button in buttons:
                    if 'Chat' in button.text:
                        button.click()
                        print("Clic realizado en el botón 'Chat'.")
                        status = True  # Regresa True si se hizo clic
                        break
                if status:
                    break
                # Verifica si ha pasado el tiempo máximo permitido
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_timeout:
                    print("Timeout: No se pudo hacer clic en el botón 'Chat' en {} segundos.".format(max_timeout))
                    break

                time.sleep(1)  # Espera 1 segundo antes de intentar de nuevo
            except NoSuchElementException:
                print("No se encontró el botón 'Chat'. Intentando de nuevo...")
                continue
            except Exception as e01:
                print("Error in search button follow: "+str(e01))
        print("Finish Check click button Chat")
        return status

    def perform_click_and_focus_on_editable_div(self, max_timeout=120):
        start_time = time.time()  # Captura el tiempo de inicio
        while True:
            try:
                # Busca el div editable
                editable_div = self.driver.find_elements_by_xpath('//div[@contenteditable="true"][@role="textbox"]')
                if editable_div:
                    editable_div[0].click()  # Simula un clic en el div editable
                    print("Clic realizado y foco dado en el div editable.")
                    return True  # Regresa True si se hizo clic

                # Verifica si ha pasado el tiempo máximo permitido
                elapsed_time = time.time() - start_time
                if elapsed_time >= max_timeout:
                    print("Timeout: No se pudo hacer clic en el div editable en {} segundos.".format(max_timeout))
                    return False

                time.sleep(1)  # Espera 1 segundo antes de intentar de nuevo
            except NoSuchElementException:
                print("No se encontró el div editable. Intentando de nuevo...")
                continue
            except Exception as e01:
                print("Error in search button follow: "+str(e01))
    
    def send_dm(self, text_dm):
        print("Check Send dm")
        status = False
        try:
            for t in text_dm:
                self.driver.find_element_by_xpath("//div[@role='textbox']").send_keys(t)
        except Exception as e:
            logging.info("Error in textbox")

        if "Activar notificaciones" in str(self.driver.page_source) or "Turn on Notifications" in str(self.driver.page_source):
            for b in self.driver.find_elements_by_tag_name("button"):
                if "Ahora no" == str(b.text).strip() or "Not Now" in str(b.text).strip() or "Not now" in str(b.text).strip():
                    b.click()
                    break
        time.sleep(2)
        try:
            # Not everyone can message this account.
            buttons = self.driver.find_elements_by_xpath("//div[@role='button']")
            for b in buttons:
                if "Enviar" in b.text or "Send" in b.text:
                    b.click()
                    status = True
                    break
        except Exception as e:
            logging.info("Error in button Enviar mensaje")
        print("Finish Check Send dm")
        return status

class ManageInsta:
    def __init__(self, email, password_email, password, username, name, end_search) -> None:
        self.url = "https://www.instagram.com"
        self.driver = None
        self._email = email
        self._password = password
        self._password_email = password_email
        self._username = username
        self._name = name
        self.end_search = end_search
        self._active_search = True

        self.day = str(random.randint(1, 27))
        self.month = random.choice(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"])
        self.anio = str(random.randint(1990, 2005))

    @property
    def cant(self):
        return self.end_search

    @property
    def active_search(self):
        return self._active_search
    
    @active_search.setter
    def active_search(self, state):
        self._active_search = state

    def create(self):
        pass
    
    def _webdriver(self):
        #if platform.system() == "Windows":
        return self._driver_chrome()
        #else:
        #return self._driver_firefox()

    def _driver_firefox(self):
        options = Options()
        #options.add_argument("--headless")
        #options.add_argument("--disable-gpu")
        #options.add_argument("--no-sandbox")
        # Configura la dirección del proxy y el puerto
        proxy_address = "144.76.124.83:10000"

        # Crea una instancia de Options para Firefox
        options.set_preference("network.proxy.type", 1)  # Establece el tipo de proxy a manual
        options.set_preference("network.proxy.http", proxy_address.split(':')[0])  # Dirección del proxy HTTP
        options.set_preference("network.proxy.http_port", int(proxy_address.split(':')[1]))  # Puerto del proxy HTTP
        options.set_preference("network.proxy.ssl", proxy_address.split(':')[0])  # Dirección del proxy SSL
        options.set_preference("network.proxy.ssl_port", int(proxy_address.split(':')[1]))  # Puerto del proxy SSL
        options.set_preference("network.proxy.ftp", proxy_address.split(':')[0])  # Dirección del proxy FTP
        options.set_preference("network.proxy.ftp_port", int(proxy_address.split(':')[1]))  # Puerto del proxy FTP
        options.set_preference("network.proxy.socks", proxy_address.split(':')[0])  # Dirección del proxy SOCKS
        options.set_preference("network.proxy.socks_port", int(proxy_address.split(':')[1]))  # Puerto del proxy SOCKS
        options.set_preference("network.proxy.socks_version", 5)  # Versión del proxy SOCKS
        options.set_preference("network.proxy.socks_remote_dns", True)  # Para usar DNS remoto
        #path_extention = os.path.abspath("autobot.py").replace("autobot.py", "captchaSolver")
        #options.add_argument(f"--load-extension={path_extention}")
        if platform.system() == "Windows":
            path_file = Service(os.path.abspath("geckodriver.exe"))
        else:
            path_file = Service(os.path.abspath("geckodriver"))
        return webdriver.Firefox(service=path_file, options=options)

    def _driver_chrome(self, proxy_extention=None):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("no-sandbox")
        options.add_argument("--lang=en")  # Cambia el idioma a inglés
        path_extention = os.path.abspath("autobot.py").replace("autobot.py", "captchaSolver")
        #path_extention2 = os.path.abspath("autobot.py").replace("autobot.py", "holaVpn")
        #path_extention3 = os.path.abspath("autobot.py").replace("autobot.py", "VeePn")
        #path_extention4 = os.path.abspath("autobot.py").replace("autobot.py", "vpn")
        options.add_argument(f"--load-extension={path_extention}")
        proxy_address = "144.76.124.83:10000"
        #options.add_argument(f'--proxy-server=http://{proxy_address}')  # Establece el proxy
        if platform.system() == "Windows":
            path_driver = os.path.abspath("chromedriver.exe")
        else:
            path_driver = os.path.abspath("chromedriver")
        print(path_driver)
        #if proxy_extention:
        #    options.add_extension(proxy_extention)
        return webdriver.Chrome(path_driver, options=options)

    def create_account(self, _driver):
        try:
            _driver.get(self.url)
            _driver.implicitly_wait(15)
            #_driver.maximize_window()
            time.sleep(4)
            self.check_cookies(_driver)
            for a in _driver.find_elements_by_tag_name("a"):
                #logging.info(a.text)
                if "Regístrate" == str(a.text).strip() or "Sign up" in str(a.text).strip():
                    a.click()
                    break
            sleep(2)
            _driver.find_element_by_xpath("//input[@name='emailOrPhone']").send_keys(self._email)
            sleep(1)
            _driver.find_element_by_xpath("//input[@name='password']").send_keys(self._password)
            sleep(1)
            _driver.find_element_by_xpath("//input[@name='fullName']").send_keys(self._name)
            sleep(1)
            _driver.find_element_by_xpath("//input[@name='username']").send_keys(self._username)
            sleep(1)
            #screen_width = _driver.execute_script("return window.screen.availWidth;")
            #screen_height = _driver.execute_script("return window.screen.availHeight;")
            #print(screen_width, screen_height)
            # Calcular las dimensiones de cada ventana (mitad de la pantalla)
            #half_screen_width = screen_width // 2
            #_driver.set_window_size(half_screen_width, screen_height)
            #_driver.set_window_position(0, 0)

            for b in _driver.find_elements_by_xpath("//button[@type='submit']"):
                if "Registrarte" == str(b.text).strip() or "Siguiente" == str(b.text).strip() or "Sign up" in str(b.text).strip() or "Next" in str(b.text).strip():
                    logging.info("Click button Registrarte")
                    b.click()
                    break
            time.sleep(2)
            if "Este nombre de usuario no está disponible. Prueba otro." in _driver.page_source or "This username isn't available. Please try another." in _driver.page_source:
                logging.info(f"Este nombre de usuario no está disponible. Prueba otro: {self._email}")
                return False, False

            time.sleep(2)

            for day in _driver.find_element_by_xpath("//select[@title='Day:']").find_elements_by_tag_name("option"):
                if day.text == self.day:
                    day.click()

            for day in _driver.find_element_by_xpath("//select[@title='Month:']").find_elements_by_tag_name("option"):
                if day.text == self.month:
                    day.click()

            for day in _driver.find_element_by_xpath("//select[@title='Year:']").find_elements_by_tag_name("option"):
                if day.text == self.anio:
                    day.click()

            for b in _driver.find_elements_by_tag_name("button"):
                if "Siguiente" == str(b.text).strip() or "Next" == str(b.text).strip():
                    b.click()
                    logging.info("Click button Siguiente date")
                    break
            
            time.sleep(5)
            re_captcha = ReCapchat(_driver)
            re_captcha.run()

            service_email = ServiceEmail(
                username=self._email,
                password=self._password_email,
                to=""
            )
            start_time = time.time()
            status = True
            block = False
            logging.info("Check code confirmation")
            time_out_end = 241
            time_out_resend = 100
            while time.time() - start_time < time_out_end:
                try:
                    confirmation_code = service_email.received(self._email.split("@")[1])
                    #logging.info(confirmation_code)
                except Exception as e:
                    logging.info(e)
                    status = False
                    break
                if confirmation_code != None:
                    logging.info(confirmation_code)
                    _driver.find_element_by_xpath("//input[@name='email_confirmation_code']").send_keys(confirmation_code)
                    try:
                        for b in _driver.find_elements_by_xpath("//div[@role='button']"):
                            if "Siguiente" == str(b.text).strip() or "Next" == str(b.text).strip():
                                b.click()
                                break
                    except Exception as ebtn:
                        logging.info("Error buttonclick: "+str(ebtn))
                    try:
                        time.sleep(1)
                        if "El código no es válido. Puedes solicitar uno nuevo." in str(_driver.page_source) or "That code isn't valid. You can request a new one." in str(_driver.page_source):
                            logging.info("El código no es válido. Puedes solicitar uno nuevo.")
                            _driver.find_element_by_xpath("//input[@name='email_confirmation_code']").clear()
                            self.resend_code(_driver)
                            time.sleep(3)
                            re_captcha = ReCapchat(_driver)
                            re_captcha.run()
                        else:
                            print("[+] Check code success...")
                            time.sleep(5)
                            if "The IP address you are using has been flagged as an open proxy. If you believe this to be incorrect, please visit" in str(_driver.page_source):
                                status = False
                            else:
                                status = True
                            break
                    except Exception as ebtn2:
                        logging.info("Error Check code confirmation: "+str(ebtn2))
                else:
                    if time.time() - start_time > time_out_resend:
                        self.resend_code(_driver)
                        time.sleep(3)
                        re_captcha = ReCapchat(_driver)
                        re_captcha.run()
                        time_out_resend += time_out_resend
                    status = False
            time.sleep(10)
            self.notification(_driver)
            time.sleep(5)
            block = self.check_suspend(_driver)
        except Exception as e:
            logging.info("Error: "+str(e))
            status = False
            block = False
        print(status, block)
        return status, block
    
    def resend_code(self, _driver):
        logging.info("[+] Resend code...")
        for b in _driver.find_elements_by_xpath("//div[@role='button']"):
            if "Reenviar código." == str(b.text).strip() or "Resend code." == str(b.text).strip()  or "Resend Code." == str(b.text).strip():
                logging.info("[+] Resend code Success...")
                b.click()
                break
    
    def check_cookies(self, _driver):
        for b in _driver.find_elements_by_tag_name("button"):
            if "Permitir todas las cookies" in b.text or "Allow all cookies" in b.text:
                b.click()
                time.sleep(5)
                break

    def sign_in(self, _driver):
        _driver.get(self.url)
        _driver.implicitly_wait(15)
        _driver.maximize_window()
        time.sleep(5)
        self.check_cookies(_driver)
        _driver.find_element_by_xpath("//input[@name='username']").send_keys(self._email)
        _driver.find_element_by_xpath("//input[@name='password']").send_keys(self._password)
        time.sleep(1)
        for b in _driver.find_elements_by_xpath("//button[@type='submit']"):
            if "Entrar" == str(b.text).strip() or "Log in" == str(b.text).strip():
                b.click()
                break
        time.sleep(10)
        status = self.save_session(_driver)
        if not status:
            time.sleep(10)
            block = self.check_session(_driver)
            if not block:
                time.sleep(2)
                block = self.check_suspend(_driver)
        else:
            block = False
            try:
                time.sleep(4)
                self.notification(_driver)
                time.sleep(2)
                self.config_account(_driver)
                time.sleep(2)
                self.config_account(_driver)
            except Exception as e:
                logging.info("Error 756: "+str(e))
        return status, block
    
    def config_account(self, _driver):
        logging.info(f"Button Next with Find friends and accounts you like")
        if "Find friends and accounts you like" in _driver.page_source:
            for b in _driver.find_elements_by_xpath("//div[@role='button']"):
                if "Next" == str(b.text).strip() or "Siguiente" == str(b.text).strip():
                    b.click()
                    break

    def check_session(self, _driver):
        block = False
        for b in _driver.find_elements_by_xpath("//button[@type='submit']"):
            if "Entrar" == str(b.text).strip() or "Log in" == str(b.text).strip():
                if "Tu contraseña no es correcta. Vuelve a comprobarla." in _driver.page_source or "Sorry, your password was incorrect. Please double-check your password." in _driver.page_source:
                    block = True
                    logging.info(f"Account login problem: {self._email}")
                break
        return block

    def check_suspend(self, _driver):
        block = False
        logging.info(f"Check account suspend")
        if "hemos suspendido tu cuenta permanentemente." in _driver.page_source or "Intento de inicio de sesión sospechoso" in _driver.page_source or "We Detected An Unusual Login Attempt" in _driver.page_source or "Suspicious Login Attempt" in _driver.page_source or "We suspended your account" in _driver.page_source  or "We suspect automated behavior on your account" in _driver.page_source:
            logging.info(f"Account login problem block: {self._email}")
            block = True
        return block

    def save_session(self, _driver):
        status = False
        logging.info(f"Check button save session")
        if "¿Guardar tu información de inicio de sesión?" in str(_driver.page_source) or "Save your login info?" in str(_driver.page_source):
            status = True
            for b in _driver.find_elements_by_xpath("//div[@role='button']"):
                if "Ahora no" == str(b.text).strip() or "Not now" == str(b.text).strip():
                    b.click()
        return status

    def notification(self, _driver):
        logging.info(f"Check button notifications")
        if "Activar notificaciones" in str(_driver.page_source) or "Turn on Notifications" in str(_driver.page_source):
            for b in _driver.find_elements_by_tag_name("button"):
                #print(b.text)
                if "Ahora no" == str(b.text).strip() or "Not Now" in str(b.text).strip() or "Not now" in str(b.text).strip():
                    b.click()
                    break

    def logout(self, _driver):
        _driver.get(self.url)
        _driver.implicitly_wait(15)
        _driver.maximize_window()
        time.sleep(4)
        block = False
        status = False
        block = self.check_suspend(_driver)
        if not block:
            #print("Activar notificaciones" in str(_driver.page_source))

            self.notification(_driver)

            time.sleep(1)
            buttons = _driver.find_elements_by_xpath("//a[@role='link']")
            for b in buttons:
                if "Más" == str(b.text).strip("") or "More" == str(b.text).strip(""):
                    b.click()
                    break
            time.sleep(1)
            _dialog = _driver.find_elements_by_xpath("//div[@role='dialog']")
            for d in _dialog:
                if "Salir" in d.text or "Log out" in d.text:
                    for s in d.find_elements_by_tag_name("div"):
                        if "Salir" == str(s.text).strip() or "Log out" == str(s.text).strip():
                            #print(str(s.text).strip())
                            status = True
                            s.click()
                            break
                    break
        return status, block

    def send_dm(self, person_user, text_dm, _driver):
        _driver.get(self.url+"/"+person_user+"/")
        _driver.implicitly_wait(15)
        #_driver.maximize_window()
        time.sleep(2)
        block = False
        status = False
        if "hemos suspendido tu cuenta permanentemente." in _driver.page_source or "Intento de inicio de sesión sospechoso" in _driver.page_source or "We Detected An Unusual Login Attempt" in _driver.page_source or "Suspicious Login Attempt" in _driver.page_source or "We suspended your account" in _driver.page_source or "We suspect automated behavior on your account" in _driver.page_source:
            block = True
            logging.info(f"Account login problem block: {self._email}")
        if not block:
            if "Esta página no está disponible." not in _driver.page_source and "Esta cuenta es privada" not in _driver.page_source and "Síguela para ver sus fotos o vídeos." not in _driver.page_source and "This account is private" not in _driver.page_source:
                # try:
                #     buttons = _driver.find_elements_by_xpath("//button[@type='button']")
                #     for b in buttons:
                #         if "Seguir" in b.text or "Follow" in b.text:
                #             b.click()
                #             break
                # except Exception as e:
                #     logging.info("Error in button Seguir")

                time.sleep(2)
                button_message = False
                try:
                    buttons = _driver.find_elements_by_xpath("//div[@role='button']")
                    for b in buttons:
                        if "Enviar mensaje" in b.text or "Message" in b.text:
                            b.click()
                            button_message = True
                            break
                except Exception as e:
                    logging.info("Error in button Enviar mensaje")
                if button_message:
                    time.sleep(3)
                    try:
                        for t in text_dm:
                            _driver.find_element_by_xpath("//div[@role='textbox']").send_keys(t)
                    except Exception as e:
                        logging.info("Error in textbox")

                    if "Activar notificaciones" in str(_driver.page_source) or "Turn on Notifications" in str(_driver.page_source):
                        for b in _driver.find_elements_by_tag_name("button"):
                            if "Ahora no" == str(b.text).strip() or "Not Now" in str(b.text).strip() or "Not now" in str(b.text).strip():
                                b.click()
                                break
                    time.sleep(2)
                    try:
                        # Not everyone can message this account.
                        buttons = _driver.find_elements_by_xpath("//div[@role='button']")
                        for b in buttons:
                            if "Enviar" in b.text or "Send" in b.text:
                                logging.info(f"[+] Send Message with user {person_user}...")
                                b.click()
                                status = True
                                break
                    except Exception as e:
                        logging.info("Error in button Enviar mensaje")
        return status, block
    
    def change_size_windows(self, _driver):
        screen_width = _driver.execute_script("return window.screen.availWidth;")
        screen_height = _driver.execute_script("return window.screen.availHeight;")
        print(screen_width, screen_height)
        #Calcular las dimensiones de cada ventana (mitad de la pantalla)
        half_screen_width = screen_width // 2
        _driver.set_window_size(half_screen_width, screen_height)
        _driver.set_window_position(0, 0)

    def send_dm_v2(self, person_user, text_dm, _driver):
        _driver.get(self.url+"/direct/inbox/")
        _driver.implicitly_wait(15)
        #_driver.minimize_window()
        time.sleep(2)
        self.change_size_windows(_driver)
        block = False
        status = False
        block = self.check_suspend(_driver)
        if not block:
            web_actions = WebActions(_driver)
            # Llama a las funciones según sea necesario
            web_actions.perform_button_click_and_input()
            print(f"Seguidor para buscar: {person_user}")
            web_actions.click_on_input_field(follow=person_user)
            time.sleep(2)
            _check = web_actions.perform_button_click_with_checkbox()
            if _check:
                web_actions.perform_button_click_chat()
                time.sleep(1)
                #web_actions.perform_click_and_focus_on_editable_div()
                status = web_actions.send_dm(text_dm=text_dm)
                logging.info(f"[+] Send Message with user {person_user}...")

        return status, block

    def get_users(self, person_user, _driver):
        _driver.get(self.url+"/"+person_user+"/")
        _driver.implicitly_wait(15)
        #_driver.maximize_window()

        time.sleep(3)
        _driver.find_element_by_xpath("//a[@href='/crece.en.redes.sociales/followers/']").click()
        time.sleep(5)
        return self.dialog_data(_driver)

    def dialog_data(self, _driver):
        time.sleep(5)
        _dialog = _driver.find_elements_by_xpath("//div[@role='dialog']")
        div_class = ""
        links_user = []
        #for d in _dialog:
            #print(d.get_attribute("innerHTML"))
            #print("----------------------------------------------------")
        if "Seguidores" in str(_dialog[1].get_attribute("innerHTML")):
            soup = BeautifulSoup(_dialog[1].get_attribute("innerHTML"), 'html.parser')
            if "Siguiendo" in str(_dialog[1].get_attribute("innerHTML")):
                for c in soup.find_all("div")[19].get("class"):
                    div_class += c+" "

                logging.info(f"[+] Account with used... {div_class}")
            else:
                next_div = soup.find("div").find("div")
                #print(next_div.find_all("div")[19])
                #for nd in next_div.find_all("div"):
                #    print("-------------------------------------------")
                #    print(nd)
                for c in next_div.find_all("div")[13].get("class"):
                    div_class += c+" "
                
                logging.info(f"[+] Account new... {div_class}")

            #print(div_class)
            acum = 400
            _dialog2 = _driver.find_element_by_xpath("//div[@class='"+div_class.strip()+"']")
            while self.active_search:
                try:
                    _driver.execute_script("arguments[0].scrollTop="+str(acum)+";", _dialog2)
                    acum += 600
                    time.sleep(1)
                    _dialog = _driver.find_elements_by_xpath("//div[@role='dialog']")
                    soup = BeautifulSoup(_dialog[1].get_attribute("innerHTML"), 'html.parser')
                    for a in soup.find_all("a", {"role":"link"}):
                        #print(a.get("href"))
                        if str(a.get("href")).strip()[1:-1] not in links_user:
                            #print(str(a.get("href")).strip()[1:-1])
                            links_user.append(str(a.get("href")).strip()[1:-1])
                            yield str(a.get("href")).strip()[1:-1]

                    #if len(links_user) >= self.end_search:
                    #    break
                except Exception as e:
                    logging.info("Error in get follows sleep 15 seconds...")
                    time.sleep(15)
            
            for b in _dialog2.find_elements_by_xpath("//button[@type='button']"):
                if "Cerrar" in b.get_attribute("innerHTML"):
                    #print(b.get_attribute("innerHTML"))
                    b.click()
                    break
            #self.write_file(links_user)
        #return links_user

        #print("-------------------------------2------------------------------")
        #_dialog2 = _driver.find_element_by_xpath("//div[@style='height: auto; overflow: hidden auto;']")
        #print(_dialog2.get_attribute("innerHTML"))
        #print(_dialog2)
        #_driver.execute_script("arguments[0].scrollTop=200;", _dialog2)

        #_dialog3 = _driver.find_element_by_xpath("//div[@style='height: auto; overflow: hidden auto;']/preceding-sibling::div")
        #print(_dialog3)
        #actions = ActionChains(_driver)
        #actions.move_to_element(_dialog2).perform()

    def close(self, _driver):
        _driver.close()

    def write_file(self, data):
        with open("file.txt", "w") as file:
            for d in data:
                file.write(d+"\n")

class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration

DRIVER = {}
websocket = None

def create_accounts(data):
    manage_insta = ManageInsta(
        email=data["email"],
        password_email=data["password_email"],
        password=data["password"],
        username=data["username"],
        name=data["username"],
        end_search=0
    )
    _driver = manage_insta._webdriver()
    status, block = manage_insta.create_account(_driver)
    if status:
        DRIVER[data["email"]] = {"driver": _driver, "instance": manage_insta}
        logging.info("[+] SignUp success...")
    else:
       manage_insta.close(_driver)
    return status, block

# def sign_in_account(data):
#     manage_insta = ManageInsta(
#         email=data["email"],
#         password_email=data["password_email"],
#         password=data["password"],
#         username=data["username"],
#         name=data["username"],
#         end_search=0
#     )
#     _driver = manage_insta._webdriver()
#     #manage_insta.create_account(_driver)
#     state, block = manage_insta.sign_in(_driver)
#     logging.info(state, block)
#     time.sleep(5)
#     if not block:
#         manage_insta.logout(_driver)
#         # if state:
#         #     data = manage_insta.get_users("crece.en.redes.sociales")
#         #     for d in data:
#         #manage_insta.send_dm("thehollywoodhustle", "Yo bro, this is the an automatic message from the demo of the instahack software we are working on. we are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.")
#         time.sleep(10)

#     manage_insta.close(_driver)

# def send_dm_account(data):
#     manage_insta = ManageInsta(
#         email=data["email"],
#         password_email=data["password_email"],
#         password=data["password"],
#         username=data["username"],
#         name=data["username"],
#         end_search=0
#     )
#     _driver = manage_insta._webdriver()
#     #manage_insta.create_account(_driver)
#     state, block = manage_insta.sign_in(_driver)
#     #print(state, block)
#     #time.sleep(1)
#     #manage_insta.logout(_driver)
#     logging.info(state)
#     if state:
#         # data = manage_insta.get_users("crece.en.redes.sociales")
#         # for d in data:
#         manage_insta.send_dm(
#             "wuilsoft", 
#             "Yo bro, this is the an automatic message from the demo of the instahack software we are working on. we are Anonymous. We are Legion. We do not forgive. We do not forget. Expect us.",
#             _driver    
#         )
#         manage_insta.logout(_driver)
#     time.sleep(10)

#     manage_insta.close(_driver)


def sign_in_with_browse(data):
    manage_insta = ManageInsta(
        email=data["email"],
        password_email=data["password_email"],
        password=data["password"],
        username=data["username"],
        name=data["username"],
        end_search=0
    )
    _driver = manage_insta._webdriver()
    status, block = manage_insta.sign_in(_driver)
    if status:
        logging.info("[+] SignIn success...")
        DRIVER[data["email"]] = {"driver": _driver, "instance": manage_insta}
    else:
        _driver.close()
    return status, block

def logout_with_browse(data):
    status, block = DRIVER[data["email"]]["instance"].logout(DRIVER[data["email"]]["driver"])
    sleep(3)
    DRIVER[data["email"]]["instance"].close(DRIVER[data["email"]]["driver"])
    del DRIVER[data["email"]]
    logging.info("[+] LogOut success...")
    return status, block

def send_dm_with_browse(data):
    status, block = DRIVER[data["email"]]["instance"].send_dm_v2(
        data["follow"],
        data["text"],
        DRIVER[data["email"]]["driver"]
    )
    if block:
        DRIVER[data["email"]]["instance"].close(DRIVER[data["email"]]["driver"])
        del DRIVER[data["email"]]
    logging.info("[+] Send DM success...")
    return status, block

@sync_to_async
def task_in_async(data) -> bool:
    if data["object"] == "CreateAccount":
        status, block = create_accounts(data)
    # elif data["object"] == "SignInAccount":
    #     status, block = sign_in_account(data)
    # elif data["object"] == "SendDmAccount":
    #     status, block = send_dm_account(data)
    elif data["object"] == "SignIn":
        status, block = sign_in_with_browse(data)
    elif data["object"] == "LogOut":
        status, block = logout_with_browse(data)
    elif data["object"] == "SendDm":
        status, block = send_dm_with_browse(data)
    return status, block

async def task_follow_current(data):
    status, block = await task_in_async(data)
    aux_data = data
    aux_data["status"] = status
    aux_data["block"] = block
    aux_data["machine"] = "BotMaster"
    await websocket.send(json.dumps(aux_data))

async def task_account_current(data):
    status, block = await task_in_async(data)
    aux_data = data
    aux_data["status"] = status
    aux_data["block"] = block
    aux_data["machine"] = "BotMaster"
    await websocket.send(json.dumps(aux_data))

async def received(machine, _url):
    global websocket
    url = f"wss://{_url}/ws/sync/fda7166a4c4766a77327769624b9416035762dd3/{machine}"
    while True:
        try:
            async with websockets.connect(url) as ws:
                websocket = ws
                logging.info(f"[+] Connection to Server success! MachineName: {machine}")
                print(f"[+] Connection to Server success! MachineName: {machine}")
                while True:
                    try:
                        logging.info("[+] Esperando Datos...")
                        print("[+] Esperando Datos...")
                        r = await websocket.recv()
                        data = json.loads(r)
                        logging.info(f"{data['email']} {data['object']}")
                        print(f"{data['email']} {data['object']}")
                        if data["object"] == "SendDm":
                            #follows = data["follow"]
                            #for f in follows:
                            #data["follow"] = f
                            asyncio.create_task(task_follow_current(data))
                        else:
                            asyncio.create_task(task_account_current(data))
                            
                    except Exception as e:
                        logging.info(f"Error al recibir o procesar datos: " + str(e))
                        break
        except Exception as errorConnect:
            logging.info(f"[-] Error to connect: "+str(errorConnect))
            logging.info(f"[+] Reconected websocket in 5 seconds...")
            await asyncio.sleep(5)
    
    logging.info(f"[+] Disconnection to Server success! MachineName: {machine}")

if __name__ == "__main__":
    # _email = "albertopineda202401@mivisaya.com"
    # _clave = "colombia123*"
    # service_email = ServiceEmail(_email, _clave, _email)
    # service_email.send('<div class="rcmBody" id="message-htmlpart1" style="margin: 0; padding: 0; background-color: #ffffff" dir="ltr"><table border="0" cellspacing="0" cellpadding="0" align="center" id="v1email_table" style="border-collapse: collapse"><tbody><tr><td id="v1email_content" style="font-family: Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif; background: #ffffff"><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td height="20" style="line-height: 20px" colspan="3">&nbsp;</td></tr><tr><td height="1" colspan="3" style="line-height: 1px"></td></tr><tr><td><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse; text-align: center; width: 100%"><tbody><tr><td width="15px" style="width: 15px"></td><td style="line-height: 0px; max-width: 600px; padding: 0 0 15px 0"><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td style="width: 100%; text-align: left; height: 33px"><img height="33" src="program/resources/blocked.gif" style="border: 0"></td></tr></tbody></table></td><td width="15px" style="width: 15px"></td></tr></tbody></table></td></tr><tr><td><table border="0" width="430" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin: 0 auto 0 auto"><tbody><tr><td><table border="0" width="430px" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin: 0 auto 0 auto; width: 430px"><tbody><tr><td width="15" style="display: block; width: 15px">&nbsp;&nbsp;&nbsp;</td></tr><tr><td width="12" style="display: block; width: 12px">&nbsp;&nbsp;&nbsp;</td><td><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td></td><td style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px"><p style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px">Hola:</p><p style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px">Alguien intentó registrarse en una cuenta de Instagram con manuel_mujica202301@servicio-tecnico-apple.shop. Si fuiste tú, ingresa este código de registro en la app:</p></td></tr></tbody></table></td></tr><tr><td></td><td style="padding: 10px; color: #565a5c; font-size: 32px; font-weight: 500; text-align: center; padding-bottom: 25px">581043</td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin: 0 auto 0 auto; width: 100%; max-width: 600px"><tbody><tr><td height="4" style="line-height: 4px" colspan="3">&nbsp;</td></tr><tr><td width="15px" style="width: 15px"></td><td width="20" style="display: block; width: 20px">&nbsp;&nbsp;&nbsp;</td><td style="text-align: center"><div style="padding-top: 10px; display: flex"><div style="margin: auto"><img class="v1img" src="program/resources/blocked.gif" height="26" width="52"></div><br></div><div style="height: 10px"></div><div style="color: #abadae; font-size: 11px; margin: 0 auto 5px auto">© Instagram. Meta Platforms, Inc., 1601 Willow Road, Menlo Park, CA 94025<br></div><div style="color: #abadae; font-size: 11px; margin: 0 auto 5px auto">Este mensaje se envió a <a style="color: #abadae; text-decoration: underline">manuel_mujica202301@servicio-tecnico-apple.shop</a>.<br></div></td><td width="20" style="display: block; width: 20px">&nbsp;&nbsp;&nbsp;</td><td width="15px" style="width: 15px"></td></tr><tr><td height="32" style="line-height: 32px" colspan="3">&nbsp;</td></tr></tbody></table>&nbsp;<span><img src="program/resources/blocked.gif" style="border: 0; width: 1px; height: 1px"></span></div>')
    # time.sleep(10)
    # code = service_email.received(_email.split("@")[1])
    # print(code)
    
    #parser = argparse.ArgumentParser(description='Autobot Instagram')
    #parser.add_argument('machine', type=str, help='Name machine')
    #parser.add_argument('url', type=str, help='url botMaster')
    #Parsear los argumentos
    #args = parser.parse_args()
    #asyncio.run(received(args.machine, args.url))

    # Ejemplo de uso
    prompt = '<div class="rcmBody" id="message-htmlpart1" style="margin: 0; padding: 0; background-color: #ffffff" dir="ltr"><table border="0" cellspacing="0" cellpadding="0" align="center" id="v1email_table" style="border-collapse: collapse"><tbody><tr><td id="v1email_content" style="font-family: Helvetica Neue,Helvetica,Lucida Grande,tahoma,verdana,arial,sans-serif background: #ffffff"><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td height="20" style="line-height: 20px" colspan="3"> nbsp;</td></tr><tr><td height="1" colspan="3" style="line-height: 1px"></td></tr><tr><td><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse text-align: center; width: 100%"><tbody><tr><td width="15px" style="width: 15px"></td><td style="line-height: 0px; max-width: 600px; padding: 0 0 15px 0"><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td style="width: 100%; text-align: left; height: 33px"><img height="33" src="program/resources/blocked.gif" style="border: 0"></td></tr></tbody></table></td><td width="15px" style="width: 15px"></td></tr></tbody></table></td></tr><tr><td><table border="0" width="430" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin: 0 auto 0 auto"><tbody><tr><td><table border="0" width="430px" cellspacing="0" cellpadding="0" style="border-collapse: collapse margin: 0 auto 0 auto; width: 430px"><tbody><tr><td width="15" style="display: block; width: 15px">&nbsp;&nbsp;&nbsp;</td></tr><tr><td width="12" style="display: block; width: 12px"> nbsp;&nbsp;&nbsp;</td><td><table border="0" width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse"><tbody><tr><td></td><td style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px"><p style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px">Hola:</p><p style="margin: 10px 0 10px 0; color: #565a5c; font-size: 18px">Alguien intentó registrarse en una cuenta de Instagram con albertopineda202401@mivisaya.com. Si fuiste tú, ingresa este código de registro en la app:</p></td></tr></tbody></table></td></tr><tr><td>< td><td style="padding: 10px; color: #565a5c; font-size: 32px; font-weight: 500; text-align: center; padding-bottom: 25px">568012</td></tr></tbody></table></td></tr></tbody></table>< td></tr></tbody></table></td></tr></tbody></table><table border="0" cellspacing="0" cellpadding="0" style="border-collapse: collapse; margin: 0 auto 0 auto; width: 100%; max-width: 600px"><tbody><tr><td height="4" style="line-height: 4px" colspan="3">&nbsp;</td></tr><tr><td width="15px" style="width: 15px"></td><td width="20" style="display: block; width: 20px"> nbsp;&nbsp;&nbsp;</td><td style="text-align: center"><div style="padding-top: 10px; display: flex"><div style="margin: auto"><img class="v1img" src="program/resources/blocked.gif" height="26" width="52"></div><br></div><div style="height: 10px"></div><div style="color: #abadae; font-size: 11px; margin: 0 auto 5px auto">© Instagram. Meta Platforms, Inc., 1601 Willow Road, Menlo Park, CA 94025<br></div><div style="color: #abadae; font-size: 11px; margin: 0 auto 5px auto">Este mensaje se envió a <a style="color: #abadae; text-decoration: underline">albertopineda202401@mivisaya.com</a>.<br></div></td><td width="20" style="display: block; width: 20px">&nbsp;&nbsp;&nbsp;</td><td width="15px" style="width: 15px"></td>< tr><tr><td height="32" style="line-height: 32px" colspan="3">&nbsp;</td></tr></tbody></table>&nbsp;<span><img src="program/resources/blocked.gif" style="border: 0; width: 1px; height: 1px"></span></div>dame el codigo de verificacion en json. con la key \'code\' y en otra key check true o false si el codigo es de instagram.'
    respuesta = chat_with_gpt(str(prompt))
    print(json.loads(respuesta["data"]))