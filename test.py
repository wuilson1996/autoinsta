from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Configura la dirección del proxy y el puerto
proxy_address = "144.76.124.83:10000"
username = "d27f280453401cb51f9d__cr.es"
password = "f33b651635b7c9e7"

# Crea una instancia de Options para Chrome
options = Options()
#options.add_argument(f'--proxy-server=http://{proxy_address}')  # Establece el proxy

# Configura el servicio de Chrome (asegúrate de que chromedriver está en la ruta correcta)
service = Service(os.path.abspath("chromedriver.exe"))

# Inicializa el controlador de Chrome con las opciones y el servicio configurados
driver = webdriver.Chrome(service=service, options=options)

# Maneja la ventana emergente de autenticación con usuario y contraseña
# Inyectamos un script que coloca las credenciales en el cuadro emergente
driver.get("http://instagram.com")  # Cambia a la URL que deseas abrir

# Espera un poco para que aparezca la ventana de autenticación
#time.sleep(2)

# Inyecta el nombre de usuario y contraseña en la ventana emergente de autenticación
#driver.execute_script(
#    f"window.open('http://{username}:{password}@{proxy_address}');"
#)

# Espera un momento para la redirección
time.sleep(3600)

# Continúa con la navegación
#driver.get("http://instagram.com")

# Finaliza el controlador
driver.quit()