# Drive2HD - Backup do Google Drive

Uma aplicação moderna para Windows que faz backup do Google Drive mantendo a estrutura de pastas e formato dos arquivos, com funcionalidade de backup incremental para otimizar o processo.

## Características

- ✅ Interface moderna e intuitiva
- ✅ Backup incremental (baixa apenas arquivos modificados)
- ✅ Mantém estrutura de pastas original
- ✅ Preserva formato dos arquivos
- ✅ Progresso em tempo real
- ✅ Log detalhado de atividades
- ✅ Configurações salvas automaticamente
- ✅ Possibilidade de parar backup em andamento

## Pré-requisitos

1. **Python 3.8 ou superior**
2. **Conta Google com Google Drive**
3. **Arquivo de credenciais do Google Cloud Console**

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais do Google Drive

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a API do Google Drive
4. Crie credenciais OAuth 2.0 para aplicação desktop
5. Baixe o arquivo JSON das credenciais
6. Renomeie o arquivo para `credentials.json` e coloque na pasta do projeto

### 3. Executar a aplicação

```bash
python main.py
```

## Como usar

### Primeira execução

1. **Autenticar**: Clique em "Autenticar Google Drive"
2. **Selecionar destino**: Escolha a pasta onde salvar o backup
3. **Escolher tipo**: Selecione "Backup Incremental" (recomendado) ou "Backup Completo"
4. **Iniciar backup**: Clique em "Iniciar Backup"

### Backup incremental

- Na primeira execução, baixa todos os arquivos
- Nas execuções subsequentes, baixa apenas arquivos modificados desde o último backup
- Economiza tempo e banda de internet
- Mantém registro de todos os backups realizados

### Interface

- **Configurações**: Define pasta de destino e tipo de backup
- **Controles**: Botões para autenticar, iniciar e parar backup
- **Progresso**: Barra de progresso e status em tempo real
- **Log**: Registro detalhado de todas as atividades

## Estrutura de arquivos

```
Drive2HD/
├── main.py              # Aplicação principal
├── requirements.txt     # Dependências Python
├── README.md           # Este arquivo
├── credentials.json    # Credenciais do Google (você precisa baixar)
├── token.json          # Token de autenticação (gerado automaticamente)
└── backup_info.json    # Informações dos backups (gerado automaticamente)
```

## Configuração do Google Cloud Console

### Passo a passo detalhado:

1. **Acessar Google Cloud Console**

   - Vá para https://console.cloud.google.com/
   - Faça login com sua conta Google

2. **Criar projeto**

   - Clique em "Selecionar projeto" no topo
   - Clique em "Novo projeto"
   - Digite um nome (ex: "Drive2HD")
   - Clique em "Criar"

3. **Ativar API do Google Drive**

   - No menu lateral, vá em "APIs e serviços" > "Biblioteca"
   - Procure por "Google Drive API"
   - Clique na API e depois em "Ativar"

4. **Criar credenciais**

   - Vá em "APIs e serviços" > "Credenciais"
   - Clique em "Criar credenciais" > "ID do cliente OAuth"
   - Selecione "Aplicativo para computador"
   - Digite um nome (ex: "Drive2HD Desktop")
   - Clique em "Criar"

5. **Baixar credenciais**
   - Clique no ID do cliente criado
   - Clique em "Baixar JSON"
   - Renomeie o arquivo para `credentials.json`
   - Coloque na pasta do projeto

## Solução de problemas

### Erro de autenticação

- Verifique se o arquivo `credentials.json` está na pasta do projeto
- Certifique-se de que a API do Google Drive está ativada
- Tente deletar o arquivo `token.json` e autenticar novamente

### Erro de permissão

- Verifique se a pasta de destino tem permissões de escrita
- Execute a aplicação como administrador se necessário

### Backup não inicia

- Verifique se está autenticado no Google Drive
- Confirme se selecionou uma pasta de destino
- Verifique a conexão com a internet

## Recursos técnicos

- **Interface**: PySide6 com design moderno
- **API Google**: Google Drive API v3
- **Autenticação**: OAuth 2.0
- **Backup incremental**: Baseado em timestamp de modificação
- **Threading**: Operações de backup em thread separada
- **Persistência**: Configurações salvas em JSON

## Licença

Este projeto é de código aberto e pode ser usado livremente.

## Suporte

Para dúvidas ou problemas:

1. Verifique se seguiu todos os passos de configuração
2. Consulte o log de atividades na aplicação
3. Verifique se as credenciais estão corretas
4. Teste com uma pasta pequena primeiro
