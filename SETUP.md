# Guia de Configuração - Drive2HD

Este guia te ajudará a configurar o Drive2HD passo a passo.

## Passo 1: Instalação

### Opção A - Instalação Automática (Recomendada)

1. Execute o arquivo `install.bat` clicando duas vezes nele
2. Aguarde a instalação das dependências
3. Pule para o Passo 2

### Opção B - Instalação Manual

1. Abra o PowerShell ou Prompt de Comando
2. Navegue até a pasta do projeto
3. Execute: `pip install -r requirements.txt`

## Passo 2: Configurar Google Drive API

### 2.1 Acessar Google Cloud Console

1. Vá para https://console.cloud.google.com/
2. Faça login com sua conta Google
3. Aceite os termos de serviço se solicitado

### 2.2 Criar Projeto

1. Clique em "Selecionar projeto" no topo da página
2. Clique em "Novo projeto"
3. Digite um nome (ex: "Drive2HD")
4. Clique em "Criar"

### 2.3 Ativar Google Drive API

1. No menu lateral, clique em "APIs e serviços" > "Biblioteca"
2. Procure por "Google Drive API"
3. Clique na API "Google Drive API"
4. Clique em "Ativar"

### 2.4 Criar Credenciais

1. No menu lateral, clique em "APIs e serviços" > "Credenciais"
2. Clique em "Criar credenciais" > "ID do cliente OAuth"
3. Se solicitado, configure a tela de consentimento OAuth:
   - Tipo de usuário: Externo
   - Nome do app: Drive2HD
   - Email de suporte: seu email
   - Clique em "Salvar e continuar"
   - Em "Escopos", clique em "Salvar e continuar"
   - Em "Usuários de teste", adicione seu email e clique em "Salvar e continuar"
4. Volte para "Credenciais" e clique em "Criar credenciais" > "ID do cliente OAuth"
5. Tipo de aplicativo: "Aplicativo para computador"
6. Nome: "Drive2HD Desktop"
7. Clique em "Criar"

### 2.5 Baixar Credenciais

1. Clique no ID do cliente que foi criado
2. Clique em "Baixar JSON"
3. Renomeie o arquivo para `credentials.json`
4. Mova o arquivo para a pasta do projeto Drive2HD

## Passo 3: Executar a Aplicação

### Opção A - Execução Rápida

1. Execute o arquivo `run.bat` clicando duas vezes nele

### Opção B - Execução Manual

1. Abra o PowerShell ou Prompt de Comando
2. Navegue até a pasta do projeto
3. Execute: `python main.py`

## Passo 4: Primeira Execução

1. **Autenticar**: Clique em "Autenticar Google Drive"
2. **Autorizar**: Uma janela do navegador abrirá, faça login e autorize o acesso
3. **Selecionar destino**: Clique em "Procurar" e escolha onde salvar o backup
4. **Escolher tipo**: Selecione "Backup Incremental" (recomendado)
5. **Iniciar backup**: Clique em "Iniciar Backup"

## Estrutura de Arquivos

Após a configuração, sua pasta deve ter esta estrutura:

```
Drive2HD/
├── main.py                    # Aplicação principal
├── config.py                  # Configurações
├── requirements.txt           # Dependências
├── README.md                 # Documentação principal
├── SETUP.md                  # Este guia
├── install.bat               # Instalador automático
├── run.bat                   # Executor rápido
├── credentials.json          # SUAS credenciais (você baixou)
├── token.json                # Token de acesso (gerado automaticamente)
├── backup_info.json          # Informações de backup (gerado automaticamente)
└── .gitignore               # Arquivos ignorados pelo Git
```

## Solução de Problemas

### Erro: "Arquivo credentials.json não encontrado"

- Verifique se o arquivo está na pasta do projeto
- Confirme se o nome está correto (sem espaços ou caracteres especiais)

### Erro: "API não ativada"

- Volte ao Google Cloud Console
- Verifique se a Google Drive API está ativada
- Aguarde alguns minutos e tente novamente

### Erro: "Permissão negada"

- Execute a aplicação como administrador
- Verifique se a pasta de destino tem permissões de escrita

### Erro: "Token expirado"

- Delete o arquivo `token.json`
- Autentique novamente

### Backup não inicia

- Verifique a conexão com a internet
- Confirme se está autenticado
- Verifique se selecionou uma pasta de destino

## Recursos Avançados

### Backup Incremental

- Na primeira execução: baixa todos os arquivos
- Execuções subsequentes: baixa apenas arquivos modificados
- Economiza tempo e banda de internet

### Log de Atividades

- Todas as operações são registradas
- Útil para diagnosticar problemas
- Mostra progresso em tempo real

### Configurações Salvas

- A pasta de destino é lembrada
- Credenciais são salvas automaticamente
- Informações de backup são preservadas

## Suporte

Se encontrar problemas:

1. Verifique se seguiu todos os passos
2. Consulte o log de atividades na aplicação
3. Teste com uma pasta pequena primeiro
4. Verifique se as credenciais estão corretas

## Segurança

- O arquivo `credentials.json` contém informações sensíveis
- Nunca compartilhe este arquivo
- O arquivo `token.json` é gerado automaticamente
- Ambos os arquivos estão no `.gitignore` para segurança
