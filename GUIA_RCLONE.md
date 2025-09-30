# Drive2HD - Guia de Configuração Rclone

## Por que usar Rclone?

O Rclone é uma ferramenta especializada em sincronização de arquivos que oferece:

✅ **Estrutura de pastas perfeita** - Mantém exatamente a mesma hierarquia do Google Drive  
✅ **Sincronização inteligente** - Só baixa arquivos modificados  
✅ **Suporte nativo ao Google Drive** - Feito especificamente para isso  
✅ **Mais rápido e confiável** - Otimizado para grandes volumes  
✅ **Interface simples** - Comando único para sincronizar tudo

## Instalação

### 1. Instalar Rclone

Execute o script de instalação:

```bash
setup_rclone.bat
```

Ou baixe manualmente:

1. Acesse: https://rclone.org/downloads/
2. Baixe a versão Windows
3. Extraia e adicione ao PATH

### 2. Configurar Google Drive

Execute no terminal:

```bash
rclone config
```

Siga os passos:

1. **Escolha `n`** (new remote)
2. **Nome do remote:** `gdrive`
3. **Escolha `drive`** (Google Drive)
4. **Escolha `n`** (não usar auto config)
5. **Client ID:** Deixe vazio (Enter)
6. **Client Secret:** Deixe vazio (Enter)
7. **Escolha `y`** (sim, usar auto config)
8. **Escolha `1`** (My Drive)
9. **Escolha `y`** (sim, confirma)
10. **Escolha `q`** (sair)

### 3. Testar Configuração

```bash
rclone lsd gdrive:
```

Deve mostrar as pastas do seu Google Drive.

## Uso da Aplicação

### 1. Executar Aplicação

```bash
python main_rclone.py
```

### 2. Configurar

1. **Escolher pasta de destino** - Clique em "Escolher pasta"
2. **Verificar remote** - Deve mostrar "gdrive" (ou o nome que você escolheu)
3. **Escolher tipo de backup:**
   - **Completo:** Baixa todos os arquivos
   - **Incremental:** Só arquivos novos/modificados

### 3. Iniciar Backup

Clique em "Iniciar Backup" e aguarde a conclusão.

## Vantagens do Rclone

### Estrutura Perfeita

```
Google Drive:                    Local:
├── Documentos/                  ├── Documentos/
│   ├── Trabalho/               │   ├── Trabalho/
│   │   └── relatorio.xlsx      │   │   └── relatorio.xlsx
│   └── Pessoal/                │   └── Pessoal/
│       └── foto.jpg            │       └── foto.jpg
└── Videos/                     └── Videos/
    └── apresentacao.mp4            └── apresentacao.mp4
```

### Sincronização Inteligente

- ✅ Só baixa arquivos modificados
- ✅ Mantém timestamps originais
- ✅ Detecta mudanças automaticamente
- ✅ Suporte a arquivos grandes

### Performance

- ✅ Múltiplas transferências simultâneas
- ✅ Buffer otimizado
- ✅ Retry automático em caso de erro
- ✅ Progresso em tempo real

## Comandos Úteis

### Listar arquivos

```bash
rclone ls gdrive:
```

### Listar pastas

```bash
rclone lsd gdrive:
```

### Sincronizar (modo seco - só simular)

```bash
rclone sync gdrive: C:\destino --dry-run
```

### Sincronizar (real)

```bash
rclone sync gdrive: C:\destino
```

### Sincronizar (só arquivos modificados)

```bash
rclone sync gdrive: C:\destino --update
```

## Solução de Problemas

### Erro de autenticação

```bash
rclone config reconnect gdrive:
```

### Verificar configuração

```bash
rclone config show
```

### Testar conexão

```bash
rclone about gdrive:
```

## Comparação: API vs Rclone

| Aspecto             | Google Drive API | Rclone      |
| ------------------- | ---------------- | ----------- |
| Estrutura de pastas | ❌ Complexa      | ✅ Perfeita |
| Performance         | ⚠️ Lenta         | ✅ Rápida   |
| Confiabilidade      | ⚠️ Instável      | ✅ Estável  |
| Configuração        | ❌ Complexa      | ✅ Simples  |
| Suporte             | ⚠️ Limitado      | ✅ Completo |

## Conclusão

O Rclone é a **melhor opção** para backup do Google Drive porque:

1. **Estrutura perfeita** - Mantém exatamente a hierarquia original
2. **Mais confiável** - Ferramenta especializada e testada
3. **Mais rápida** - Otimizada para transferências
4. **Mais simples** - Configuração única, uso contínuo

Recomendamos usar a versão Rclone (`main_rclone.py`) em vez da versão API (`main.py`).
