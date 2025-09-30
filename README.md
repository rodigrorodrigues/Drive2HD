# Drive2HD

**Backup do Google Drive para Windows — simples, confiável e com estrutura de pastas preservada.**

Uma aplicação desktop que baixa todo o seu Google Drive mantendo a hierarquia original de pastas, com suporte a backup incremental (só baixa o que mudou) e duas engines: API nativa do Google ou **rclone** (recomendado para volumes grandes).

---

## Por que existe?

O Google Drive não tem um cliente oficial de backup que preserve a estrutura de pastas de forma confiável no Windows. O Drive2HD resolve isso: você aponta a pasta de destino, autentica uma vez, e o app faz o resto — seja baixando tudo pela API do Google ou delegando pro **rclone**, que é muito mais rápido e robusto para sincronização.

---

## Qual versão usar?

| Versão | Arquivo | Ideal para |
|--------|---------|------------|
| **rclone (recomendado)** | `main_rclone.py` | Qualquer volume, estrutura complexa, confiabilidade máxima |
| **API Google** | `main.py` | Casos simples, sem instalar dependências extras |

> **Dica:** A versão rclone usa a mesma engine que o `rclone sync` — testada em produção há anos, lida com arquivos grandes, retomada de transferência, rate limits e preserva timestamps/metadados perfeitamente.

---

## Instalação rápida

```bash
# 1. Clone ou baixe o repositório
git clone https://github.com/rodigrorodrigues/Drive2HD.git
cd Drive2HD

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure credenciais (veja abaixo)
# 4. Rode
python main_rclone.py   # recomendado
# ou
python main.py
```

### Windows (sem terminal)

Dê duplo clique em:
- `install.bat` — instala dependências
- `setup_rclone.bat` — instala e configura o rclone (só na primeira vez)
- `run.bat` — abre a aplicação

---

## Configurar credenciais do Google (obrigatório)

Você precisa de um arquivo `credentials.json` na pasta do projeto. Ele **não vem no repositório** por segurança.

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto (ou use um existente)
3. Ative a **Google Drive API** (APIs e serviços → Biblioteca → Google Drive API → Ativar)
4. Crie credenciais OAuth 2.0:
   - Tipo: **Aplicativo para computador (Desktop app)**
   - Nome sugerido: `Drive2HD`
5. Baixe o JSON → renomeie para `credentials.json` → coloque na pasta do projeto

> A primeira execução abre o navegador para você autorizar o acesso. Um `token.json` é gerado automaticamente e reaproveitado nas próximas vezes.

---

## Como funciona o backup incremental

| Execução | O que acontece |
|----------|----------------|
| **Primeira** | Baixa **todos** os arquivos do Drive (pode demorar) |
| **Subsequentes** | Compara `modifiedTime` de cada arquivo — baixa **só o que mudou** |
| **Parada/retomada** | Você pode parar a qualquer momento; o progresso já feito fica salvo |

O app guarda a data do último backup em `backup_info.json` e usa isso como corte para o incremental.

---

## Estrutura de pastas preservada

```
Google Drive (nuvem)          Disco local (backup)
├── Documentos/               ├── Documentos/
│   ├── Trabalho/             │   ├── Trabalho/
│   │   └── relatorio.xlsx    │   │   └── relatorio.xlsx
│   └── Pessoal/              │   └── Pessoal/
│       └── foto.jpg          │       └── foto.jpg
└── Videos/                   └── Videos/
    └── apresentacao.mp4          └── apresentacao.mp4
```

Arquivos do Google Docs/Sheets/Slides são exportados automaticamente para `.docx`, `.xlsx`, `.pptx` etc.

---

## Solução de problemas

| Problema | O que tentar |
|----------|--------------|
| "credentials.json não encontrado" | Verifique se o arquivo está na raiz do projeto (mesma pasta do `main.py`) |
| Erro de autenticação / token expirado | Delete `token.json` e rode de novo — o navegador abre para reautorizar |
| "API não ativada" | No Cloud Console: APIs e serviços → Biblioteca → Google Drive API → Ativar |
| Permissão negada na pasta de destino | Rode como administrador ou escolha outra pasta |
| Backup não inicia | Confirme: autenticado? Pasta de destino selecionada? Internet ok? |
| rclone não encontrado | Rode `setup_rclone.bat` (instala e configura automaticamente) |

---

## Arquivos do projeto

```
Drive2HD/
├── main.py                 # App principal (API Google)
├── main_rclone.py          # App via rclone (recomendado)
├── config.py               # Configurações centralizadas
├── requirements.txt        # Dependências Python
├── credentials_example.json# Template de credenciais
├── .gitignore              # Ignora credentials.json, token.json, backup_info.json
├── install.bat             # Instala dependências (Windows)
├── run.bat                 # Executa app (Windows)
├── setup_rclone.bat        # Instala/configura rclone (Windows)
├── README.md               # Este arquivo
├── SETUP.md                # Guia detalhado de configuração
├── GUIA_RCLONE.md          # Guia completo do rclone
└── INICIO_RAPIDO.md        # Checklist de 3 passos
```

---

## Requisitos

- **Python 3.8+**
- **Windows 10/11** (testado; pode funcionar em Linux/macOS com ajustes nos `.bat`)
- Conta Google com Drive ativo

---

## Licença

MIT — use livremente, inclusive comercialmente. Código aberto, sem telemetria, sem dados seus saindo da sua máquina.

---

## Contribuindo

Achou um bug? Tem uma ideia? Abra uma *issue* ou mande um *PR*. Melhorias na UX, no rclone wrapper, na exportação de formatos Google Docs, testes automatizados — tudo bem-vindo.

---

## Agradecimentos

- [rclone](https://rclone.org/) — a engine de sincronização mais confiável que existe
- [PySide6](https://wiki.qt.io/Qt_for_Python) — interface nativa bonita e leve
- Google Drive API v3 — pela API (mesmo com rate limits chatos)