#!/usr/bin/env python3
"""
Script para testar especificamente o arquivo problemático
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

def test_file_hierarchy(service, filename):
    """Testar hierarquia de um arquivo específico"""
    print(f"\n=== TESTANDO: {filename} ===")
    
    try:
        # Buscar arquivo por nome
        results = service.files().list(
            q=f"name='{filename}'",
            fields="files(id, name, mimeType, parents)"
        ).execute()
        
        files = results.get('files', [])
        if files:
            for file in files:
                print(f"ID: {file['id']}")
                print(f"Parents: {file.get('parents', [])}")
                
                # Navegar pela hierarquia completa
                path_parts = [sanitize_filename(file['name'])]
                current_file = file
                hierarchy = [file['name']]
                level = 0
                
                print(f"\nNavegando pela hierarquia:")
                print(f"Nível {level}: {file['name']}")
                
                while 'parents' in current_file and current_file['parents']:
                    parent_id = current_file['parents'][0]
                    try:
                        parent = service.files().get(fileId=parent_id).execute()
                        level += 1
                        print(f"Nível {level}: {parent['name']} (ID: {parent_id})")
                        print(f"  Parents do pai: {parent.get('parents', [])}")
                        
                        path_parts.insert(0, sanitize_filename(parent['name']))
                        hierarchy.insert(0, parent['name'])
                        current_file = parent
                    except Exception as e:
                        print(f"Erro ao obter pai {parent_id}: {str(e)}")
                        break
                
                print(f"\nHierarquia completa: {' > '.join(hierarchy)}")
                print(f"Path parts: {path_parts}")
                
                # Simular o que a função get_file_path faria
                relative_path = os.path.join(*path_parts)
                print(f"Relative path: {relative_path}")
                
        else:
            print(f"❌ Arquivo não encontrado: {filename}")
            
    except Exception as e:
        print(f"Erro ao buscar {filename}: {str(e)}")

def main():
    """Função principal"""
    print("=== TESTE DO ARQUIVO PROBLEMÁTICO ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Testar o arquivo problemático
    test_file_hierarchy(service, "Cópia de Relatórios Agosto 25 ANALISTA FLAVIA.xlsx")

if __name__ == '__main__':
    main() 