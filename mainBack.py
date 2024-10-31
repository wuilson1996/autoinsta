# websockets
import asyncio
from asgiref.sync import sync_to_async
import websockets
import time
from time import sleep
import argparse
from manage_app import *
from singleton import singleton

@singleton
class Machine:
    def __init__(self, version, device):
        self._manage:ManageApp = ManageApp()
        self._driver = self._manage.driver(version, device)

    @property
    def driver(self):
        return self._driver

    @property
    def manage(self):
        return self._manage

def sign_up_with_app(data, api_url):
    status, block = Machine()._manage.sign_up(Machine().driver, data["email"], data["password"], data["username"], api_url)
    if status:
        logging.info("[+] SignUp success...")
    if block:
        logging.info("[+] Account block...")
    return status, block

def sign_in_with_app(data):
    try:
        status, block = Machine()._manage.sign_in(Machine().driver, data["email"], data["password"])
        if status:
            logging.info("[+] SignIn success...")
    except Exception as e:
        logging.info(f"[+] Error signin, {e}...")
    return status, block

def logout_with_browse():
    status, block = Machine()._manage.close(Machine().driver)
    logging.info("[+] LogOut success...")
    return status, block

def send_dm_with_app(data):
    status, block = Machine()._manage.send_dm(
        Machine().driver,
        data["follow"],
        data["text"]
    )
    if block:
        logging.info("[+] Send DM success...")
    return status, block

def task_in_async(data, api_url) -> bool:
    if data["object"] == "CreateAccount":
        status, block = sign_up_with_app(data, api_url)
    elif data["object"] == "SignIn":
        status, block = sign_in_with_app(data)
    elif data["object"] == "LogOut":
        status, block = logout_with_browse()
    elif data["object"] == "SendDm":
        status, block = send_dm_with_app(data)
    return status, block

@sync_to_async
def task_account_current(data, api_url):
    try:
        status, block = task_in_async(data, api_url)
        aux_data = data
        aux_data["status"] = status
        aux_data["block"] = block
        aux_data["machine"] = "BotMaster"
        return aux_data
    except Exception as e:
        print("Error: "+str(e))

async def create_task_with_browser(version, device):
    Machine(version, device)
    logging.info("[+] Starting instance...")

async def received(machine, _url, version, device):
    asyncio.create_task(create_task_with_browser(version, device))
    url = f"wss://{_url}/ws/sync/fda7166a4c4766a77327769624b9416035762dd3/{machine}"
    while True:
        try:
            async with websockets.connect(url) as websocket:
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

                        aux_data = await task_account_current(data, "https://"+_url)
                        await websocket.send(json.dumps(aux_data))
                            
                    except Exception as e:
                        logging.info(f"Error al recibir o procesar datos: " + str(e))
                        break
        except Exception as errorConnect:
            logging.info(f"[-] Error to connect: "+str(errorConnect))
            logging.info(f"[+] Reconected websocket in 5 seconds...")
            await asyncio.sleep(5)
        except KeyboardInterrupt:
            logging.info(f"[+] Interrumpido por el usuario, saliendo...")
            break
    
    logging.info(f"[+] Disconnection to Server success! MachineName: {machine}")

def execute_system(machine, url, email):
    asyncio.run(received(machine, url, email))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Autobot Instagram App')
    parser.add_argument('url', type=str, help='url Server')
    parser.add_argument('machine', type=str, help='nombre de BotNet')
    parser.add_argument('version', type=str, help='Version de android BotNet')
    parser.add_argument('device', type=str, help='serial de android BotNet')
    args = parser.parse_args()
    asyncio.run(received(args.machine, args.url, args.version, args.device))