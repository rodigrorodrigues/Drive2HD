#!/usr/bin/env python3
"""
Script de teste para verificar se o backup está funcionando corretamente
"""

import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QThread, Signal
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

class TestBackupThread(QThread):
    log_message = Signal(str)
    status_updated = Signal(str)
    progress_updated = Signal(int)
    backup_completed = Signal(bool)
    
    def __init__(self, service, destination_path):
        super().__init__()
        self.service = service
        self.destination_path = destination_path
        self.stop_requested = False
    
    def run(self):
        try:
            self.log_message.emit("=== TESTE DE BACKUP ===")
            self.log_message.emit("Iniciando teste de backup...")
            
            # Obter lista de arquivos do Google Drive
            self.status_updated.emit("Obtendo lista de arquivos do Google Drive...")
            files = self.get_drive_files()
            
            if not files:
                self.log_message.emit("Nenhum arquivo encontrado no Google Drive!")
                self.backup_completed.emit(False)
                return
            
            self.log_message.emit(f"Encontrados {len(files)} arquivos no Google Drive")
            
            # Testar download de apenas 1 arquivo
            test_file = files[0]
            self.log_message.emit(f"Testando download do arquivo: {test_file['name']}")
            
            success = self.test_download_file(test_file)
            
            if success:
                self.log_message.emit("Teste de backup concluído com sucesso!")
                self.backup_completed.emit(True)
            else:
                self.log_message.emit("Teste de backup falhou!")
                self.backup_completed.emit(False)
                
        except Exception as e:
            self.log_message.emit(f"ERRO NO TESTE: {str(e)}")
            self.backup_completed.emit(False)
    
    def get_drive_files(self):
        files = []
        page_token = None
        
        try:
            results = self.service.files().list(
                pageSize=10,  # Limitar a 10 arquivos para teste
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
                pageToken=page_token
            ).execute()
            
            files.extend(results.get('files', []))
            self.log_message.emit(f"Arquivos obtidos: {len(files)}")
            
        except Exception as e:
            self.log_message.emit(f"Erro ao obter arquivos: {str(e)}")
        
        return files
    
    def test_download_file(self, file):
        try:
            self.status_updated.emit(f"Testando download: {file['name']}")
            
            # Criar pasta de teste
            test_path = os.path.join(self.destination_path, "test_backup")
            os.makedirs(test_path, exist_ok=True)
            
            file_path = os.path.join(test_path, file['name'])
            
            # Baixar arquivo
            if file['mimeType'] != 'application/vnd.google-apps.folder':
                self.log_message.emit(f"Baixando arquivo: {file['name']} (ID: {file['id']})")
                
                request = self.service.files().get_media(fileId=file['id'])
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    if self.stop_requested:
                        return False
                
                # Salvar arquivo
                with open(file_path, 'wb') as f:
                    f.write(fh.getvalue())
                
                self.log_message.emit(f"Arquivo salvo com sucesso: {file_path}")
                
                # Verificar se o arquivo foi criado
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    self.log_message.emit(f"Arquivo criado com sucesso! Tamanho: {file_size} bytes")
                    return True
                else:
                    self.log_message.emit("ERRO: Arquivo não foi criado!")
                    return False
            else:
                self.log_message.emit(f"Pulando pasta: {file['name']}")
                return True
                
        except Exception as e:
            self.log_message.emit(f"Erro ao baixar {file['name']}: {str(e)}")
            return False
    
    def stop(self):
        self.stop_requested = True

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

def main():
    print("=== TESTE DE BACKUP DO DRIVE2HD ===")
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
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    
    # Definir pasta de destino para teste
    destination_path = os.path.join(os.getcwd(), "test_backup_output")
    os.makedirs(destination_path, exist_ok=True)
    
    print(f"Pasta de destino para teste: {destination_path}")
    
    # Criar thread de teste
    test_thread = TestBackupThread(service, destination_path)
    
    # Conectar sinais
    def on_log_message(message):
        print(f"[LOG] {message}")
    
    def on_status_updated(status):
        print(f"[STATUS] {status}")
    
    def on_progress_updated(progress):
        print(f"[PROGRESSO] {progress}%")
    
    def on_backup_completed(success):
        if success:
            print("✅ TESTE CONCLUÍDO COM SUCESSO!")
            QMessageBox.information(None, "Teste", "Teste de backup concluído com sucesso!")
        else:
            print("❌ TESTE FALHOU!")
            QMessageBox.critical(None, "Teste", "Teste de backup falhou!")
        app.quit()
    
    test_thread.log_message.connect(on_log_message)
    test_thread.status_updated.connect(on_status_updated)
    test_thread.progress_updated.connect(on_progress_updated)
    test_thread.backup_completed.connect(on_backup_completed)
    
    # Iniciar teste
    print("Iniciando teste de backup...")
    test_thread.start()
    
    # Executar aplicação
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 