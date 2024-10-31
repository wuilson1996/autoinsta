from tkinter import *
import threading
import argparse
import subprocess
import sys
from time import sleep

def launch_bots(script_name, url, hilos, botNum):
    # Ejecuta el script con la cantidad de hilos especificada, cada uno en una nueva ventana
    if hilos > 0:
        for i in range(1, int(hilos) + 1):
            print(f"[+] Ejecutando BotNet{i}")
            # En Windows usamos 'start', en Mac 'open' y en Linux 'gnome-terminal' (puede variar según el terminal que uses)
            if sys.platform == "win32":
                subprocess.Popen(['start', 'python', script_name, url, str(i)], shell=True)
            elif sys.platform == "darwin":  # macOS
                subprocess.Popen(['open', '-a', 'Terminal', 'python', script_name, url, str(i)])
            else:  # Linux
                subprocess.Popen(['gnome-terminal', '--', 'python3', script_name, url, str(i)])
            sleep(8)
    else:
        print(f"[+] Ejecutando BotNet{botNum}")
        # En Windows usamos 'start', en Mac 'open' y en Linux 'gnome-terminal' (puede variar según el terminal que uses)
        if sys.platform == "win32":
            subprocess.Popen(['start', 'python', script_name, url, str(botNum)], shell=True)
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(['open', '-a', 'Terminal', 'python', script_name, url, str(botNum)])
        else:  # Linux
            subprocess.Popen(['gnome-terminal', '--', 'python3', script_name, url, str(botNum)])

class Windows:
    def __init__(self):
        self.window = None
        self.type_bot = None

    def create(self):
        # Crear la ventana principal
        self.window = Tk()
        self.window.title("Create bots")
        self.window.geometry("400x250")
        self.type_bot = BooleanVar(value=True)  # colección o un bot por número.

        # Frame para agrupar la selección de Gmail o Yahoo
        email_frame = Frame(self.window)
        email_frame.pack(pady=10)

        # ------------------- Frame para agrupar la selección de uso de Proxy ------------------
        proxy_frame = Frame(self.window)
        proxy_frame.pack(pady=10)

        # Etiqueta para las opciones de uso de proxy
        label_bot = Label(proxy_frame, text="Tipo de bots")
        label_bot.pack()

        # Radio button para seleccionar Colección de bots
        bot_si_radio = Radiobutton(proxy_frame, text="Colección de bots", variable=self.type_bot, value=True)
        bot_si_radio.pack(side=LEFT, padx=5)

        # Radio button para seleccionar Un bot
        bot_no_radio = Radiobutton(proxy_frame, text="Un bot", variable=self.type_bot, value=False)
        bot_no_radio.pack(side=LEFT, padx=5)

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
        label_cant = Label(phone_frame, text="Número de bot o la cantidad de bots.")
        label_cant.grid(row=0, column=0, columnspan=2, pady=(0, 5))

        # Entrada para la URL API (columna izquierda)
        label_url = Label(phone_frame, text="URL API")
        label_url.grid(row=1, column=0, padx=5, sticky="e")
        self.entry_url = Entry(phone_frame)
        self.entry_url.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Entrada para la cantidad o número (columna derecha)
        label_cant = Label(phone_frame, text="Cant. o Num.")
        label_cant.grid(row=2, column=0, padx=5, sticky="e")
        self.entry_cant = Entry(phone_frame)
        self.entry_cant.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        # Botón para enviar el número de teléfono
        send_bot_button = Button(phone_frame, text="Crear", command=self.send_create_bots)
        send_bot_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Iniciar el bucle principal de eventos
        self.window.mainloop()

    def send_create_bots(self):
        # Obtener el valor del Entry y mostrarlo en la consola
        value = self.entry_cant.get()
        url = self.entry_url.get()
        print(f"Valor ingresado: {value}")  # Aquí puedes agregar más lógica
        type_bot = self.type_bot.get()  # Obtener el proveedor seleccionado
        print(f"Proveedor de correo seleccionado: {type_bot}")
        if value:
            if type_bot:
                threading.Thread(target=launch_bots, args=("autobotV1.py", url, int(value), 0)).start()
            else:
                threading.Thread(target=launch_bots, args=("autobotV1.py", url, 0, int(value))).start()


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Autobot Instagram')
    # parser.add_argument('url', type=str, help='url botMaster')
    # parser.add_argument('hilos', type=int, help='hilos de BotNet')
    # parser.add_argument('botNum', type=int, help='Numero de BotNet')
    # args = parser.parse_args()

    # launch_bots("autobotV1.py", args.url, args.hilos, args.botNum)
    windows = Windows()
    windows.create()