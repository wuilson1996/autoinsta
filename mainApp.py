from tkinter import *
import threading
import argparse
import subprocess
import sys
from time import sleep
from manage_app import ManageApp
import random

class Windows:
    def __init__(self):
        self.window = None
        self.type_bot = None
        self.manage_app = {}

    def create(self):
        # Crear la ventana principal
        self.window = Tk()
        self.window.title("Create bots")
        self.window.geometry("420x420")
        self.type_bot = BooleanVar(value=True)  # colección o un bot por número.

        # Frame para agrupar la selección de Gmail o Yahoo
        email_frame = Frame(self.window)
        email_frame.pack(pady=10)

        # ------------------- Frame para agrupar la selección de uso de Proxy ------------------
        # proxy_frame = Frame(self.window)
        # proxy_frame.pack(pady=10)

        # # Etiqueta para las opciones de uso de proxy
        # label_bot = Label(proxy_frame, text="Tipo de bots")
        # label_bot.pack()

        # # Radio button para seleccionar Colección de bots
        # bot_si_radio = Radiobutton(proxy_frame, text="Colección de bots", variable=self.type_bot, value=True)
        # bot_si_radio.pack(side=LEFT, padx=5)

        # # Radio button para seleccionar Un bot
        # bot_no_radio = Radiobutton(proxy_frame, text="Un bot", variable=self.type_bot, value=False)
        # bot_no_radio.pack(side=LEFT, padx=5)

        # -------------- Crear un Frame para alinear los botones de iniciar y cerrar navegador ------------------
        top_frame = Frame(self.window)
        top_frame.pack(pady=10)

        # Botón para cerrar la ventana
        close_button = Button(self.window, text="Cerrar", command=self.window.destroy)
        close_button.place(x=350, y=10)  # Posicionarlo en la parte superior derecha

        # Frame para agrupar la entrada de teléfono y el botón de enviar
        phone_frame = Frame(self.window)
        phone_frame.pack(pady=10)

        # Etiqueta para las opciones de uso de proxy
        label_dm = Label(phone_frame, text="Enviar dm en app")
        label_dm.grid(row=0, column=0, columnspan=2, pady=(0, 5))

        # Entrada para la URL API (columna izquierda)
        label_version = Label(phone_frame, text="Android version")
        label_version.grid(row=1, column=0, padx=5, sticky="e")
        self.entry_version = Entry(phone_frame, width=40)
        self.entry_version.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Entrada para la cantidad o número (columna derecha)
        label_serial = Label(phone_frame, text="Serial device")
        label_serial.grid(row=2, column=0, padx=5, sticky="e")
        self.entry_serial = Entry(phone_frame, width=40)
        self.entry_serial.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Botón para enviar el número de teléfono
        send_bot_button = Button(phone_frame, text="Conectar", command=self.run_driver, width=20)
        send_bot_button.grid(row=3, column=0, columnspan=2, pady=5)
        # Entrada para la cantidad o número (columna derecha)
        label_message = Label(phone_frame, text="Message")
        label_message.grid(row=4, column=0, padx=5, sticky="e")
        self.entry_message = Entry(phone_frame, width=40)
        self.entry_message.grid(row=4, column=1, padx=5, pady=2, sticky="w")
        # Entrada para la URL API (columna izquierda)
        label_follow = Label(phone_frame, text="Follow")
        label_follow.grid(row=5, column=0, padx=5, sticky="e")
        self.entry_follow = Entry(phone_frame, width=40)
        self.entry_follow.grid(row=5, column=1, padx=5, pady=2, sticky="w")

        # Botón para enviar el número de teléfono
        send_bot_button = Button(phone_frame, text="Enviar Dm", command=self.send_dm,  width=20)
        send_bot_button.grid(row=6, column=0, columnspan=2, pady=5)

        label_email = Label(phone_frame, text="Email")
        label_email.grid(row=7, column=0, padx=5, sticky="e")
        self.entry_email = Entry(phone_frame, width=40)
        self.entry_email.grid(row=7, column=1, padx=5, pady=2, sticky="w")
        # Entrada para la URL API (columna izquierda)
        label_password = Label(phone_frame, text="Password")
        label_password.grid(row=8, column=0, padx=5, sticky="e")
        self.entry_password = Entry(phone_frame, width=40)
        self.entry_password.grid(row=8, column=1, padx=5, pady=2, sticky="w")

        # Botón para enviar el número de teléfono
        send_bot_button = Button(phone_frame, text="Registrar", command=self.sign_up,  width=20)
        send_bot_button.grid(row=9, column=0, columnspan=2, pady=5)
        # Botón para enviar el número de teléfono
        send_bot_button = Button(phone_frame, text="Iniciar sesion", command=self.sign_in,  width=20)
        send_bot_button.grid(row=10, column=0, columnspan=2, pady=5)
        send_bot_button = Button(phone_frame, text="Cerrar conexion", command=self.quit_driver,  width=20)
        send_bot_button.grid(row=11, column=0, columnspan=2, pady=5)

        # Iniciar el bucle principal de eventos
        self.window.mainloop()

    def run_driver(self):
        version = self.entry_version.get()
        serial = self.entry_serial.get()
        #if serial not in list(self.manage_app.keys()):
        _manage = ManageApp()
        self.manage_app[serial] = {
            "device": _manage,
            "driver":_manage.driver(version, serial)
        }
        #else:
        #    print("[+] Dispositivo ya esta instanciado.")
    
    def quit_driver(self):
        serial = self.entry_serial.get()
        self.manage_app[serial]["device"].close(self.manage_app[serial]["driver"])
    
    def sign_up(self):
        serial = self.entry_serial.get()

        email = self.entry_email.get()
        password = self.entry_password.get()
        name = email.split("@")[0]
        threading.Thread(target=self.manage_app[serial]["device"].sign_up, args=(self.manage_app[serial]["driver"], email, password, name)).start()
    
    def sign_in(self):
        serial = self.entry_serial.get()

        email = self.entry_email.get()
        password = self.entry_password.get()
        threading.Thread(target=self.manage_app[serial]["device"].sign_in, args=(self.manage_app[serial]["driver"], email, password)).start()

    def send_dm(self):
        serial = self.entry_serial.get()

        # Obtener el valor del Entry y mostrarlo en la consola
        follow = self.entry_follow.get()
        message = self.entry_message.get()
        print(f"Follow ingresado: {follow}")  # Aquí puedes agregar más lógica
        threading.Thread(target=self.manage_app[serial]["device"].send_dm, args=(self.manage_app[serial]["driver"], follow, message)).start()

if __name__ == "__main__":
    windows = Windows()
    windows.create()