import os
import requests
from datetime import date

# ============================================================
# 🎂 LISTA DE ANIVERSARIANTES
# Formato: ("Nome", mês, dia)
# ============================================================
ANIVERSARIANTES = [
    ("Pastora",    1, 7),
    ("Bola de Neve CMQ",    2, 22),
    ("João Brunno",  2, 26),
    ("Vitomar",   3, 2),
    ("Mauricio",    3,  30),
    ("Jagner",  5, 3),
    ("Kellen",   5, 11),
    ("Haithana", 6, 19),
    ("Lucas", 6, 24),
    ("Laysla", 6, 30),
    ("Vladi", 7, 13),
    ("Rebeca", 7, 23),
    ("Pastor", 7, 30),
    ("Angelise", 11, 14),
    ("Vitória", 12, 14),
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
        msg = f"Nenhum aniversariante hoje ({hoje.strftime('%d/%m')}). 🎂"
        print(msg)
        send_whatsapp(msg)
        return

    nomes = ", ".join(aniversariantes_hoje)

    if len(aniversariantes_hoje) == 1:
        msg = f"Hoje é aniversário de *{nomes}*! Não esqueça de parabenizar! 🎂"
    else:
        msg = f"Hoje fazem aniversário: *{nomes}*! Não esqueça de parabenizar! 🎂"

    print(f"Enviando: {msg}")
    send_whatsapp(msg)


if __name__ == "__main__":
    main()
