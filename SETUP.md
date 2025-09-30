# Configuração detalhada do Google Cloud Console

> **Resumo rápido no [README.md](README.md#configurar-credenciais-do-google-obrigatório).**  
> Este guia é para quem quer o passo-a-passo completo com capturas de tela mentais.

---

## 1. Acesse o Google Cloud Console

- Abra https://console.cloud.google.com/
- Faça login com sua conta Google
- Aceite os termos se for o primeiro acesso

---

## 2. Crie (ou selecione) um projeto

1. No topo, clique em **"Selecionar projeto"** ▸ **"Novo projeto"**
2. Nome: `Drive2HD` (ou o que preferir)
3. Localização: sua organização ou "Sem organização"
4. **Criar** ▸ aguarde a notificação ▸ clique no sino ▸ **Selecionar projeto**

---

## 3. Ative a Google Drive API

1. Menu lateral ▸ **APIs e serviços** ▸ **Biblioteca**
2. Busque **"Google Drive API"**
3. Clique no card ▸ **Ativar**
4. Confirme se aparece "API ativada" com ✅ verde

---

## 4. Configure a tela de consentimento OAuth

> Obrigatório para apps "Externos" (qualquer conta Google pode logar).

1. **APIs e serviços** ▸ **Tela de consentimento OAuth**
2. **Tipo de usuário:** Externo ▸ **Criar**
3. **Nome do app:** `Drive2HD`
4. **E-mail de suporte do usuário:** seu e-mail
5. **E-mail de contato do desenvolvedor:** seu e-mail
6. **Salvar e continuar** (escopos: pular) ▸ **Salvar e continuar**
7. **Usuários de teste:** + **ADICIONAR USUÁRIOS** ▸ seu e-mail ▸ **Salvar e continuar**
8. **Resumo** ▸ **Voltar ao painel**

---

## 5. Crie as credenciais OAuth 2.0

1. **APIs e serviços** ▸ **Credenciais** ▸ **+ CRIAR CREDENCIAIS** ▸ **ID do cliente OAuth**
2. **Tipo de aplicativo:** Aplicativo para computador (Desktop app)
3. **Nome:** `Drive2HD Desktop`
4. **Criar** ▸ aparece modal com **ID do cliente** e **Chave secreta do cliente**
5. **BAIXAR JSON** ▸ salva como `credentials.json` na pasta do projeto

---

## 6. Teste

```bash
python main_rclone.py   # recomendado
# ou
python main.py
```

Na primeira execução:
- Abre o navegador em `accounts.google.com`
- Escolha sua conta ▸ **Continuar** ▸ "O Google não verificou este app" ▸ **Avançado** ▸ **Acessar Drive2HD (não seguro)** ▸ **Permitir**
- Volta pro app: pasta de destino ▸ tipo de backup ▸ **Iniciar Backup**

---

## Problemas comuns nessa etapa

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| "Error 400: redirect_uri_mismatch" | App tipo errado | Refaça credenciais como **Desktop app** |
| "Access blocked: app not verified" | Tela de consentimento incompleta | Adicione seu e-mail em **Usuários de teste** |
| "API not enabled" | Passo 3 pulado | Ative Google Drive API na Biblioteca |
| credentials.json não encontrado | Arquivo fora da pasta | Coloque na raiz do projeto (mesmo nível do `main.py`) |

---

## Segurança

- `credentials.json` **não versionado** (`.gitignore` já ignora)
- `token.json` gerado automaticamente na primeira auth
- Nunca compartilhe nenhum dos dois