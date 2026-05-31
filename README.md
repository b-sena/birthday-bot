# 🎂 Birthday Bot — WhatsApp via Z-API + GitHub Actions

Envia uma mensagem no WhatsApp todo dia se houver alguém aniversariante.

---

## 📋 Como configurar

### 1. Criar conta e instância na Z-API

1. Acesse [z-api.io](https://z-api.io) e crie uma conta (7 dias grátis)
2. Crie uma nova **instância**
3. Escaneie o QR Code com seu WhatsApp para conectar
4. Anote o **Instance ID**, o **Token** e o **Security Token** (Client Token)

### 2. Adicionar os Secrets no GitHub

No seu repositório, vá em:
**Settings → Secrets and variables → Actions → New repository secret**

| Secret name     | Onde encontrar na Z-API                  |
|-----------------|------------------------------------------|
| `ZAPI_INSTANCE` | ID da instância                          |
| `ZAPI_TOKEN`    | Token da instância                       |
| `ZAPI_SECURITY` | Security Token (Client Token)            |
| `ZAPI_PHONE`    | Seu número com DDI, sem `+` — ex: `5551999990000` |

### 3. Editar a lista de aniversariantes

Abra `check_birthdays.py` e edite a lista:

```python
ANIVERSARIANTES = [
    ("Maria Silva",   1, 15),   # (Nome, mês, dia)
    ("João Santos",   3, 22),
    # ...
]
```

### 4. Commit e Push

Suba os arquivos para o repositório. O GitHub Actions vai rodar automaticamente todo dia às **08:00 (horário de Brasília)**.

---

## 🧪 Testar manualmente

Na aba **Actions** do seu repositório, clique em:
**"🎂 Verificar Aniversariantes" → "Run workflow"**

---

## 📁 Estrutura dos arquivos

```
.
├── check_birthdays.py
└── .github/
    └── workflows/
        └── birthday_check.yml
```
