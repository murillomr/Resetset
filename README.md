# System Info Telegram Bot

Este projeto consiste em um script Python que coleta informações básicas de um sistema Linux (como Hostname, Uptime e Endereço IP) e as envia para um chat específico no Telegram.

## Funcionalidades

- Coleta o **Hostname** da máquina.
- Verifica o **Uptime** (há quanto tempo a máquina está ligada).
- Obtém o **Endereço IP** local.
- Lê o conteúdo de um arquivo de texto estático (`info.txt`) e o anexa à mensagem.
- Envia todas essas informações formatadas para um chat do Telegram através de um bot.
- **Gera um log local (`events.log`) em formato CEF para cada tentativa de envio, registrando sucesso ou falha.**

## Pré-requisitos

- Python 3.6+
- Um bot do Telegram e seu respectivo **token de API**.
- O **Chat ID** da conversa para onde a mensagem será enviada.

## Instalação e Configuração

1. **Clone este repositório (ou baixe os arquivos):**
   ```bash
   # git clone <url-do-repositorio>
   # cd <nome-do-repositorio>
   ```

2. **Instale as dependências:**
   Crie um ambiente virtual (recomendado) e instale as dependências do `requirements.txt`.
   ```bash
   python -m venv venv
   source venv/bin/activate 
   pip install -r requirements.txt
   ```

3. **Configure as credenciais:**
   - Crie o arquivo `config.py` (a partir do `config.py.example` se disponível) e insira o seu `TELEGRAM_BOT_TOKEN` e o `TELEGRAM_CHAT_ID`.

4. **Personalize a mensagem estática:**
   - Edite o arquivo `info.txt` com a mensagem adicional que você deseja enviar.

## Como Usar

Para executar o script, basta rodar o seguinte comando no terminal:

```bash
python main.py
```

O script será executado, coletará as informações, as enviará para o chat configurado no Telegram e registrará a operação em `events.log`.

## Logs

A cada execução, o script gera uma linha de log no arquivo `events.log`. O formato utilizado é o **Common Event Format (CEF)**, que é um padrão aberto para interoperabilidade de logs.

- **Exemplo de log (sucesso):**
  ```
  Mar 10 2026 12:30:00 meu-host CEF:0|Custom|TelegramBot|1.0|TELEGRAM_SEND|Telegram message send attempt|0|outcome=SUCCESS destinationUserID=123456789
  ```
- **Exemplo de log (falha):**
  ```
  Mar 10 2026 12:31:00 meu-host CEF:0|Custom|TelegramBot|1.0|TELEGRAM_SEND|Telegram message send attempt|5|outcome=FAILURE destinationUserID=123456789 msg=HTTPError: 400 Client Error: Bad Request for url: ...
  ```

## Estrutura do Projeto
```
.
├── .gitignore         # Ignora arquivos como config.py e *.log
├── config.py          # Arquivo para configuração das credenciais
├── info.txt           # Arquivo com texto estático
├── logger.py          # Módulo responsável por gerar os logs em CEF
├── main.py            # Script principal
├── README.md          # Este arquivo
└── requirements.txt   # Dependências do projeto
```
