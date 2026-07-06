# 🎂 Birthday Bot — WhatsApp via Evolution API + GitHub Actions

Todo dia, o bot consulta uma planilha do Google Sheets e envia uma mensagem no WhatsApp (para um número pessoal e para um grupo) avisando quem faz aniversário.

---

## 📋 Como configurar

### 1. Preparar a planilha de aniversariantes

1. Crie uma planilha no Google Sheets com as colunas: **Nome**, **Dia**, **Mês**, **Célula**
2. Vá em **Arquivo → Compartilhar → Publicar na web**
3. Selecione a aba desejada e o formato **CSV**, e publique
4. Copie o link gerado e atualize a constante `SHEETS_URL` em [check_birthdays.py](check_birthdays.py)

### 2. Criar a instância na Evolution API

1. Suba/acesse sua instância da [Evolution API](https://github.com/EvolutionAPI/evolution-api)
2. Conecte o WhatsApp escaneando o QR Code
3. Anote a **URL base**, a **API Key** e o **nome da instância**

### 3. Adicionar os Secrets no GitHub

No seu repositório, vá em:
**Settings → Secrets and variables → Actions → New repository secret**

| Secret name          | Descrição                                            |
|-----------------------|------------------------------------------------------|
| `EVOLUTION_URL`      | URL base da Evolution API                            |
| `EVOLUTION_APIKEY`   | API Key da instância                                 |
| `EVOLUTION_INSTANCE` | Nome da instância                                    |
| `EVOLUTION_PHONE`    | Número pessoal com DDI, sem `+` — ex: `5551999990000` |
| `EVOLUTION_GROUP`    | ID do grupo do WhatsApp — ex: `120363000000000000@g.us` |

### 4. Commit e Push

Suba os arquivos para o repositório. O GitHub Actions vai rodar automaticamente todo dia às **06:00 (horário de Brasília / 09:00 UTC)**.

---

## 🧪 Testar manualmente

Na aba **Actions** do seu repositório, clique em:
**"🎂 Verificar Aniversariantes" → "Run workflow"**

---

## 💬 Como funciona

- O script busca a planilha publicada em `SHEETS_URL` e lê as colunas **Nome**, **Dia**, **Mês** e **Célula**
- Compara com a data atual (horário de Brasília) e monta a mensagem:
  - Sem aniversariante: mensagem avisando que não há ninguém no dia
  - Um aniversariante: mensagem citando nome (e célula, se preenchida)
  - Vários aniversariantes: lista com todos os nomes do dia
- Envia duas mensagens via Evolution API: uma para o número pessoal (`EVOLUTION_PHONE`) e outra para o grupo (`EVOLUTION_GROUP`)

---

## 📁 Estrutura dos arquivos

```
.
├── check_birthdays.py
└── .github/
    └── workflows/
        └── birthday_check.yml
```
