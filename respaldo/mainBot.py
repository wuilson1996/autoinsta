import argparse
import subprocess
import sys

def launch_bots(script_name, url, hilos):
    # Ejecuta el script con la cantidad de hilos especificada, cada uno en una nueva ventana
    for i in range(1, int(hilos) + 1):
        print(f"[+] Ejecutando BotNet{i}")
        # En Windows usamos 'start', en Mac 'open' y en Linux 'gnome-terminal' (puede variar según el terminal que uses)
        if sys.platform == "win32":
            subprocess.Popen(['start', 'python', script_name, url, str(i)], shell=True)
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(['open', '-a', 'Terminal', 'python', script_name, url, str(i)])
        else:  # Linux
            subprocess.Popen(['gnome-terminal', '--', 'python3', script_name, url, str(i)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Autobot Instagram')
    parser.add_argument('url', type=str, help='url botMaster')
    parser.add_argument('hilos', type=int, help='hilos de BotNet')
    args = parser.parse_args()

    launch_bots("autobotV1.py", args.url, args.hilos)