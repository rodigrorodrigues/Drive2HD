#!/usr/bin/env python3
"""
Script de teste simples para verificar se o backup está funcionando
"""

import sys
import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import json

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
                print("Por favor, configure suas credenciais do Google Drive.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salvar credenciais
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Construir serviço
    service = build('drive', 'v3', credentials=creds)
    return service

def get_drive_files(service):
    """Obter lista de arquivos do Google Drive"""
    files = []
    page_token = None
    
    try:
        print("Obtendo lista de arquivos do Google Drive...")
        results = service.files().list(
            pageSize=10,  # Limitar a 10 arquivos para teste
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
            pageToken=page_token
        ).execute()
        
        files.extend(results.get('files', []))
        print(f"Encontrados {len(files)} arquivos no Google Drive")
        
    except Exception as e:
        print(f"Erro ao obter arquivos: {str(e)}")
    
    return files

def get_export_mime_type(mime_type):
    """Mapear tipos de arquivos do Google Docs para tipos exportáveis"""
    export_mime_types = {
        'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
        'application/vnd.google-apps.spreadsheet': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'application/vnd.google-apps.presentation': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # .pptx
        'application/vnd.google-apps.drawing': 'image/png',  # .png
        'application/vnd.google-apps.form': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'application/vnd.google-apps.script': 'application/vnd.google-apps.script+json',  # .json
    }
    return export_mime_types.get(mime_type)

def get_file_extension(mime_type):
    """Obter extensão de arquivo para tipos do Google Docs"""
    extensions = {
        'application/vnd.google-apps.document': '.docx',
        'application/vnd.google-apps.spreadsheet': '.xlsx',
        'application/vnd.google-apps.presentation': '.pptx',
        'application/vnd.google-apps.drawing': '.png',
        'application/vnd.google-apps.form': '.xlsx',
        'application/vnd.google-apps.script': '.json',
    }
    return extensions.get(mime_type)

def get_file_path(file, destination_path):
    """Construir caminho do arquivo"""
    # Construir caminho completo baseado na estrutura de pastas
    path_parts = [file['name']]
    current_file = file
    
    # Navegar pelos pais para construir o caminho completo
    while 'parents' in current_file and current_file['parents']:
        parent_id = current_file['parents'][0]
        try:
            parent = service.files().get(fileId=parent_id).execute()
            path_parts.insert(0, parent['name'])
            current_file = parent
        except:
            break
    
    # Construir caminho relativo
    relative_path = os.path.join(*path_parts)
    
    # Adicionar extensão correta para arquivos do Google Docs
    if file['mimeType'].startswith('application/vnd.google-apps.'):
        extension = get_file_extension(file['mimeType'])
        if extension and not relative_path.endswith(extension):
            relative_path += extension
    
    # Criar diretório pai se não existir
    full_path = os.path.join(destination_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    return full_path

def test_download_file(service, file, destination_path):
    """Testar download de um arquivo"""
    try:
        print(f"Testando download: {file['name']}")
        
        # Criar pasta de teste
        test_path = os.path.join(destination_path, "test_backup")
        os.makedirs(test_path, exist_ok=True)
        
        # Usar apenas o nome do arquivo para simplificar o teste
        file_name = file['name']
        if file['mimeType'].startswith('application/vnd.google-apps.'):
            extension = get_file_extension(file['mimeType'])
            if extension and not file_name.endswith(extension):
                file_name += extension
        
        file_path = os.path.join(test_path, file_name)
        
        # Baixar arquivo
        if file['mimeType'] != 'application/vnd.google-apps.folder':
            print(f"Baixando arquivo: {file['name']} (ID: {file['id']})")
            
            # Verificar se é um arquivo do Google Docs
            if file['mimeType'].startswith('application/vnd.google-apps.'):
                # Para arquivos do Google Docs, usar export
                export_mime_type = get_export_mime_type(file['mimeType'])
                if export_mime_type:
                    request = service.files().export_media(fileId=file['id'], mimeType=export_mime_type)
                    print(f"Exportando arquivo do Google Docs: {file['name']}")
                else:
                    print(f"Tipo de arquivo não suportado: {file['mimeType']}")
                    return False
            else:
                # Para arquivos normais, usar get_media
                request = service.files().get_media(fileId=file['id'])
            
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Salvar arquivo
            with open(file_path, 'wb') as f:
                f.write(fh.getvalue())
            
            print(f"Arquivo salvo com sucesso: {file_path}")
            
            # Verificar se o arquivo foi criado
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"Arquivo criado com sucesso! Tamanho: {file_size} bytes")
                return True
            else:
                print("ERRO: Arquivo não foi criado!")
                return False
        else:
            print(f"Pulando pasta: {file['name']}")
            return True
            
    except Exception as e:
        print(f"Erro ao baixar {file['name']}: {str(e)}")
        return False

def main():
    print("=== TESTE SIMPLES DE BACKUP DO DRIVE2HD ===")
    print()
    
    # Verificar se o arquivo de credenciais existe
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
        print("Por favor, configure suas credenciais do Google Drive primeiro.")
        return
    
    # Autenticar
    print("Autenticando com Google Drive...")
    service = authenticate_google_drive()
    
    if not service:
        print("Falha na autenticação!")
        return
    
    print("Autenticação bem-sucedida!")
    
    # Obter arquivos
    files = get_drive_files(service)
    
    if not files:
        print("Nenhum arquivo encontrado no Google Drive!")
        return
    
    # Definir pasta de destino para teste
    destination_path = os.path.join(os.getcwd(), "test_backup_output")
    os.makedirs(destination_path, exist_ok=True)
    
    print(f"Pasta de destino para teste: {destination_path}")
    
    # Testar download de apenas 1 arquivo
    test_file = files[0]
    print(f"Testando download do arquivo: {test_file['name']}")
    
    success = test_download_file(service, test_file, destination_path)
    
    if success:
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("O backup está funcionando corretamente!")
    else:
        print("❌ TESTE FALHOU!")
        print("Há problemas no backup que precisam ser corrigidos.")

if __name__ == '__main__':
    main() 