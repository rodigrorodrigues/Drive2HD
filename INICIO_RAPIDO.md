# 🚀 Início Rápido - Drive2HD

## ⚡ Execução em 3 Passos

### 1. Instalar

```bash
# Execute o instalador automático
install.bat
```

### 2. Configurar Google Drive

1. Vá para https://console.cloud.google.com/
2. Crie um projeto e ative a Google Drive API
3. Crie credenciais OAuth 2.0 para aplicação desktop
4. Baixe o arquivo JSON e renomeie para `credentials.json`
5. Coloque o arquivo na pasta do projeto

### 3. Executar

```bash
# Execute a aplicação
run.bat
```

## 📋 Checklist de Configuração

- [ ] Python 3.8+ instalado
- [ ] Dependências instaladas (`install.bat`)
- [ ] Projeto criado no Google Cloud Console
- [ ] Google Drive API ativada
- [ ] Credenciais OAuth 2.0 criadas
- [ ] Arquivo `credentials.json` na pasta do projeto
- [ ] Aplicação executada com sucesso

## 🎯 Primeira Execução

1. **Autenticar**: Clique em "Autenticar Google Drive"
2. **Autorizar**: Faça login no Google e autorize o acesso
3. **Destino**: Escolha onde salvar o backup
4. **Tipo**: Selecione "Backup Incremental"
5. **Iniciar**: Clique em "Iniciar Backup"

## 📁 Estrutura do Projeto

```
Drive2HD/
├── main.py                    # 🎯 Aplicação principal
├── config.py                  # ⚙️ Configurações
├── requirements.txt           # 📦 Dependências
├── install.bat               # 🔧 Instalador automático
├── run.bat                   # 🚀 Executor rápido
├── README.md                 # 📖 Documentação completa
├── SETUP.md                  # 🔧 Guia detalhado
├── INICIO_RAPIDO.md          # ⚡ Este guia
└── credentials.json          # 🔑 SUAS credenciais
```

## 🆘 Problemas Comuns

| Problema                          | Solução                                   |
| --------------------------------- | ----------------------------------------- |
| "Python não encontrado"           | Instale Python 3.8+                       |
| "credentials.json não encontrado" | Baixe credenciais do Google Cloud Console |
| "API não ativada"                 | Ative Google Drive API no console         |
| "Permissão negada"                | Execute como administrador                |
| "Token expirado"                  | Delete token.json e autentique novamente  |

## 📞 Suporte

- **Documentação completa**: `README.md`
- **Guia detalhado**: `SETUP.md`
- **Log de atividades**: Disponível na aplicação
- **Teste primeiro**: Use uma pasta pequena

## ⚠️ Importante

- O arquivo `credentials.json` é sensível - não compartilhe
- Backup incremental economiza tempo e banda
- Configurações são salvas automaticamente
- Log detalhado para diagnóstico de problemas

---

**🎉 Pronto! Sua aplicação Drive2HD está configurada e pronta para uso!**
