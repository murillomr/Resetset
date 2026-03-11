import datetime
import socket

# Define o nome do arquivo de log
LOG_FILE = 'events.log'

def log_event(chat_id, status, error_message=''):
    """
    Gera e salva uma linha de log em formato CEF.

    Args:
        chat_id (str): O ID do chat do Telegram.
        status (str): 'SUCCESS' ou 'FAILURE'.
        error_message (str, optional): A mensagem de erro, se houver.
    """
    try:
        # Horário atual e hostname
        timestamp = datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')
        hostname = socket.gethostname()

        # Componentes do cabeçalho CEF
        device_vendor = 'Custom'
        device_product = 'TelegramBot'
        device_version = '1.0'
        signature_id = 'TELEGRAM_SEND'
        name = 'Telegram message send attempt'
        severity = '0' if status == 'SUCCESS' else '5'  # 0 para sucesso, 5 para alerta/falha

        # Extensões CEF (detalhes do evento)
        extensions = f'outcome={status} destinationUserID={chat_id}'
        if error_message:
            # Escapa caracteres especiais para não quebrar o formato
            clean_message = error_message.replace('', '').replace('=', '\=')
            extensions += f' msg={clean_message}'

        # Monta a mensagem final no padrão: "Timestamp Hostname CEF:..."
        log_line = (
            f'{timestamp} {hostname} CEF:0|{device_vendor}|{device_product}|'
            f'{device_version}|{signature_id}|{name}|{severity}|{extensions}\n'
        )

        # Escreve no arquivo de log
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)

    except Exception as e:
        # Se o logging falhar, imprime um erro no console para diagnóstico
        print(f"CRITICAL: Failed to write to log file '{LOG_FILE}'. Error: {e}")
