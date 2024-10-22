from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import os
from autobot import *

def create_browser_with_proxy(proxy_ip="", port=""):

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
    driver = webdriver.Chrome(path_driver, options=options)
    return driver

def test_account(_email, _password, url, _driver):
    manage_insta = ManageInsta(
        email=_email,
        password_email=_password,
        password=_password,
        username=_email.split("@")[0],
        name=_email.split("@")[0],
        end_search=0,
        api_url=url
    )
    #_driver = manage_insta._webdriver()
    status, block = manage_insta.create_account(_driver)

    print(f"Status Register account: {status} and status block: {block}")
    if status:
        sleep(30)

def test_signin(_email, _password, url, _driver):
    manage_insta = ManageInsta(
        email=_email,
        password_email=_password,
        password=_password,
        username=_email.split("@")[0],
        name=_email.split("@")[0],
        end_search=0,
        api_url=url
    )
    status, block = manage_insta.sign_in(_driver)

    print(f"Status Sigin account: {status} and status block: {block}")
    if status:
        sleep(30)

def testing_register(email):
    # Ejemplo de uso
    for i in range(10008, 10020, 1):
        print(f"[+] Starting proxy port: {i}")
        driver = create_browser_with_proxy("144.76.124.83", str(i))
        test_account(email, "colombia123*", "https://15b2-186-80-28-163.ngrok-free.app", driver)
        sleep(5)
        driver.close()
        sleep(2)

def testing_signin(i, email):
    driver = create_browser_with_proxy("144.76.124.83", str(i))
    test_signin(email, "colombia123*", "https://15b2-186-80-28-163.ngrok-free.app", driver)
    sleep(5)
    driver.close()
    sleep(2)


def test_gmail():
    driver = create_browser_with_proxy(proxy_ip="144.76.124.83", port="10007")
    driver.get("https://yahoo.com/")
    driver.implicitly_wait(15)
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    #testing_signin("10008", "paulinarubioz02@servicio-tecnico-apple.shop")
    #testing_register("paulinarubioz02@servicio-tecnico-apple.shop")
    test_gmail()