import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QProgressBar, QTextEdit, QMessageBox, QFrame,
                             QComboBox, QLineEdit, QGroupBox, QGridLayout)
from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
import requests
from config import Config

class GoogleDriveBackup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Config.APP_NAME} - Backup do Google Drive")
        self.setGeometry(100, 100, Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
        self.setStyleSheet(Config.STYLESHEET)
        
        self.backup_thread = None
        self.credentials = None
        self.service = None
        self.backup_info = Config.load_backup_info()
        
        self.init_ui()
        self.setup_google_auth()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("Drive2HD - Backup do Google Drive")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title_label)
        
        # Configurações
        config_group = QGroupBox("Configurações")
        config_layout = QGridLayout(config_group)
        
        # Pasta de destino
        self.dest_path_label = QLabel("Pasta de Destino:")
        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Selecione a pasta onde salvar o backup")
        self.browse_button = QPushButton("Procurar")
        self.browse_button.clicked.connect(self.browse_destination)
        
        config_layout.addWidget(self.dest_path_label, 0, 0)
        config_layout.addWidget(self.dest_path_edit, 0, 1)
        config_layout.addWidget(self.browse_button, 0, 2)
        
        # Tipo de backup
        self.backup_type_label = QLabel("Tipo de Backup:")
        self.backup_type_combo = QComboBox()
        self.backup_type_combo.addItems(Config.BACKUP_TYPES)
        self.backup_type_combo.setCurrentText(Config.DEFAULT_BACKUP_TYPE)
        
        config_layout.addWidget(self.backup_type_label, 1, 0)
        config_layout.addWidget(self.backup_type_combo, 1, 1, 1, 2)
        
        layout.addWidget(config_group)
        
        # Controles
        controls_layout = QHBoxLayout()
        
        self.auth_button = QPushButton("Autenticar Google Drive")
        self.auth_button.clicked.connect(self.authenticate_google_drive)
        
        self.backup_button = QPushButton("Iniciar Backup")
        self.backup_button.clicked.connect(self.start_backup)
        self.backup_button.setEnabled(False)
        
        self.stop_button = QPushButton("Parar Backup")
        self.stop_button.clicked.connect(self.stop_backup)
        self.stop_button.setEnabled(False)
        
        controls_layout.addWidget(self.auth_button)
        controls_layout.addWidget(self.backup_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Progresso
        progress_group = QGroupBox("Progresso")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.status_label = QLabel("Pronto para iniciar backup")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Log
        log_group = QGroupBox("Log de Atividades")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Carregar configurações salvas
        if 'destination_path' in self.backup_info:
            self.dest_path_edit.setText(self.backup_info['destination_path'])
    
    def browse_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino")
        if folder:
            self.dest_path_edit.setText(folder)
            self.backup_info['destination_path'] = folder
            Config.save_backup_info(self.backup_info)
            self.add_log_message(f"Pasta de destino selecionada: {folder}")
            self.add_log_message("Esta pasta será a raiz do backup. A estrutura do Google Drive será criada dentro dela.")
    
    def setup_google_auth(self):
        self.credentials = None
        
        # Carregar credenciais salvas
        if Config.check_token_file():
            self.credentials = Credentials.from_authorized_user_file(Config.get_token_path(), Config.SCOPES)
        
        # Se não há credenciais válidas, autenticar
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                self.add_log_message("Autenticação necessária. Clique em 'Autenticar Google Drive'")
    
    def authenticate_google_drive(self):
        try:
            if not Config.check_credentials_file():
                self.add_log_message("ERRO: Arquivo 'credentials.json' não encontrado!")
                self.add_log_message("Por favor, baixe o arquivo de credenciais do Google Cloud Console")
                return
            
            flow = InstalledAppFlow.from_client_secrets_file(Config.get_credentials_path(), Config.SCOPES)
            self.credentials = flow.run_local_server(port=0)
            
            # Salvar credenciais
            with open(Config.get_token_path(), 'w') as token:
                token.write(self.credentials.to_json())
            
            self.service = build('drive', 'v3', credentials=self.credentials)
            self.backup_button.setEnabled(True)
            self.auth_button.setEnabled(False)
            self.add_log_message("Autenticação realizada com sucesso!")
            
        except Exception as e:
            self.add_log_message(f"ERRO na autenticação: {str(e)}")
    
    def start_backup(self):
        if not self.dest_path_edit.text():
            QMessageBox.warning(self, "Erro", "Selecione uma pasta de destino!")
            return
        
        if not self.service:
            QMessageBox.warning(self, "Erro", "Autentique-se no Google Drive primeiro!")
            return
        
        self.backup_thread = BackupThread(
            self.service,
            self.dest_path_edit.text(),
            self.backup_type_combo.currentText(),
            self.backup_info
        )
        
        self.backup_thread.progress_updated.connect(self.update_progress)
        self.backup_thread.status_updated.connect(self.update_status)
        self.backup_thread.log_message.connect(self.add_log_message)
        self.backup_thread.backup_completed.connect(self.backup_completed)
        
        self.backup_thread.start()
        
        self.backup_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
    
    def stop_backup(self):
        if self.backup_thread and self.backup_thread.isRunning():
            self.backup_thread.stop()
            self.backup_thread.wait()
        
        self.backup_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Backup interrompido")
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        self.status_label.setText(status)
    
    def add_log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.ensureCursorVisible()
    
    def backup_completed(self, success):
        self.backup_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText("Backup concluído com sucesso!")
            QMessageBox.information(self, "Sucesso", "Backup concluído com sucesso!")
        else:
            self.status_label.setText("Erro no backup")
            QMessageBox.critical(self, "Erro", "Ocorreu um erro durante o backup!")
    
    def load_backup_info(self):
        return Config.load_backup_info()
    
    def save_backup_info(self):
        Config.save_backup_info(self.backup_info)


class BackupThread(QThread):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    log_message = Signal(str)
    backup_completed = Signal(bool)
    
    def __init__(self, service, destination_path, backup_type, backup_info):
        super().__init__()
        self.service = service
        self.destination_path = destination_path
        self.backup_type = backup_type
        self.backup_info = backup_info
        self.stop_requested = False
    
    def run(self):
        try:
            self.log_message.emit("Iniciando backup...")
            
            # Obter lista de arquivos do Google Drive
            self.status_updated.emit("Obtendo lista de arquivos do Google Drive...")
            files = self.get_drive_files()
            
            if self.stop_requested:
                return
            
            # Filtrar arquivos para backup incremental
            if self.backup_type == "Backup Incremental":
                files = self.filter_incremental_files(files)
            
            if not files:
                self.log_message.emit("Nenhum arquivo para backup encontrado!")
                self.backup_completed.emit(True)
                return
            
            # Fazer backup dos arquivos
            self.status_updated.emit(f"Fazendo backup de {len(files)} arquivos...")
            success = self.backup_files(files)
            
            self.backup_completed.emit(success)
            
        except Exception as e:
            self.log_message.emit(f"ERRO: {str(e)}")
            self.backup_completed.emit(False)
    
    def get_drive_files(self):
        files = []
        page_token = None
        
        while True:
            try:
                results = self.service.files().list(
                    pageSize=1000,
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents)",
                    pageToken=page_token
                ).execute()
                
                files.extend(results.get('files', []))
                page_token = results.get('nextPageToken', None)
                
                if not page_token:
                    break
                    
            except Exception as e:
                self.log_message.emit(f"Erro ao obter arquivos: {str(e)}")
                break
        
        return files
    
    def filter_incremental_files(self, files):
        if 'last_backup_time' not in self.backup_info:
            return files
        
        # Converter last_backup_time para datetime com timezone
        last_backup_str = self.backup_info['last_backup_time']
        if last_backup_str.endswith('Z'):
            last_backup_str = last_backup_str.replace('Z', '+00:00')
        last_backup = datetime.fromisoformat(last_backup_str)
        
        new_files = []
        
        for file in files:
            # Converter modifiedTime para datetime com timezone
            modified_str = file['modifiedTime']
            if modified_str.endswith('Z'):
                modified_str = modified_str.replace('Z', '+00:00')
            file_modified = datetime.fromisoformat(modified_str)
            
            if file_modified > last_backup:
                new_files.append(file)
        
        self.log_message.emit(f"Backup incremental: {len(new_files)} arquivos modificados desde o último backup")
        return new_files
    
    def backup_files(self, files):
        total_files = len(files)
        downloaded_files = []
        
        self.log_message.emit(f"Iniciando backup de {total_files} arquivos...")
        self.log_message.emit(f"Pasta raiz do backup: {self.destination_path}")
        
        for i, file in enumerate(files):
            if self.stop_requested:
                return False
            
            try:
                self.status_updated.emit(f"Baixando: {file['name']}")
                self.log_message.emit(f"Processando arquivo {i+1}/{total_files}: {file['name']}")
                
                # Criar estrutura de pastas
                file_path = self.get_file_path(file)
                self.log_message.emit(f"Caminho do arquivo: {file_path}")
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Baixar arquivo
                if file['mimeType'] != 'application/vnd.google-apps.folder':
                    self.log_message.emit(f"Baixando arquivo: {file['name']} (ID: {file['id']})")
                    
                    # Verificar se é um arquivo do Google Docs
                    if file['mimeType'].startswith('application/vnd.google-apps.'):
                        # Para arquivos do Google Docs, usar export
                        export_mime_type = self.get_export_mime_type(file['mimeType'])
                        if export_mime_type:
                            request = self.service.files().export_media(fileId=file['id'], mimeType=export_mime_type)
                            self.log_message.emit(f"Exportando arquivo do Google Docs: {file['name']}")
                        else:
                            self.log_message.emit(f"Tipo de arquivo não suportado: {file['mimeType']}")
                            continue
                    else:
                        # Para arquivos normais, usar get_media
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
                    
                    downloaded_files.append({
                        'id': file['id'],
                        'name': file['name'],
                        'path': file_path,
                        'modified': file['modifiedTime'],
                        'size': file.get('size', 0)
                    })
                else:
                    self.log_message.emit(f"Pulando pasta: {file['name']}")
                
                # Atualizar progresso
                progress = int((i + 1) / total_files * 100)
                self.progress_updated.emit(progress)
                
            except Exception as e:
                self.log_message.emit(f"Erro ao baixar {file['name']}: {str(e)}")
        
        # Atualizar informações de backup
        self.backup_info['last_backup_time'] = datetime.now().astimezone().isoformat()
        self.backup_info['downloaded_files'] = downloaded_files
        
        Config.save_backup_info(self.backup_info)
        
        self.log_message.emit(f"Backup concluído! {len(downloaded_files)} arquivos baixados")
        return True
    
    def get_export_mime_type(self, mime_type):
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
    
    def get_file_extension(self, mime_type):
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
    
    def sanitize_filename(self, filename):
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
    
    def get_file_path(self, file):
        # Construir caminho completo baseado na estrutura de pastas
        path_parts = [self.sanitize_filename(file['name'])]
        current_file = file
        
        # Navegar pelos pais para construir o caminho completo
        # Continuar até chegar na raiz (sem mais pais)
        while 'parents' in current_file and current_file['parents']:
            parent_id = current_file['parents'][0]
            try:
                parent = self.service.files().get(fileId=parent_id).execute()
                parent_name = self.sanitize_filename(parent['name'])
                
                # Se o pai for "Meu Drive", parar aqui pois é a raiz
                if parent_name.lower() in ['meu drive', 'my drive', 'drive']:
                    break
                
                path_parts.insert(0, parent_name)
                current_file = parent
                
                # Continuar navegando até não haver mais pais
                # Não parar em nenhuma pasta específica
                    
            except Exception as e:
                self.log_message.emit(f"Erro ao obter pasta pai {parent_id}: {str(e)}")
                break
        
        # Construir caminho relativo
        relative_path = os.path.join(*path_parts)
        
        # Adicionar extensão correta para arquivos do Google Docs
        if file['mimeType'].startswith('application/vnd.google-apps.'):
            extension = self.get_file_extension(file['mimeType'])
            if extension and not relative_path.endswith(extension):
                relative_path += extension
        
        full_path = os.path.join(self.destination_path, relative_path)
        
        return full_path
    
    def stop(self):
        self.stop_requested = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)
    
    window = GoogleDriveBackup()
    window.show()
    
    sys.exit(app.exec()) 