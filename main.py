from tkinter import *
from manage_gmail import *
import threading

class Windows:
    def __init__(self):
        self.window = None
        self.driver:webdriver.Chrome = None
        self.browser:Browser = Browser()

    def create(self):
        # Crear la ventana principal
        self.window = Tk()
        self.window.title("Mi Ventana Tkinter")  # Título de la ventana
        self.window.geometry("400x300")  # Tamaño de la ventana (ancho x alto)

        # Agregar una etiqueta a la ventana
        label = Label(self.window, text="¡Bienvenido a la Aplicación Tkinter!")
        label.pack(pady=20)  # Agregar un poco de espacio vertical

        # Crear y agregar un widget Entry para la entrada del usuario
        self.entry = Entry(self.window)
        self.entry.pack(pady=10)  # Agregar un poco de espacio vertical

        # Agregar un botón para enviar el valor del Entry
        send_button = Button(self.window, text="Enviar", command=self.send_value)
        send_button.pack(pady=10)  # Agregar un poco de espacio vertical

        # Agregar un botón para enviar el valor del Entry
        send_button = Button(self.window, text="Iniciar navegador", command=self.init_browser)
        send_button.pack(pady=11)  # Agregar un poco de espacio vertical

        # Agregar un botón para enviar el valor del Entry
        send_button = Button(self.window, text="Cerrar navegador", command=self.close_blowser)
        send_button.pack(pady=12)  # Agregar un poco de espacio vertical

        # Agregar un botón para cerrar la ventana
        close_button = Button(self.window, text="Cerrar", command=self.window.destroy)
        close_button.pack(pady=10)  # Agregar un poco de espacio vertical

        # Iniciar el bucle principal de eventos
        self.window.mainloop()

    def send_value(self):
        # Obtener el valor del Entry y mostrarlo en la consola
        value = self.entry.get()
        print(f"Valor ingresado: {value}")  # Aquí puedes agregar más lógica
        threading.Thread(target=self.browser.set_phone, args=(value,)).start()

    def init_browser(self):
        threading.Thread(target=self.browser.create_browser_with_proxy, args=("144.76.124.83", str(random.randint(10000, 20000)))).start()
        threading.Thread(target=self.browser.init_browser).start()

    def close_blowser(self):
        self.browser.close()



if __name__ == "__main__":
    windows = Windows()
    windows.create()
