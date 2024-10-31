from tkinter import *
from manage_gmail import *
from manage_yahoo import *
import threading
import requests
import json

class Windows:
    def __init__(self):
        self.window = None
        self.driver: webdriver.Chrome = None
        self.browser_gmail: BrowserGmail = BrowserGmail()
        self.browser_yahoo: BrowserYahoo = BrowserYahoo()
        self.email_provider = None
        self.proxy_password = None

    def create(self):
        # Crear la ventana principal
        self.window = Tk()
        self.window.title("Bot Gmail and Yahoo")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.email_provider = StringVar(value="gmail")  # Valor por defecto es Gmail
        self.proxy_password = BooleanVar(value=False)  # Valor por defecto es Gmail
        self.proxy_uso = BooleanVar(value=False)  # Valor por defecto es Gmail

        # Frame para agrupar la selección de Gmail o Yahoo
        email_frame = Frame(self.window)
        email_frame.pack(pady=10)

        # Etiqueta para las opciones de email
        label_email = Label(email_frame, text="Selecciona tu proveedor de correo:")
        label_email.pack()

        # Radio button para seleccionar Gmail
        gmail_radio = Radiobutton(email_frame, text="Gmail", variable=self.email_provider, value="gmail")
        gmail_radio.pack(side=LEFT, padx=5)

        # Radio button para seleccionar Yahoo
        yahoo_radio = Radiobutton(email_frame, text="Yahoo", variable=self.email_provider, value="yahoo")
        yahoo_radio.pack(side=LEFT, padx=5)


        # ------------------- Frame para agrupar la selección de uso de Proxy ------------------
        proxy_frame = Frame(self.window)
        proxy_frame.pack(pady=10)

        # Etiqueta para las opciones de uso de proxy 
        label_proxy = Label(proxy_frame, text="Quieres usar proxy?")
        label_proxy.pack()

        # Radio button para seleccionar Si
        proxy_si_radio = Radiobutton(proxy_frame, text="Si", variable=self.proxy_uso, value=True)
        proxy_si_radio.pack(side=LEFT, padx=5)

        # Radio button para seleccionar No
        proxy_no_radio = Radiobutton(proxy_frame, text="No", variable=self.proxy_uso, value=False)
        proxy_no_radio.pack(side=LEFT, padx=5)


        # --------------- Frame para agrupar la selección de Proxy password-------------------
        proxy_pass_frame = Frame(self.window)
        proxy_pass_frame.pack(pady=10)

        # Etiqueta para las opciones de proxy password
        label_proxy_pass = Label(proxy_pass_frame, text="Quieres usar la clave del proxy?")
        label_proxy_pass.pack()

        # Radio button para seleccionar Si
        proxy_pass_si_radio = Radiobutton(proxy_pass_frame, text="Si", variable=self.proxy_password, value=True)
        proxy_pass_si_radio.pack(side=LEFT, padx=5)

        # Radio button para seleccionar No
        proxy_pass_no_radio = Radiobutton(proxy_pass_frame, text="No", variable=self.proxy_password, value=False)
        proxy_pass_no_radio.pack(side=LEFT, padx=5)

        # -------------- Crear un Frame para alinear los botones de iniciar y cerrar navegador ------------------
        top_frame = Frame(self.window)
        top_frame.pack(pady=10)

        # Botón para iniciar el navegador
        init_button = Button(top_frame, text="Iniciar navegador", command=self.init_browser)
        init_button.pack(side=LEFT, padx=5)

        # Botón para cerrar el navegador
        close_button_browser = Button(top_frame, text="Cerrar navegador", command=self.close_browser)
        close_button_browser.pack(side=LEFT, padx=5)

        # Botón para cerrar la ventana
        close_button = Button(self.window, text="Cerrar", command=self.window.destroy)
        close_button.place(x=350, y=10)  # Posicionarlo en la parte superior derecha

        # Frame para agrupar la entrada del código y el botón de enviar
        api_frame = Frame(self.window)
        api_frame.pack(pady=10)

        label_proxy_url = Label(api_frame, text="ApiUrl")
        label_proxy_url.grid(row=0, column=0)

        # Entrada para el código
        self.entry_api = Entry(api_frame, width=50)
        self.entry_api.grid(row=0, column=1)

        # Frame para agrupar la entrada de teléfono y el botón de enviar
        phone_frame = Frame(self.window)
        phone_frame.pack(pady=10)

        label_proxy_cel = Label(phone_frame, text="Celular")
        label_proxy_cel.grid(row=0, column=0)

        # Entrada para el número de teléfono
        self.entry_phone = Entry(phone_frame, width=33)
        self.entry_phone.grid(row=0, column=1)

        # Botón para enviar el número de teléfono
        send_phone_button = Button(phone_frame, text="Send To Browser", command=self.send_phone)
        send_phone_button.grid(row=0, column=2)

        # Frame para agrupar la entrada del código y el botón de enviar
        code_frame = Frame(self.window)
        code_frame.pack(pady=10)

        label_proxy_code = Label(code_frame, text="Codigo Email")
        label_proxy_code.grid(row=0, column=0)

        # Entrada para el código
        self.entry_code = Entry(code_frame, width=38)
        self.entry_code.grid(row=0, column=1)

        # Botón para enviar el código
        send_code_button = Button(code_frame, text="Send", command=self.send_code)
        send_code_button.grid(row=0, column=2)

        # Frame para agrupar la entrada, de envio de codigo de red social.
        email_frame = Frame(self.window)
        email_frame.pack(pady=10)

        # Botón para enviar el código
        send_email_button = Button(email_frame, text="Guardar correo creado", command=self.send_email, width=48)
        send_email_button.pack(side=LEFT, padx=5)

        # Frame para agrupar la entrada, de envio de codigo de red social.
        red_social_code_frame = Frame(self.window)
        red_social_code_frame.pack(pady=10)

        label_proxy_code2 = Label(red_social_code_frame, text="Codigo Instagram")
        label_proxy_code2.grid(row=0, column=0)

        # Entrada para el código
        self.entry_code_red_social = Entry(red_social_code_frame, width=33)
        self.entry_code_red_social.grid(row=0, column=1)

        # Botón para enviar el código
        red_social_code_button = Button(red_social_code_frame, text="Send", command=self.send_code_red_social)
        red_social_code_button.grid(row=0, column=2)

        # Iniciar el bucle principal de eventos
        self.window.mainloop()

    def send_phone(self):
        # Obtener el valor del Entry y mostrarlo en la consola
        value = self.entry_phone.get()
        print(f"Valor ingresado: {value}")  # Aquí puedes agregar más lógica
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider}")
        if email_provider == "gmail":
            threading.Thread(target=self.browser_gmail.set_phone, args=(value,)).start()
        else:
            threading.Thread(target=self.browser_yahoo.set_phone, args=(value,)).start()

    def send_code(self):
        # Obtener el valor del Entry y mostrarlo en la consola
        value = self.entry_code.get()
        print(f"Valor ingresado: {value}")  # Aquí puedes agregar más lógica
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider}")
        if email_provider == "gmail":
            threading.Thread(target=self.browser_gmail.set_code, args=(value,)).start()
        else:
            threading.Thread(target=self.browser_yahoo.set_code, args=(value,)).start()

    def send_code_red_social(self):
        # Obtener el valor del Entry y mostrarlo en la consola
        value = self.entry_code_red_social.get()
        print(f"Valor ingresado: {value}")  # Aquí puedes agregar más lógica
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider}")
        api_url = self.entry_api.get()
        if api_url:
            if email_provider == "gmail":
                threading.Thread(target=send_code_api, args=(value, self.browser_gmail.email, api_url)).start()
            else:
                threading.Thread(target=send_code_api, args=(value, self.browser_yahoo.email, api_url)).start()
        else:
            # alert configure api url
            pass
    
    def send_email(self):
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider}")
        api_url = self.entry_api.get()
        if api_url:
            if email_provider == "gmail":
                threading.Thread(target=send_email, args=(self.browser_gmail.email, self.browser_gmail.password, api_url)).start()
            else:
                threading.Thread(target=send_email, args=(self.browser_yahoo.email, self.browser_yahoo.password, api_url)).start()
        else:
            # alert configure api url
            pass

    def init_browser(self):
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        proxy_uso = self.proxy_uso.get()  # Obtener el proveedor seleccionado
        if proxy_uso == False:
            self.proxy_password.set(False)
        proxy_password = self.proxy_password.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider} {proxy_password}")

        if email_provider == "gmail":
            threading.Thread(target=self.browser_gmail.create_browser_with_proxy, args=("148.251.5.30", str(random.randint(10000, 20000)), proxy_uso)).start()
            threading.Thread(target=self.browser_gmail.init_browser, args=("84937b4537718abef992__cr.co", "8a08d42ec6cb5139", proxy_password)).start()
        else:
            threading.Thread(target=self.browser_yahoo.create_browser_with_proxy, args=("148.251.5.30", str(random.randint(10000, 20000)), proxy_uso)).start()
            threading.Thread(target=self.browser_yahoo.init_browser, args=("84937b4537718abef992__cr.co", "8a08d42ec6cb5139", proxy_password)).start()

    def close_browser(self):
        email_provider = self.email_provider.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {email_provider}")
        if email_provider == "gmail":
            threading.Thread(target=self.browser_gmail.close).start()
        else:
            threading.Thread(target=self.browser_yahoo.close).start()


def send_code_api(code, email, api_url):
    url = api_url+"/api/check/code/"
    payload = {'code': code, "email": email}
    files=[]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    return json.loads(response.text)

def send_email(email, password, api_url):
    url = api_url+"/api/create/email/"
    payload = {'email': email, "password": password}
    files=[]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    return json.loads(response.text)

if __name__ == "__main__":
    windows = Windows()
    windows.create()
