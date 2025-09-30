#!/usr/bin/env python3
"""
Script para testar a correção da hierarquia de pastas
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
    
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    service = build('drive', 'v3', credentials=creds)
    return service

def sanitize_filename(filename):
    """Sanitizar nome de arquivo"""
    invalid_chars = '<>:"|?*\\/'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    filename = filename.strip()
    if not filename:
        filename = "unnamed_file"
    return filename

def get_file_path_fixed(service, file, destination_path):
    """Versão corrigida da função get_file_path"""
    # Construir caminho completo baseado na estrutura de pastas
    path_parts = [sanitize_filename(file['name'])]
    current_file = file
    
    print(f"\nConstruindo caminho para: {file['name']}")
    print(f"Parents iniciais: {file.get('parents', [])}")
    
    # Navegar pelos pais para construir o caminho completo
    # Continuar até chegar na raiz (sem mais pais)
    while 'parents' in current_file and current_file['parents']:
        parent_id = current_file['parents'][0]
        try:
            parent = service.files().get(fileId=parent_id).execute()
            parent_name = sanitize_filename(parent['name'])
            path_parts.insert(0, parent_name)
            current_file = parent
            
            print(f"Pasta pai encontrada: {parent['name']} -> {parent_name}")
            
            # Não parar na pasta "Meu Drive" - continuar navegando
            # Só parar quando não houver mais pais
                
        except Exception as e:
            print(f"Erro ao obter pasta pai {parent_id}: {str(e)}")
            break
    
    # Construir caminho relativo
    relative_path = os.path.join(*path_parts)
    print(f"Estrutura final: {' -> '.join(path_parts)}")
    
    full_path = os.path.join(destination_path, relative_path)
    print(f"Caminho final: {full_path}")
    
    return full_path

def test_fixed_hierarchy():
    """Testar hierarquia corrigida"""
    print("=== TESTE DA HIERARQUIA CORRIGIDA ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Arquivos que deveriam estar em subpastas profundas
    test_files = [
        "Cópia de Relatórios Agosto 25 ANALISTA FLAVIA.xlsx",
        "teste2.mp4",
        "arquivos videoteca.xlsx"
    ]
    
    destination_path = "C:/test_backup_fixed"
    
    for filename in test_files:
        try:
            # Buscar arquivo por nome
            results = service.files().list(
                q=f"name='{filename}'",
                fields="files(id, name, mimeType, parents)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                for file in files:
                    path = get_file_path_fixed(service, file, destination_path)
                    print(f"✅ Arquivo seria salvo em: {path}")
            else:
                print(f"❌ Arquivo não encontrado: {filename}")
                
        except Exception as e:
            print(f"Erro ao buscar {filename}: {str(e)}")

if __name__ == '__main__':
    test_fixed_hierarchy() 