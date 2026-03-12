import os
import subprocess
import requests
import socket
import time
from logger import log_event 

try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
except ImportError:
    # Não há chat_id para logar aqui, então apenas imprimimos e saímos
    print("!!! ERRO !!!")
    print("O arquivo 'config.py' não foi encontrado.")
    exit()


# --- Arquivo estático ---
STATIC_FILE_PATH = "info.txt"

def get_machine_info():
    """Coleta as informações da máquina."""
    try:
        hostname = subprocess.check_output("hostname", shell=True).decode("utf-8").strip()
    except Exception as e:
        hostname = f"Erro ao obter o hostname: {e}"

    try:
        uptime = subprocess.check_output("uptime -p", shell=True).decode("utf-8").strip()
    except Exception as e:
        uptime = f"Erro ao obter o uptime: {e}"

    try:
        # Tenta obter o IP via socket, que é mais confiável para IPv4
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Conecta a um IP externo para descobrir o IP de saída local
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception:
        # Fallback: se o método do socket falhar, usa o comando 'hostname -I'
        try:
            all_ips = subprocess.check_output("hostname -I", shell=True).decode("utf-8").strip().split()
            # Procura pelo primeiro IP que seja IPv4 e não seja loopback
            ip_address = next(ip for ip in all_ips if '.' in ip and not ip.startswith('127.'))
        except (StopIteration, Exception) as e:
            ip_address = f"Não foi possível obter o endereço IP: {e}"

    return hostname, uptime, ip_address

def read_static_file(filepath):
    """Lê o conteúdo do arquivo estático."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return f"Erro: O arquivo '{filepath}' não foi encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo '{filepath}': {e}"

def send_telegram_message(message):
    """Envia uma mensagem para o Telegram e loga o resultado."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Gera uma exceção para respostas de erro (4xx ou 5xx)
        log_event(TELEGRAM_CHAT_ID, 'SUCCESS')
        print("Mensagem enviada com sucesso e log gerado.")
    except requests.exceptions.RequestException as e:
        log_event(TELEGRAM_CHAT_ID, 'FAILURE', error_message=str(e))
        print(f"Erro ao enviar a mensagem. O erro foi logado.")

if __name__ == "__main__":
    # Aguarda 30 segundos. Útil para dar tempo à inicialização da rede.
    time.sleep(30)

    # Verifica se as credenciais do Telegram foram alteradas
    if "SEU_TELEGRAM_BOT_TOKEN" in TELEGRAM_BOT_TOKEN or "SEU_TELEGRAM_CHAT_ID" in TELEGRAM_CHAT_ID:
        print("!!! AVISO !!!")
        print("Por favor, edite o arquivo 'config.py' e adicione suas credenciais do Telegram.")
        exit()

    # Coleta as informações
    hostname, uptime, ip_address = get_machine_info()
    static_content = read_static_file(STATIC_FILE_PATH)

    # Monta a mensagem em formato Markdown
    message = (
        f"*--- Informações da Máquina ---*\n"
        f"*Hostname:* `{hostname}`\n"
        f"*Uptime:* `{uptime}`\n"
        f"*Endereço IP:* `{ip_address}`\n\n"
        f"*--- Informações Adicionais ---*\n"
        f"{static_content}"
    )

    send_telegram_message(message)
