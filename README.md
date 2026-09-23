# Drive2HD

PT-BR: Aplicação desktop (PySide6) para backup local do Google Drive, com dois modos:
- `main.py`: integração direta com a API do Google Drive.
- `main_rclone.py`: integração via Rclone (recomendada para grandes volumes).

EN: Desktop app (PySide6) to back up Google Drive locally, with two modes:
- `main.py`: direct Google Drive API integration.
- `main_rclone.py`: Rclone-based integration (recommended for large datasets).

## Funcionalidades / Features

- Backup completo e incremental
- Preservação da estrutura de pastas
- Interface gráfica com progresso e logs
- Persistência de configurações locais (`backup_info.json`)

## Requisitos / Requirements

- Python 3.8+
- Windows (scripts `.bat` incluídos; execução manual em outros sistemas pode funcionar)
- Conta Google com API do Drive habilitada
- (Modo Rclone) `rclone` instalado e configurado

## Instalação / Installation

### Dependências Python

```bash
pip install -r requirements.txt
```

Script disponível no repositório:
- `setup_rclone.bat` (instala dependências Python)

### Credenciais Google (modo API / `main.py`)

1. Crie um projeto no Google Cloud Console.
2. Habilite Google Drive API.
3. Gere OAuth Client ID para app desktop.
4. Salve o arquivo como `credentials.json` na raiz do projeto.

Use `credentials_example.json` apenas como referência de estrutura.

### Configuração Rclone (modo `main_rclone.py`)

1. Instale/configure o Rclone.
2. Crie um remote (ex.: `gdrive`) com `rclone config`.
3. Valide com `rclone lsd gdrive:`.

Script auxiliar no repositório:
- `install.bat` (setup guiado de Rclone no Windows)

## Uso / Usage

### Modo API (Google client)

```bash
python main.py
```

ou `run.bat`.

### Modo Rclone

```bash
python main_rclone.py
```

## Configuração local / Local configuration

Arquivos gerados localmente (ignorados pelo Git):
- `credentials.json`
- `token.json`
- `backup_info.json`

## Limitações conhecidas / Known limitations

- Projeto focado em Windows para fluxos com `.bat`.
- Scripts utilitários de diagnóstico exigem configuração manual de nomes/IDs de teste.
- Não há pipeline CI versionado neste repositório até o momento.

## Segurança e privacidade / Security & privacy

- **Nunca** commite `credentials.json` e `token.json`.
- Revogue tokens no Google Cloud em caso de exposição.
- Consulte `SECURITY.md` para reporte de vulnerabilidades.

## Contribuição / Contributing

Leia `CONTRIBUTING.md` antes de abrir PRs.

## Licenciamento / Licensing

Este repositório **ainda não possui licença open-source definida**.

Até a definição explícita de uma licença pelo proprietário, todos os direitos permanecem reservados por padrão. Veja `LICENSE_STATUS.md`.
