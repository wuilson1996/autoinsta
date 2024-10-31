from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import random

def create_browser_with_proxy(proxy_ip="", port="", proxy_uso=0):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("no-sandbox")
    options.add_argument("--lang=en")  # Cambia el idioma a inglés
    
    path_extention = os.path.abspath("autobot.py").replace("autobot.py", "captchaSolver")
    #path_extention2 = os.path.abspath("autobot.py").replace("autobot.py", "HolaVPN")
    #path_extention3 = os.path.abspath("autobot.py").replace("autobot.py", "UrbanVPNV2")
    options.add_argument(f"--load-extension={path_extention}")

    # Aplicar el proxy a las opciones de Chrome
    if proxy_uso == True:
        options.add_argument(f'--proxy-server={proxy_ip}:{port}')

    path_driver = os.path.abspath("chromedriver.exe")
    # Inicializar el navegador con el proxy
    return webdriver.Chrome(path_driver, options=options)

driver = create_browser_with_proxy("pe.smartproxy.com", str(random.randint(10000, 20000)), proxy_uso=True)
driver.get("https://instagram.com")
time.sleep(120)