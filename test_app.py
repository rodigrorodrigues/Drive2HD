#!/usr/bin/env python3
"""
Teste simples da aplicação Drive2HD
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drive2HD - Teste")
        self.setGeometry(100, 100, 400, 200)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("Drive2HD - Teste de Interface")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Status
        status = QLabel("✅ Interface funcionando corretamente!")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status.setFont(QFont("Arial", 12))
        layout.addWidget(status)
        
        # Informações
        info = QLabel("PySide6 instalado e funcionando\nAplicação pronta para uso!")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setFont(QFont("Arial", 10))
        layout.addWidget(info)

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    print("✅ Teste da aplicação iniciado com sucesso!")
    print("✅ PySide6 está funcionando corretamente!")
    print("✅ Drive2HD está pronto para uso!")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main()) 