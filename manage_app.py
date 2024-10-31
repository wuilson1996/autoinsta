#from appium.options.android import UiAutomator2Options
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import logging
import json
import random

class ManageApp:
    API_URL = "https://bb88-186-80-29-32.ngrok-free.app"
    @classmethod
    def driver(cls, version, device):
        # Configura las opciones en lugar de `desired_capabilities`
        desired_capabilities = {
            "platformName": "Android",
            "platformVersion": version,  # versión de Android de tu dispositivo
            "deviceName": device,  # nombre o ID de tu dispositivo
            "appPackage": "com.instagram.android",
            "appActivity": ".activity.MainTabActivity",
            "automationName": "UiAutomator2",
            "newCommandTimeout": 3600
        }

        # Inicializa el controlador de Appium
        driver = webdriver.Remote("http://127.0.0.1:4723", desired_capabilities)
        print("Driver iniciado con éxito.")
        return driver
    
    @classmethod
    def sign_in(cls, driver:webdriver.Remote, email, password):
        print("[+] Starting process signIn")
        status = False
        block = False
        try:
            wait = WebDriverWait(driver, 20)
            # Espera a que el campo de búsqueda esté presente
            search_field = driver.find_element("xpath", '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup')
            search_field.click()
            time.sleep(2)
            search_field = driver.find_element("xpath", '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText')
            search_field.send_keys(email)
            time.sleep(2)
            search_field = driver.find_element("xpath", '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup')
            search_field.click()
            time.sleep(2)
            search_field = driver.find_element("xpath", '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.EditText')
            search_field.send_keys(password)
            time.sleep(2)
            search_field = driver.find_element("xpath", '//android.widget.Button[@content-desc="Iniciar sesión"]')
            search_field.click()
            cls._ahora_no(wait)
            status = True
        except Exception as e:
            print(f"Error al iniciar el driver o interactuar con la app: {e}")

        print("[+] Finish process signIn")
        return status, block
    
    @classmethod
    def sign_up(cls, driver: webdriver.Remote, email, password, name, api_url):
        print("[+] Starting process signUp")
        status = False
        block = False
        try:
            # Espera hasta que aparezca el DatePicker
            wait = WebDriverWait(driver, 20)
            # Espera a que el botón "Crear cuenta nueva" esté presente y haz clic
            search_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Crear cuenta nueva"]'))
            )
            search_field.click()
            print("[+] Click button crear cuenta nueva success.")

            # Espera a que el botón "Registrarte con tu correo electrónico" esté presente y haz clic
            search_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Registrarte con tu correo electrónico"]'))
            )
            search_field.click()
            print("[+] Click button Registrate con tu correo electronico success.")

            # Espera al campo de correo y envía la información
            search_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText'))
            )
            search_field.clear()
            search_field.send_keys(email)
            print("[+] Send email with input success")

            # Espera al botón "Siguiente" y haz clic
            cls._button_next(wait)
            print("[+] Click button siguiente success")

            # Espera al campo de código y luego ingresa el código
            input_code = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.view.View[@content-desc="Código de confirmación"]'))
            )
            input_code = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup'))
            )
            input_code.click()
            print("[+] click input code verification success")

            # Reintenta cada 5 segundos hasta obtener el código de confirmación
            while True:
                resp = cls.api_check_code(email, api_url)
                if resp["code_email"]:
                    if len(resp["code_email"]) == 6:
                        input_code = wait.until(
                            EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText'))
                        )
                        print(f"Confirmation code: {resp['code_email']}")
                        input_code.send_keys(resp['code_email'])
                        break
                time.sleep(5)

            print("[+] code confirmation success")

            # Espera al botón "Siguiente" y haz clic
            cls._button_next(wait)
            print("[+] click button siguiente success")
            
            button_next = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.view.View[@content-desc="Contraseña"]'))
            )
            print("[+] input password visible.")
            # Espera al campo de contraseña y envía la información
            input_password = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText'))
            )
            input_password.send_keys(password)
            print("[+] send password with input success")

            # Haz clic en el botón "Siguiente"
            cls._button_next(wait)
            print("[+] click button siguiente success")

            try:
                button_crear = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@resource-id="android:id/button2"]'))
                )
                button_crear.click()
            except Exception as e:
                print("Error button crear alert.")
            # Haz clic en el botón "Ahora no"
            cls._ahora_no(wait)
            print("[+] click button ahora no success")

            date_picker = wait.until(EC.presence_of_element_located((MobileBy.ID, "android:id/datePicker")))

            cls.mover_number_picker(
                driver=driver, 
                day=random.randint(1,28), 
                month=random.choice(["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "nov", "dic"]), 
                year=random.randint(1990, 2003)
            )

            # Guardar la selección
            guardar_btn = driver.find_element(MobileBy.ID, "android:id/button1")
            guardar_btn.click()

            # Haz clic en el botón "Siguiente"
            cls._button_next(wait)
            print("[+] configure datepicker success")

            button_next = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.view.View[@content-desc="Nombre completo"]'))
            )
            print("[+] input password visible.")
            # Espera al campo de contraseña y envía la información
            input_name = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText'))
            )
            input_name.send_keys(name)

            cls._button_next(wait)
            time.sleep(4)
            cls._button_next(wait)

            button_next = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Acepto"]'))
            )
            button_next.click()

            button_omitir = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Omitir"]'))
            )
            button_omitir.click()

            button_siguiente = wait.until(
                EC.visibility_of_element_located((By.ID, 'com.instagram.android:id/button_text'))
            )
            button_siguiente.click()
            status = True

        except Exception as e:
            print(f"[-] Error al interactuar con la app: {e}")
        
        print("[+] Finish process register")
        return status, block

    @classmethod
    def _button_next(cls, wait):
        button_next = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Siguiente"]'))
        )
        button_next.click()
    
    @classmethod
    def _ahora_no(cls, wait):
        button = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Ahora no"]'))
        )
        button.click()

    @classmethod
    def mover_number_picker(cls, driver, day=None, month=None, year=None):
        # Crear un objeto de espera explícita para los NumberPickers
        wait = WebDriverWait(driver, 20)

        # Seleccionar el NumberPicker correspondiente según el tipo: día, mes o año
        day_picker = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[1]'))
        )
        month_picker = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[2]'))
        )
        year_picker = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.LinearLayout[@resource-id="android:id/pickers"]/android.widget.NumberPicker[3]'))
        )

        # Ajustar el día, mes y año si se pasan valores
        if day != None:
            print("[+] search day...")
            cls.adjust_picker(day_picker, day)
        if year != None:
            print("[+] search year...")
            cls.adjust_picker(year_picker, year)
        if month != None:
            cls.adjust_picker(month_picker, month, True)

        # Esperar un momento antes de finalizar
        time.sleep(1)
    
    # Función para ajustar el valor en el NumberPicker
    @classmethod
    def adjust_picker(cls, picker, target_value, m=False):
        months = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"]
        if not m:
            current_value = int(picker.find_element_by_class_name('android.widget.EditText').get_attribute('text'))
        else:
            current_value = picker.find_element_by_class_name('android.widget.EditText').get_attribute('text')
        target_text = target_value

        while current_value != target_value: # 1 != 2, 2000 != 2001, ene != feb
            print(f"[+] Current element: {current_value}, Target Element: {target_value}")
            if m:
                current_value = months.index(current_value) # feb -> 1
                target_value = months.index(target_value) # ene -> 0
            if current_value < target_value:
                buttons = picker.find_elements_by_class_name('android.widget.Button')
                buttons[1].click()
            else:
                buttons = picker.find_elements_by_class_name('android.widget.Button')
                buttons[0].click()
            time.sleep(0.08)  # Esperar un momento para que se actualice el valor
            if not m:
                current_value = int(picker.find_element_by_class_name('android.widget.EditText').get_attribute('text'))
            else:
                current_value = picker.find_element_by_class_name('android.widget.EditText').get_attribute('text')
                target_value = target_text

    @classmethod
    def send_dm(cls, driver:webdriver.Remote, follow, message):
        print("[+] Starting send dm")
        status = False
        block = False
        try:
            wait = WebDriverWait(driver, 20)
            button_inbox = wait.until(
                EC.visibility_of_element_located((By.ID, "com.instagram.android:id/action_bar_inbox_button"))
            )
            button_inbox.click()

            button_search = wait.until(
                EC.visibility_of_element_located((By.ID, "com.instagram.android:id/search_edit_text"))
            )
            button_search.click()

            search_field = wait.until(
                EC.visibility_of_element_located((By.ID, "com.instagram.android:id/search_bar_real_field"))
            )
            search_field.send_keys(follow)
            print("[+] Send follow with search success")

            try:
                button_search = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.ID, "com.instagram.android:id/meta_ai_share_button"))
                )
                button_search.click()
                print("[+] Click button search success")
            except Exception as e:
                print("[-] Error button search name")
            try:
                follow_container = wait.until(
                    EC.visibility_of_element_located((By.ID, 'com.instagram.android:id/row_inbox_container'))
                )
                print(follow_container)
            except Exception as e:
                print("[-] Container follow not fount")
                follow_container = None

            if follow_container:
                print("[+] Follow fount...")
                follow_container.click()
                try:
                    button_acept = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/bb_primary_action_container"))
                    )
                    button_acept.click()
                except Exception as e:
                    print("[-] Error button accept, not fount")
                
                try:
                    search_field = wait.until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/row_thread_composer_edittext"))
                    )
                    search_field.send_keys(message)

                    button_acept = wait.until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/row_thread_composer_send_button_background"))
                    )
                    button_acept.click()
                    status = True
                except Exception as e01:
                    print("[-] Error send dm, input not active.")
                try:
                    button_arrow = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/header_left_button"))
                    )
                    button_arrow.click()
                except Exception as e:
                    print("[-] Error button arrow, not fount")

                try:
                    button_arrow = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/action_bar_button_back"))
                    )
                    button_arrow.click()
                except Exception as e:
                    print("[-] Error button arrow, not fount")
                
            else:
                print("[-] Follow not fount...")
                try:
                    button_arrow = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/back_arrow"))
                    )
                    button_arrow.click()
                except Exception as e:
                    print("[-] Error button arrow, not fount")
                
                try:
                    button_arrow = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "com.instagram.android:id/action_bar_button_back"))
                    )
                    button_arrow.click()
                except Exception as e:
                    print("[-] Error button arrow, not fount")
            
            print("[+] Finish send dm")
        except Exception as e:
            print(f"[-] Error general: {e}")
        return status, block

    @classmethod
    def error(cls):
        #//android.widget.TextView[@text="Se ha producido un error."]
        pass

    @classmethod
    def close(cls, driver:webdriver.Remote):
        driver.quit()
        print("[+] Finish Driver success.")
    
    @classmethod
    def api_check_code(cls, email, api_url):
        response = requests.request("GET", api_url + f"/api/check/code/?email={email}")
        logging.info(f"Reponse api code: {response.text}")
        return json.loads(response.text)

if __name__ == "__main__":
    manage_app = ManageApp()
    _driver = manage_app.driver()
    time.sleep(10)
    #manage_app.sign_in(_driver)
    manage_app.sign_up(_driver, "valeriagarciahw3998@gmail.com", "colombia123*", "valeria garcia")
    print("Sleep 120 seconds")
    time.sleep(120)
    #manage_app.close(_driver)