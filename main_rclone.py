#!/usr/bin/env python3
"""
Drive2HD - Backup do Google Drive usando Rclone
Interface moderna para Windows
"""

import sys
import os
import subprocess
import json
import threading
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QProgressBar, QFileDialog,
    QMessageBox, QComboBox, QLineEdit, QGroupBox, QGridLayout
)
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QFont, QIcon

class Config:
    """Configurações da aplicação"""
    APP_NAME = "Drive2HD - Rclone"
    VERSION = "2.0"
    
    @staticmethod
    def load_backup_info():
        """Carregar informações de backup"""
        try:
            with open('backup_info.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'last_backup_time': None,
                'destination_path': None,
                'rclone_remote': 'gdrive'
            }
    
    @staticmethod
    def save_backup_info(backup_info):
        """Salvar informações de backup"""
        with open('backup_info.json', 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)


class RcloneBackup(QMainWindow):
    """Interface principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        self.backup_thread = None
        self.backup_info = Config.load_backup_info()
        self.init_ui()
    
    def init_ui(self):
        """Inicializar interface do usuário"""
        self.setWindowTitle(f"{Config.APP_NAME} v{Config.VERSION}")
        self.setGeometry(100, 100, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Título
        title_label = QLabel(Config.APP_NAME)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Grupo de configurações
        config_group = QGroupBox("Configurações")
        config_layout = QGridLayout(config_group)
        
        # Pasta de destino
        self.destination_label = QLabel("Pasta de destino:")
        self.destination_path_label = QLabel("Nenhuma pasta selecionada")
        self.destination_path_label.setStyleSheet("color: gray;")
        self.browse_button = QPushButton("Escolher pasta")
        self.browse_button.clicked.connect(self.browse_destination)
        
        config_layout.addWidget(self.destination_label, 0, 0)
        config_layout.addWidget(self.destination_path_label, 0, 1)
        config_layout.addWidget(self.browse_button, 0, 2)
        
        # Remote do Rclone
        self.remote_label = QLabel("Remote do Rclone:")
        self.remote_combo = QComboBox()
        self.remote_combo.addItems(['gdrive', 'google-drive', 'drive'])
        self.remote_combo.setCurrentText(self.backup_info.get('rclone_remote', 'gdrive'))
        
        config_layout.addWidget(self.remote_label, 1, 0)
        config_layout.addWidget(self.remote_combo, 1, 1, 1, 2)
        
        layout.addWidget(config_group)
        
        # Grupo de backup
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout(backup_group)
        
        # Tipo de backup
        self.backup_type_combo = QComboBox()
        self.backup_type_combo.addItems([
            "Backup Completo",
            "Backup Incremental (só arquivos novos/modificados)"
        ])
        backup_layout.addWidget(QLabel("Tipo de backup:"))
        backup_layout.addWidget(self.backup_type_combo)
        
        # Botões
        button_layout = QHBoxLayout()
        self.backup_button = QPushButton("Iniciar Backup")
        self.backup_button.clicked.connect(self.start_backup)
        self.stop_button = QPushButton("Parar Backup")
        self.stop_button.clicked.connect(self.stop_backup)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.backup_button)
        button_layout.addWidget(self.stop_button)
        backup_layout.addLayout(button_layout)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        backup_layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("Pronto para backup")
        backup_layout.addWidget(self.status_label)
        
        layout.addWidget(backup_group)
        
        # Log
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Verificar se Rclone está instalado
        self.check_rclone()
    
    def check_rclone(self):
        """Verificar se Rclone está instalado"""
        try:
            result = subprocess.run(['rclone', 'version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.add_log_message("✅ Rclone encontrado!")
                version = result.stdout.split('\n')[0]
                self.add_log_message(f"Versão: {version}")
            else:
                self.add_log_message("❌ Rclone não encontrado!")
                self.add_log_message("Por favor, instale o Rclone: https://rclone.org/downloads/")
                self.backup_button.setEnabled(False)
        except FileNotFoundError:
            self.add_log_message("❌ Rclone não encontrado!")
            self.add_log_message("Por favor, instale o Rclone: https://rclone.org/downloads/")
            self.backup_button.setEnabled(False)
        except Exception as e:
            self.add_log_message(f"❌ Erro ao verificar Rclone: {str(e)}")
            self.backup_button.setEnabled(False)
    
    def browse_destination(self):
        """Escolher pasta de destino"""
        folder = QFileDialog.getExistingDirectory(
            self, "Escolher pasta de destino", 
            self.backup_info.get('destination_path', '')
        )
        
        if folder:
            self.backup_info['destination_path'] = folder
            self.destination_path_label.setText(folder)
            self.destination_path_label.setStyleSheet("color: black;")
            Config.save_backup_info(self.backup_info)
            self.add_log_message(f"Pasta de destino selecionada: {folder}")
    
    def start_backup(self):
        """Iniciar backup"""
        if not self.backup_info.get('destination_path'):
            QMessageBox.warning(self, "Aviso", "Por favor, escolha uma pasta de destino!")
            return
        
        self.backup_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Criar thread de backup
        self.backup_thread = RcloneBackupThread(
            self.backup_info['destination_path'],
            self.remote_combo.currentText(),
            self.backup_type_combo.currentText(),
            self.backup_info
        )
        
        # Conectar sinais
        self.backup_thread.progress_updated.connect(self.update_progress)
        self.backup_thread.status_updated.connect(self.update_status)
        self.backup_thread.log_message.connect(self.add_log_message)
        self.backup_thread.backup_completed.connect(self.backup_completed)
        
        # Iniciar thread
        self.backup_thread.start()
    
    def stop_backup(self):
        """Parar backup"""
        if self.backup_thread and self.backup_thread.isRunning():
            self.backup_thread.stop()
            self.backup_thread.wait()
        
        self.backup_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Backup interrompido")
    
    def update_progress(self, value):
        """Atualizar barra de progresso"""
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        """Atualizar status"""
        self.status_label.setText(status)
    
    def add_log_message(self, message):
        """Adicionar mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.ensureCursorVisible()
    
    def backup_completed(self, success):
        """Backup concluído"""
        self.backup_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if success:
            self.status_label.setText("Backup concluído com sucesso!")
            QMessageBox.information(self, "Sucesso", "Backup concluído com sucesso!")
        else:
            self.status_label.setText("Erro no backup")
            QMessageBox.critical(self, "Erro", "Ocorreu um erro durante o backup!")


class RcloneBackupThread(QThread):
    """Thread para executar backup com Rclone"""
    
    progress_updated = Signal(int)
    status_updated = Signal(str)
    log_message = Signal(str)
    backup_completed = Signal(bool)
    
    def __init__(self, destination_path, remote_name, backup_type, backup_info):
        super().__init__()
        self.destination_path = destination_path
        self.remote_name = remote_name
        self.backup_type = backup_type
        self.backup_info = backup_info
        self.stop_requested = False
    
    def run(self):
        """Executar backup"""
        try:
            self.log_message.emit("Iniciando backup com Rclone...")
            
            # Verificar se remote existe
            if not self.check_remote():
                self.log_message.emit("❌ Remote não configurado!")
                self.log_message.emit("Execute: rclone config")
                self.backup_completed.emit(False)
                return
            
            # Executar sincronização
            success = self.sync_files()
            
            if success:
                # Atualizar informações de backup
                self.backup_info['last_backup_time'] = datetime.now().astimezone().isoformat()
                self.backup_info['destination_path'] = self.destination_path
                self.backup_info['rclone_remote'] = self.remote_name
                Config.save_backup_info(self.backup_info)
                
                self.log_message.emit("✅ Backup concluído com sucesso!")
            
            self.backup_completed.emit(success)
            
        except Exception as e:
            self.log_message.emit(f"❌ ERRO: {str(e)}")
            self.backup_completed.emit(False)
    
    def check_remote(self):
        """Verificar se remote está configurado"""
        try:
            result = subprocess.run(
                ['rclone', 'listremotes'],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                remotes = result.stdout.strip().split('\n')
                if f"{self.remote_name}:" in remotes:
                    self.log_message.emit(f"✅ Remote '{self.remote_name}' encontrado!")
                    return True
                else:
                    self.log_message.emit(f"❌ Remote '{self.remote_name}' não encontrado!")
                    self.log_message.emit(f"Remotes disponíveis: {remotes}")
                    return False
            else:
                self.log_message.emit(f"❌ Erro ao listar remotes: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_message.emit(f"❌ Erro ao verificar remote: {str(e)}")
            return False
    
    def sync_files(self):
        """Sincronizar arquivos"""
        try:
            self.status_updated.emit("Sincronizando arquivos...")
            
            # Comando base do Rclone
            cmd = [
                'rclone', 'sync',
                f'{self.remote_name}:',
                self.destination_path,
                '--progress',
                '--stats', '30s',
                '--transfers', '4',
                '--checkers', '8',
                '--buffer-size', '16M'
            ]
            
            # Adicionar flags baseadas no tipo de backup
            if "Incremental" in self.backup_type:
                cmd.extend(['--update', '--modify-window', '1s'])
                self.log_message.emit("Modo incremental ativado")
            else:
                self.log_message.emit("Modo completo ativado")
            
            self.log_message.emit(f"Comando: {' '.join(cmd)}")
            
            # Executar comando
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitorar saída
            for line in process.stdout:
                if self.stop_requested:
                    process.terminate()
                    self.log_message.emit("Backup interrompido pelo usuário")
                    return False
                
                line = line.strip()
                if line:
                    self.log_message.emit(line)
                    
                    # Atualizar progresso se possível
                    if "Transferred:" in line:
                        try:
                            # Tentar extrair progresso da linha
                            if "100%" in line:
                                self.progress_updated.emit(100)
                        except:
                            pass
            
            # Aguardar conclusão
            return_code = process.wait()
            
            if return_code == 0:
                self.log_message.emit("✅ Sincronização concluída!")
                return True
            else:
                self.log_message.emit(f"❌ Sincronização falhou (código: {return_code})")
                return False
                
        except Exception as e:
            self.log_message.emit(f"❌ Erro na sincronização: {str(e)}")
            return False
    
    def stop(self):
        """Parar backup"""
        self.stop_requested = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)
    
    window = RcloneBackup()
    window.show()
    
    sys.exit(app.exec()) 