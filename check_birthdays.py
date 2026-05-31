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
GROUP      = os.environ["WPPCONNECT_GROUP"]


def send_whatsapp(message: str, phone: str) -> None:
    url = f"{SERVER_URL}/api/{SESSION}/send-message"
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }
    payload = {
        "phone":   phone,
        "isGroup": "@g.us" in phone,
        "message": message,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Status {phone}: {resp.status_code}")
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
        msg_pessoal = f"Nenhum aniversariante hoje ({hoje.strftime('%d/%m')}). 🎂"
        msg_grupo   = "📅 *Oi, líderes!*\n\nNenhum aniversariante hoje. Que seja um ótimo dia! ☀️"
    elif len(aniversariantes_hoje) == 1:
        nome = aniversariantes_hoje[0]
        msg_pessoal = f"Hoje é aniversário de *{nome}*! 🎂"
        msg_grupo   = f"🎂 *Oi, líderes!*\n\nHoje é aniversário de *{nome}*! Não esqueçam de parabenizá-lo(a) e fazer ele(a) se sentir especial! 🎉"
    else:
        nomes = ", ".join(aniversariantes_hoje[:-1]) + f" e {aniversariantes_hoje[-1]}"
        msg_pessoal = f"Hoje fazem aniversário: *{nomes}*! 🎂"
        msg_grupo   = f"🎂 *Oi, líderes!*\n\nHoje fazem aniversário: *{nomes}*! Não esqueçam de parabenizá-los e fazer eles se sentirem especiais! 🎉"

    print(f"Enviando: {msg_grupo}")
    send_whatsapp(msg_pessoal, PHONE)
    send_whatsapp(msg_grupo, GROUP)


if __name__ == "__main__":
    main()
