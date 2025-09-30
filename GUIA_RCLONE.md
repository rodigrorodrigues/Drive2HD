# Guia rclone — configuração e comandos úteis

> O **rclone** é a engine recomendada (`main_rclone.py`).  
> Este guia cobre só o que é específico do rclone.  
> Visão geral e comparação no [README.md](README.md#qual-versão-usar).

---

## Instalação automática (Windows)

```cmd
setup_rclone.bat
```

Faz tudo: baixa, extrai, coloca no PATH, abre `rclone config`.

---

## Instalação manual

1. Baixe em https://rclone.org/downloads/ (Windows 64-bit)
2. Extraia ▸ renomeie a pasta para `rclone` ▸ mova para `C:\rclone`
3. Adicione `C:\rclone` ao PATH do sistema (Variáveis de Ambiente)

Verifique:
```cmd
rclone version
```

---

## Configurar remote do Google Drive

```cmd
rclone config
```

Passo a passo:
```
n                 # New remote
gdrive            # Nome do remote (use este)
drive             # Storage: Google Drive
                  # client_id → Enter (vazio)
                  # client_secret → Enter (vazio)
y                 # Auto config? Yes
1                 # Scope: 1 = Full access (My Drive)
y                 # Confirm
y                 # Team Drive? No (Enter)
q                 # Quit
```

> Se der erro de auth: `rclone config reconnect gdrive:`

Teste:
```cmd
rclone lsd gdrive:
```
Deve listar suas pastas do Drive.

---

## Usar pelo app (`main_rclone.py`)

1. `python main_rclone.py`
2. Escolha pasta de destino
3. Remote: `gdrive` (já aparece se configurado)
4. Tipo: **Incremental** (recomendado) ou Completo
5. **Iniciar Backup**

---

## Comandos CLI diretos (sem o app)

| Ação | Comando |
|------|---------|
| Listar arquivos | `rclone ls gdrive:` |
| Listar pastas | `rclone lsd gdrive:` |
| Simular sync (dry-run) | `rclone sync gdrive: C:\destino --dry-run` |
| Sync real | `rclone sync gdrive: C:\destino` |
| Só novos/modificados | `rclone sync gdrive: C:\destino --update` |
| Ver progresso | `rclone sync gdrive: C:\destino -P` |
| Ver stats do remote | `rclone about gdrive:` |

### Flags úteis
- `-P` / `--progress` — barra de progresso
- `--transfers N` — paralelas (padrão 4, aumente se link bom)
- `--bwlimit 10M` — limitar banda
- `--dry-run` — simula sem gravar
- `--fast-list` — acelera listagem em drives grandes

---

## Estrutura preservada

```
gdrive:                        C:\destino\
├── Documentos/                ├── Documentos/
│   ├── Trabalho/              │   ├── Trabalho/
│   │   └── relatorio.xlsx     │   │   └── relatorio.xlsx
│   └── Pessoal/               │   └── Pessoal/
│       └── foto.jpg           │       └── foto.jpg
└── Videos/                    └── Videos/
    └── video.mp4                  └── video.mp4
```

Google Docs/Sheets/Slides → exportados como `.docx`, `.xlsx`, `.pptx`.

---

## Solução de problemas rclone

| Erro | Solução |
|------|---------|
| `Failed to get token` | `rclone config reconnect gdrive:` |
| `Rate limited` | `--bwlimit 5M --transfers 2` ou espere |
| `Permission denied` | Rode terminal como Admin; pasta destino com escrita |
| `Config not found` | `rclone config show` ▸ verifique se remote chama `gdrive` |
| Arquivos Google Docs não baixam | rclone exporta auto; se falhar, use `--drive-export-formats docx,xlsx,pptx` |

---

## Por que rclone > API nativa

| Critério | API Google (`main.py`) | rclone (`main_rclone.py`) |
|----------|------------------------|---------------------------|
| Estrutura de pastas | Frágil, quebra em profundidade | Nativa, perfeita |
| Velocidade | Uma transferência por vez | Paralela (configurável) |
| Retomada | Manual | Automática (`--progress`) |
| Rate limit | Seu código lida | Backoff interno |
| Google Docs export | Código próprio | Nativo (`--drive-export-formats`) |
| Manutenção | Sua | Comunidade ativa (10+ anos) |

**Conclusão:** use `main_rclone.py`. O app é só um wrapper GUI pro `rclone sync`.