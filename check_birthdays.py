import os
import requests
from datetime import date

# ============================================================
# 🎂 LISTA DE ANIVERSARIANTES
# Formato: ("Nome", mês, dia)
# ============================================================
ANIVERSARIANTES = [
    ("Maria Silva",    1, 15),
    ("João Santos",    3, 22),
    ("Ana Oliveira",   5, 10),
    ("Pedro Costa",    7,  4),
    ("Lucas Pereira",  9, 30),
    ("Carla Souza",   11, 18),
    # Adicione quantos quiser aqui...
]

# ============================================================
# CONFIGURAÇÃO DO WPPCONNECT
# Variáveis definidas como Secrets no GitHub
# ============================================================
SERVER_URL = os.environ["WPPCONNECT_URL"]      # Ex: http://163.176.211.25:21465
TOKEN      = os.environ["WPPCONNECT_TOKEN"]    # Token gerado
SESSION    = os.environ["WPPCONNECT_SESSION"]  # Ex: mySession
PHONE      = os.environ["WPPCONNECT_PHONE"]    # Ex: 5551999990000


def send_whatsapp(message: str) -> None:
    url = f"{SERVER_URL}/api/{SESSION}/send-message"
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    payload = {
        "phone":   PHONE,
        "isGroup": False,
        "message": message,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status: {resp.status_code}")
        print(resp.text)
    except Exception as e:
        print(f"Erro: {e}")


def main():
    hoje = date.today()
    aniversariantes_hoje = [
        nome
        for nome, mes, dia in ANIVERSARIANTES
        if mes == hoje.month and dia == hoje.day
    ]

    if not aniversariantes_hoje:
        print(f"Nenhum aniversariante hoje ({hoje.strftime('%d/%m')}).")
        return

    nomes = ", ".join(aniversariantes_hoje)

    if len(aniversariantes_hoje) == 1:
        msg = f"Hoje e aniversario de *{nomes}*! Nao esqueca de parabenizar!"
    else:
        msg = f"Hoje fazem aniversario: *{nomes}*! Nao esqueca de parabenizar!"

    print(f"Enviando: {msg}")
    send_whatsapp(msg)


if __name__ == "__main__":
    main()
