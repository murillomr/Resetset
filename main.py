import os
import subprocess
import requests

try:
    from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
except ImportError:
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
        # Pega o primeiro endereço IP da lista
        ip_address = subprocess.check_output("hostname -I", shell=True).decode("utf-8").strip().split()[0]
    except Exception as e:
        ip_address = f"Erro ao obter o endereço IP: {e}"

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
    """Envia uma mensagem para o Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Mensagem enviada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar a mensagem para o Telegram: {e}")

if __name__ == "__main__":
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
