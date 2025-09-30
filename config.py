import os
import json
from pathlib import Path

class Config:
    """Configurações centralizadas da aplicação"""
    
    # Configurações da aplicação
    APP_NAME = "Drive2HD"
    APP_VERSION = "1.0.0"
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    
    # Arquivos de configuração
    BACKUP_INFO_FILE = "backup_info.json"
    TOKEN_FILE = "token.json"
    CREDENTIALS_FILE = "credentials.json"
    
    # Configurações do Google Drive
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    # Configurações de backup
    DEFAULT_BACKUP_TYPE = "Backup Incremental"
    BACKUP_TYPES = ["Backup Completo", "Backup Incremental"]
    
    # Configurações de interface
    STYLESHEET = """
        QMainWindow {
            background-color: #f0f0f0;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 14px;
            border-radius: 5px;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #cccccc;
            border-radius: 5px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #4CAF50;
        }
        QProgressBar {
            border: 2px solid #cccccc;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 3px;
        }
        QTextEdit {
            border: 2px solid #cccccc;
            border-radius: 5px;
            font-family: 'Consolas', monospace;
            font-size: 12px;
        }
    """
    
    @classmethod
    def get_backup_info_path(cls):
        """Retorna o caminho completo do arquivo de informações de backup"""
        return os.path.join(os.getcwd(), cls.BACKUP_INFO_FILE)
    
    @classmethod
    def get_token_path(cls):
        """Retorna o caminho completo do arquivo de token"""
        return os.path.join(os.getcwd(), cls.TOKEN_FILE)
    
    @classmethod
    def get_credentials_path(cls):
        """Retorna o caminho completo do arquivo de credenciais"""
        return os.path.join(os.getcwd(), cls.CREDENTIALS_FILE)
    
    @classmethod
    def load_backup_info(cls):
        """Carrega as informações de backup do arquivo JSON"""
        if os.path.exists(cls.get_backup_info_path()):
            try:
                with open(cls.get_backup_info_path(), 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar backup_info.json: {e}")
        return {}
    
    @classmethod
    def save_backup_info(cls, backup_info):
        """Salva as informações de backup no arquivo JSON"""
        try:
            with open(cls.get_backup_info_path(), 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar backup_info.json: {e}")
    
    @classmethod
    def check_credentials_file(cls):
        """Verifica se o arquivo de credenciais existe"""
        return os.path.exists(cls.get_credentials_path())
    
    @classmethod
    def check_token_file(cls):
        """Verifica se o arquivo de token existe"""
        return os.path.exists(cls.get_token_path())
    
    @classmethod
    def get_app_data_dir(cls):
        """Retorna o diretório de dados da aplicação"""
        app_data = Path.home() / "AppData" / "Local" / cls.APP_NAME
        app_data.mkdir(parents=True, exist_ok=True)
        return app_data 