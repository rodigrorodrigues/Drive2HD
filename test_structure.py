#!/usr/bin/env python3
"""
Script de teste para verificar a estrutura de pastas
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configurações
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def authenticate_google_drive():
    """Autenticar com Google Drive"""
    creds = None
    
    # Carregar credenciais salvas
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Se não há credenciais válidas, fazer login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salvar credenciais
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Construir serviço
    service = build('drive', 'v3', credentials=creds)
    return service

def sanitize_filename(filename):
    """Sanitizar nome de arquivo removendo caracteres inválidos do Windows"""
    # Caracteres inválidos no Windows: < > : " | ? * \ /
    invalid_chars = '<>:"|?*\\/'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remover espaços no início e fim
    filename = filename.strip()
    
    # Se o nome ficou vazio, usar nome padrão
    if not filename:
        filename = "unnamed_file"
    
    return filename

def get_file_path(service, file, destination_path):
    """Construir caminho do arquivo"""
    # Construir caminho completo baseado na estrutura de pastas
    path_parts = [sanitize_filename(file['name'])]
    current_file = file
    
    print(f"Construindo caminho para: {file['name']}")
    print(f"Parents do arquivo: {file.get('parents', [])}")
    
    # Navegar pelos pais para construir o caminho completo
    while 'parents' in current_file and current_file['parents']:
        parent_id = current_file['parents'][0]
        try:
            parent = service.files().get(fileId=parent_id).execute()
            parent_name = sanitize_filename(parent['name'])
            path_parts.insert(0, parent_name)
            print(f"Pasta pai encontrada: {parent['name']} -> {parent_name}")
            current_file = parent
        except Exception as e:
            print(f"Erro ao obter pasta pai {parent_id}: {str(e)}")
            break
    
    # Construir caminho relativo
    relative_path = os.path.join(*path_parts)
    print(f"Estrutura de pastas: {' -> '.join(path_parts)}")
    
    full_path = os.path.join(destination_path, relative_path)
    print(f"Caminho final: {full_path}")
    
    return full_path

def test_structure():
    """Testar estrutura de pastas"""
    print("=== TESTE DE ESTRUTURA DE PASTAS ===")
    print()
    
    # Verificar se o arquivo de credenciais existe
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    # Autenticar
    print("Autenticando com Google Drive...")
    service = authenticate_google_drive()
    
    if not service:
        print("Falha na autenticação!")
        return
    
    print("Autenticação bem-sucedida!")
    
    # Obter alguns arquivos para teste
    try:
        results = service.files().list(
            pageSize=5,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
        ).execute()
        
        files = results.get('files', [])
        print(f"Encontrados {len(files)} arquivos para teste")
        print()
        
        destination_path = "C:/test_backup"
        
        for file in files:
            print("=" * 50)
            print(f"Arquivo: {file['name']}")
            print(f"Tipo: {file['mimeType']}")
            print(f"ID: {file['id']}")
            print(f"Parents: {file.get('parents', [])}")
            
            if file['mimeType'] != 'application/vnd.google-apps.folder':
                path = get_file_path(service, file, destination_path)
                print(f"Arquivo seria salvo em: {path}")
            else:
                print("É uma pasta - seria pulada no backup")
            
            print()
            
    except Exception as e:
        print(f"Erro ao obter arquivos: {str(e)}")

if __name__ == '__main__':
    test_structure() 