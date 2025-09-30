#!/usr/bin/env python3
"""
Script para debugar a construção da estrutura de pastas
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

def debug_file_structure(service, file):
    """Debugar estrutura de um arquivo específico"""
    print(f"\n=== DEBUG: {file['name']} ===")
    print(f"ID: {file['id']}")
    print(f"Tipo: {file['mimeType']}")
    print(f"Parents: {file.get('parents', [])}")
    
    # Construir caminho completo
    path_parts = [sanitize_filename(file['name'])]
    current_file = file
    level = 0
    
    print(f"\nNavegando pela hierarquia:")
    print(f"Nível {level}: {file['name']}")
    
    while 'parents' in current_file and current_file['parents']:
        parent_id = current_file['parents'][0]
        try:
            parent = service.files().get(fileId=parent_id).execute()
            level += 1
            print(f"Nível {level}: {parent['name']} (ID: {parent_id})")
            path_parts.insert(0, sanitize_filename(parent['name']))
            current_file = parent
        except Exception as e:
            print(f"Erro ao obter pai {parent_id}: {str(e)}")
            break
    
    print(f"\nEstrutura final: {' -> '.join(path_parts)}")
    return path_parts

def test_specific_files():
    """Testar arquivos específicos que estão na raiz"""
    print("=== DEBUG DE ESTRUTURA DE PASTAS ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Arquivos que estão na raiz (baseado no check_structure.py)
    problem_files = [
        "2025-06-12-Bioinsumos-SolloAgro-Treinmento-Nogueira.pptx",
        "Alinhamento - Tutor - 2025_07_04 13_59 GMT-03_00 - Anotações do Gemini.docx",
        "Cópia de Suporte retenção - CS 2025.xlsx",
        "Indice de saúde do solo em SPD - Cherubin 2025.pptx",
        "SIGLAS _ Inadimplencia.xlsx",
        "Tutor _ Apresentação de Plataforma - Agro Para Todos - 2025_07_11 14_04 GMT-03_00 - Anotações do Gemini.docx"
    ]
    
    print(f"\nProcurando por {len(problem_files)} arquivos problemáticos...")
    
    for filename in problem_files:
        try:
            # Buscar arquivo por nome
            results = service.files().list(
                q=f"name='{filename}'",
                fields="files(id, name, mimeType, parents)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                for file in files:
                    debug_file_structure(service, file)
            else:
                print(f"\n❌ Arquivo não encontrado: {filename}")
                
        except Exception as e:
            print(f"Erro ao buscar {filename}: {str(e)}")

if __name__ == '__main__':
    test_specific_files() 