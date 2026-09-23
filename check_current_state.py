#!/usr/bin/env python3
"""
Script para verificar o estado atual dos arquivos
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

def check_current_files():
    """Verificar estado atual dos arquivos"""
    print("=== VERIFICAÇÃO ATUAL DOS ARQUIVOS ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Buscar por arquivos específicos
    target_files = [
        "exemplo_relatorio.xlsx",
        "exemplo_video.mp4",
        "exemplo_documento.docx"
    ]
    
    print(f"\nProcurando por arquivos específicos...")
    
    for filename in target_files:
        try:
            results = service.files().list(
                q=f"name='{filename}'",
                fields="files(id, name, mimeType, parents)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                for file in files:
                    print(f"\n📄 {file['name']}")
                    print(f"   ID: {file['id']}")
                    print(f"   Tipo: {file['mimeType']}")
                    print(f"   Parents: {file.get('parents', [])}")
                    
                    # Se tem pais, mostrar a hierarquia
                    if file.get('parents'):
                        current_file = file
                        hierarchy = [file['name']]
                        
                        while 'parents' in current_file and current_file['parents']:
                            parent_id = current_file['parents'][0]
                            try:
                                parent = service.files().get(fileId=parent_id).execute()
                                hierarchy.insert(0, parent['name'])
                                current_file = parent
                            except:
                                break
                        
                        print(f"   Hierarquia: {' > '.join(hierarchy)}")
                    else:
                        print(f"   ⚠️  SEM PAIS - arquivo na raiz")
            else:
                print(f"\n❌ Arquivo não encontrado: {filename}")
                
        except Exception as e:
            print(f"Erro ao buscar {filename}: {str(e)}")
    
    # Também verificar todas as pastas
    print(f"\n" + "="*60)
    print("VERIFICANDO TODAS AS PASTAS:")
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
            else:
                print(f"   ⚠️  SEM PAIS - pasta na raiz")
        
    except Exception as e:
        print(f"Erro ao buscar pastas: {str(e)}")

if __name__ == '__main__':
    check_current_files() 