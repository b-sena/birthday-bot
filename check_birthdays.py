import os
import csv
import requests
from datetime import datetime, timezone, timedelta
from io import StringIO

# ============================================================
# CONFIGURAÇÃO
# ============================================================
SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTrF-9UTvX92qw-7Jj7xpebBO58Hk7W9YZN3kcg3vpXR02-cYk4BAky0LBODHtHK4WpujtPsEf7h-Zq/pub?gid=0&single=true&output=csv"

EVOLUTION_URL      = os.environ["EVOLUTION_URL"]
EVOLUTION_APIKEY   = os.environ["EVOLUTION_APIKEY"]
EVOLUTION_INSTANCE = os.environ["EVOLUTION_INSTANCE"]
PHONE              = os.environ["EVOLUTION_PHONE"]
AVISOS             = os.environ["EVOLUTION_AVISOS"]
# GROUP              = os.environ["EVOLUTION_GROUP"]


# ============================================================
# LER ANIVERSARIANTES DO GOOGLE SHEETS
# Colunas: Nome | Dia | Mês | Célula
# ============================================================
def carregar_aniversariantes():
    resp = requests.get(SHEETS_URL, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    reader = csv.DictReader(StringIO(resp.text))
    aniversariantes = []
    for row in reader:
        try:
            nome   = row["Nome"].strip()
            dia    = int(row["Dia"].strip())
            mes    = int(row["Mês"].strip())
            celula = row["Célula"].strip()
            if nome:
                aniversariantes.append((nome, dia, mes, celula))
        except (ValueError, KeyError):
            continue
    return aniversariantes


# ============================================================
# ENVIAR PELO WHATSAPP
# ============================================================
def send_whatsapp(message: str, number: str) -> None:
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_APIKEY,
    }
    payload = {
        "number": number,
        "text": message,
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        print(f"Enviado para {number}: {resp.status_code}")
    except Exception as e:
        print(f"Erro ao enviar para {number}: {e}")


# ============================================================
# MAIN
# ============================================================
def main():
    BRT = timezone(timedelta(hours=-3))
    hoje = datetime.now(BRT).date()

    print(f"Verificando aniversariantes para {hoje.strftime('%d/%m/%Y')}...")

    aniversariantes = carregar_aniversariantes()
    print(f"{len(aniversariantes)} aniversariantes carregados da planilha.")

    aniversariantes_hoje = [
        (nome, celula)
        for nome, dia, mes, celula in aniversariantes
        if dia == hoje.day and mes == hoje.month
    ]

    if not aniversariantes_hoje:
        msg_pessoal = f"Nenhum aniversariante hoje ({hoje.strftime('%d/%m')}). 🎂"
        msg_avisos  = "📅 *Bom dia, família!*\n\nNenhum aniversariante hoje. Que seja um ótimo dia! ☀️"
    elif len(aniversariantes_hoje) == 1:
        nome, celula = aniversariantes_hoje[0]
        celula_txt   = f" _(Célula {celula})_" if celula and celula != "-" else ""
        msg_pessoal  = f"Hoje é aniversário de *{nome}*{celula_txt}! 🎂"
        msg_avisos   = (
            f"🎂 Hoje é aniversário de *{nome}*{celula_txt}!\n\n"
            f"Não esqueça de enviar uma mensagem parabenizando 🎉🙏"
        )
    else:
        linhas = "\n".join(
            f"• *{nome}*" + (f" _(Célula {celula})_" if celula and celula != "-" else "")
            for nome, celula in aniversariantes_hoje
        )
        msg_pessoal = f"Hoje fazem aniversário:\n{linhas} 🎂"
        msg_avisos  = (
            f"Hoje é dia especial para:\n{linhas}\n\n"
            f"Não esqueça de enviar uma mensagem parabenizando 🎉🙏"
        )

    print(f"Enviando mensagens...")
    send_whatsapp(msg_pessoal, PHONE)
    send_whatsapp(msg_avisos, AVISOS)


if __name__ == "__main__":
    main()