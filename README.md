# System Info Telegram Bot

Este projeto consiste em um script Python que coleta informações básicas de um sistema Linux (como Hostname, Uptime e Endereço IP) e as envia para um chat específico no Telegram.

## Funcionalidades

- Coleta o **Hostname** da máquina.
- Verifica o **Uptime** (há quanto tempo a máquina está ligada).
- Obtém o **Endereço IP** local.
- Lê o conteúdo de um arquivo de texto estático (`info.txt`) e o anexa à mensagem.
- Envia todas essas informações formatadas para um chat do Telegram através de um bot.

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
   - Abra o arquivo `config.py` e insira o seu `TELEGRAM_BOT_TOKEN` e o `TELEGRAM_CHAT_ID`.

4. **Personalize a mensagem estática:**
   - Edite o arquivo `info.txt` com a mensagem adicional que você deseja enviar.

## Como Usar

Para executar o script, basta rodar o seguinte comando no terminal:

```bash
python main.py
```

O script será executado, coletará as informações e as enviará para o chat configurado no Telegram.

## Estrutura do Projeto
```
.
├── .gitignore         # Ignora arquivos como config.py
├── config.py  # Arquivo de exemplo para configuração
├── info.txt           # Arquivo com texto estático
├── main.py            # Script principal
├── README.md          # Este arquivo
└── requirements.txt   # Dependências do projeto
```
