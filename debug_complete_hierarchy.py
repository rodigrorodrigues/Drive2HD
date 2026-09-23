#!/usr/bin/env python3
"""
Script para debugar completamente a hierarquia
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

def debug_complete_hierarchy(service, file_id):
    """Debugar hierarquia completa de um arquivo"""
    try:
        file = service.files().get(fileId=file_id).execute()
        print(f"\n=== DEBUG COMPLETO: {file['name']} ===")
        print(f"ID: {file['id']}")
        print(f"Tipo: {file['mimeType']}")
        print(f"Parents: {file.get('parents', [])}")
        
        hierarchy = [file['name']]
        current_file = file
        level = 0
        
        print(f"\nNavegando pela hierarquia completa:")
        print(f"Nível {level}: {file['name']}")
        
        while 'parents' in current_file and current_file['parents']:
            parent_id = current_file['parents'][0]
            try:
                parent = service.files().get(fileId=parent_id).execute()
                level += 1
                print(f"Nível {level}: {parent['name']} (ID: {parent_id}, Tipo: {parent['mimeType']})")
                print(f"  Parents do pai: {parent.get('parents', [])}")
                hierarchy.insert(0, parent['name'])
                current_file = parent
            except Exception as e:
                print(f"Erro ao obter pai {parent_id}: {str(e)}")
                break
        
        print(f"\nHierarquia completa: {' > '.join(hierarchy)}")
        return hierarchy
        
    except Exception as e:
        print(f"Erro ao debugar arquivo {file_id}: {str(e)}")
        return []

def test_specific_files():
    """Testar arquivos específicos"""
    print("=== DEBUG COMPLETO DE HIERARQUIA ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Defina IDs via variável de ambiente DRIVE2HD_TEST_IDS, separados por vírgula
    test_ids = [item.strip() for item in os.getenv("DRIVE2HD_TEST_IDS", "").split(",") if item.strip()]

    if not test_ids:
        print("Nenhum ID informado. Defina DRIVE2HD_TEST_IDS para executar este teste.")
        return

    for file_id in test_ids:
        debug_complete_hierarchy(service, file_id)

if __name__ == '__main__':
    test_specific_files() 