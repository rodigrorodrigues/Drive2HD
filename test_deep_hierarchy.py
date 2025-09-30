#!/usr/bin/env python3
"""
Script para testar a navegação completa pela hierarquia de pastas pai
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

def get_complete_hierarchy(service, file):
    """Obter hierarquia completa de um arquivo"""
    print(f"\n=== ANALISANDO: {file['name']} ===")
    print(f"ID: {file['id']}")
    print(f"Parents: {file.get('parents', [])}")
    
    path_parts = [sanitize_filename(file['name'])]
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
            path_parts.insert(0, sanitize_filename(parent['name']))
            hierarchy.insert(0, parent['name'])
            current_file = parent
        except Exception as e:
            print(f"Erro ao obter pai {parent_id}: {str(e)}")
            break
    
    print(f"\nHierarquia completa: {' > '.join(hierarchy)}")
    print(f"Path parts: {path_parts}")
    
    return {
        'name': file['name'],
        'hierarchy': hierarchy,
        'path_parts': path_parts,
        'levels': level
    }

def test_deep_hierarchy():
    """Testar hierarquia profunda"""
    print("=== TESTE DE HIERARQUIA PROFUNDA ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Buscar especificamente por arquivos que deveriam estar em subpastas
    problem_files = [
        "Cópia de Relatórios Agosto 25 ANALISTA FLAVIA.xlsx",
        "teste2.mp4",
        "arquivos videoteca.xlsx"
    ]
    
    print(f"\nProcurando por arquivos que deveriam estar em subpastas...")
    
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
                    analysis = get_complete_hierarchy(service, file)
            else:
                print(f"\n❌ Arquivo não encontrado: {filename}")
                
        except Exception as e:
            print(f"Erro ao buscar {filename}: {str(e)}")
    
    # Também buscar por pastas para entender a estrutura
    print(f"\n" + "="*60)
    print("BUSCANDO POR PASTAS:")
    print("="*60)
    
    try:
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder'",
            fields="files(id, name, mimeType, parents)",
            pageSize=50
        ).execute()
        
        folders = results.get('files', [])
        print(f"Encontradas {len(folders)} pastas")
        
        for folder in folders:
            print(f"\n📁 {folder['name']} (ID: {folder['id']})")
            print(f"   Parents: {folder.get('parents', [])}")
            
            # Se tem pais, mostrar a hierarquia
            if folder.get('parents'):
                current_folder = folder
                hierarchy = [folder['name']]
                
                while 'parents' in current_folder and current_folder['parents']:
                    parent_id = current_folder['parents'][0]
                    try:
                        parent = service.files().get(fileId=parent_id).execute()
                        hierarchy.insert(0, parent['name'])
                        current_folder = parent
                    except:
                        break
                
                print(f"   Hierarquia: {' > '.join(hierarchy)}")
        
    except Exception as e:
        print(f"Erro ao buscar pastas: {str(e)}")

if __name__ == '__main__':
    test_deep_hierarchy() 