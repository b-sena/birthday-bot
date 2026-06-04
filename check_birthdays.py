import os
import requests
from datetime import date

# ============================================================
# 🎂 LISTA DE ANIVERSARIANTES
# Formato: ("Nome", mês, dia)
# ============================================================
ANIVERSARIANTES = [
    ("Viviane",             1,  3),
    ("Pastora",             1,  7),
    ("Marina KIDS",         1,  7),
    ("Gabriel KIDS",        1,  16),
    ("Lorenzo TEENS",       1, 28),
    ("Dani FLAME",          2,  5),
    ("Lucas TEENS",         2, 12),
    ("Luciano",             2, 13),
    ("Bola de Neve CMQ",    2, 22),
    ("Richelle",            2, 26),
    ("João Brunno",         2, 26),
    ("Dc. Vitomar",         3,  2),
    ("Manuela KIDS",        3,  2),
    ("Presb. Mauricio",     3, 30),
    ("Dc. Léo",             4,  1),
    ("Thaís",               4,  2),
    ("Fabio Boeira",        4, 13),
    ("Ana Paula",           4, 18),
    ("Karine",              4, 22),
    ("Alexia TEENS",        4, 25),
    ("Lucas Figueiredo",    4, 25),
    ("José Gabriel KIDS",   5,  2),
    ("Ld. Jagner",          5,  3),
    ("Alice",               5,  4),
    ("Ld. Kellen",          5, 11),
    ("Bruna",               5, 14),
    ("Ielen TEENS",         5, 19),
    ("Serginho",            5, 21),
    ("Jackson",             5, 26),
    ("Bruna KIDS",          6,  4),
    ("Helena KIDS",         6, 13),
    ("Presb. Haithana",     6, 19),
    ("Ld. Lucas Varante",   6, 24),
    ("Ld. Laysla",          6, 30),
    ("Jaqueline",           6, 30),
    ("Deyvit",              7, 10),
    ("Ld. Vladi",           7, 13),
    ("Giovana TEENS",       7, 22),
    ("Rebeca KIDS",         7, 23),
    ("Pastor",              7, 29),
    ("Suzana",              7, 31),
    ("Joaquim KIDS",        8,  2),
    ("Sofia KIDS",          8,  2),
    ("Isa TEENS",           8,  4),
    ("José TEENS",          8,  6),
    ("Alice TEENS",         8, 26),
    ("Daniel",              9,  4),
    ("Andressa",            9, 13),
    ("Lucas Santos",        9, 18),
    ("Luana",              10,  5),
    ("Nei Borget",         10, 14),
    ("Kelly",              10, 30),
    ("Hope KIDS",          11, 10),
    ("Dc. Angelise",       11, 14),
    ("Davi TEENS",         11, 17),
    ("Enio",               11, 27),
    ("Bento KIDS",         12,  2),
    ("Amélia",             12, 13),
    ("Ld. Vitória",        12, 14),
    ("Júlio",              12, 23),
]

# ============================================================
# CONFIGURAÇÃO DO WPPCONNECT
# Variáveis definidas como Secrets no GitHub
# ============================================================
SERVER_URL = os.environ["EVOLUTION_URL"]      # http://163.176.211.25:8080
API_KEY    = os.environ["EVOLUTION_APIKEY"]   # birthday123bot
INSTANCE   = os.environ["EVOLUTION_INSTANCE"] # birthday-bot
PHONE      = os.environ["EVOLUTION_PHONE"]    # 5551997063185
GROUP      = os.environ["EVOLUTION_GROUP"]    # 120363040976590973@g.us


def send_whatsapp(message: str, number: str) -> None:
    url = f"{SERVER_URL}/message/sendText/{INSTANCE}"
    headers = {
        "Content-Type": "application/json",
        "apikey": API_KEY,
    }
    payload = {
        "number": number,
        "textMessage": {"text": message},
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Enviado para {number}: {resp.status_code}")
    except Exception as e:
        print(f"Erro ao enviar para {number}: {e}")


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