#!/usr/bin/env python3
"""
Script para testar todos os arquivos e suas estruturas
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

def analyze_file_structure(service, file):
    """Analisar estrutura de um arquivo"""
    path_parts = [sanitize_filename(file['name'])]
    current_file = file
    hierarchy = [file['name']]
    
    while 'parents' in current_file and current_file['parents']:
        parent_id = current_file['parents'][0]
        try:
            parent = service.files().get(fileId=parent_id).execute()
            parent_name = sanitize_filename(parent['name'])
            path_parts.insert(0, parent_name)
            hierarchy.insert(0, parent['name'])
            current_file = parent
        except Exception as e:
            break
    
    return {
        'name': file['name'],
        'id': file['id'],
        'mime_type': file['mimeType'],
        'parents': file.get('parents', []),
        'hierarchy': hierarchy,
        'path_parts': path_parts,
        'is_root': len(file.get('parents', [])) == 0
    }

def test_all_files():
    """Testar todos os arquivos"""
    print("=== ANÁLISE COMPLETA DE ESTRUTURA ===")
    
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        return
    
    service = authenticate_google_drive()
    if not service:
        print("Falha na autenticação!")
        return
    
    # Obter todos os arquivos
    try:
        results = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
        ).execute()
        
        files = results.get('files', [])
        print(f"Total de arquivos encontrados: {len(files)}")
        
        # Analisar cada arquivo
        root_files = []
        subfolder_files = []
        
        for file in files:
            if file['mimeType'] != 'application/vnd.google-apps.folder':
                analysis = analyze_file_structure(service, file)
                
                if analysis['is_root']:
                    root_files.append(analysis)
                else:
                    subfolder_files.append(analysis)
        
        print(f"\n📁 Arquivos na raiz do Google Drive: {len(root_files)}")
        print(f"📁 Arquivos em subpastas: {len(subfolder_files)}")
        
        print("\n" + "=" * 60)
        print("ARQUIVOS NA RAIZ DO GOOGLE DRIVE:")
        print("=" * 60)
        for file in root_files:
            print(f"📄 {file['name']}")
        
        print("\n" + "=" * 60)
        print("ARQUIVOS EM SUBPASTAS:")
        print("=" * 60)
        
        # Agrupar por pasta pai
        folders = {}
        for file in subfolder_files:
            if file['hierarchy']:
                parent_folder = file['hierarchy'][0]
                if parent_folder not in folders:
                    folders[parent_folder] = []
                folders[parent_folder].append(file)
        
        for folder, files in sorted(folders.items()):
            print(f"\n📁 {folder}:")
            for file in files:
                print(f"  📄 {file['name']}")
        
    except Exception as e:
        print(f"Erro ao obter arquivos: {str(e)}")

if __name__ == '__main__':
    test_all_files() 