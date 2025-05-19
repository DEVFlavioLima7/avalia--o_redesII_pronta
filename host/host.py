import time
import os
import subprocess
import sys

def ping(destination):
    print(f"Tentando pingar {destination}...")
    response = os.system(f"ping -c 1 {destination}")
    if response == 0:
        print(f"Ping para {destination} bem-sucedido!")
    else:
        print(f"Falha no ping para {destination}.")

if __name__ == "__main__":
    destination = os.getenv("DESTINATION")
    connection_router = os.getenv("CONNECTION_ROUTER")
    
    try:
        subprocess.run(["ip", "route", "del", "default"], check=True)
        print(f"Rota default adicionada via {connection_router}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao remover rota default: {e}")
        sys.exit(1)
    
    try:
        subprocess.run(["ip", "route", "add", "default", "via", connection_router, "dev", "eth0"], check=True)
        print(f"Rota default adicionada via {connection_router}.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao adicionar rota default: {e}")
        sys.exit(1)
    
    while True:
        ping(destination)
        time.sleep(20)

