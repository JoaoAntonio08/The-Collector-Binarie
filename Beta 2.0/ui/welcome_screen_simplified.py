"""
Módulo para implementação da tela de boas-vindas com logo.
Este módulo fornece uma interface inicial quando não há abas abertas.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon

class WelcomeScreen(QWidget):
    """
    Tela de boas-vindas exibida quando não há abas abertas.
    """
    
    def __init__(self, parent=None, logo_path=None):
        """
        Inicializa a tela de boas-vindas.
        
        Args:
            parent: Widget pai
            logo_path: Caminho para o arquivo de logo
        """
        super().__init__(parent)
        
        # Caminho para o logo
        self.logo_path = logo_path
        
        # Configurações de estilo
        self.setObjectName("welcomeScreen")
        self.setStyleSheet("""
            #welcomeScreen {
                background-color: #181a20;
                border-radius: 18px;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #bd93f9;
                color: #23272e;
                border-radius: 12px;
                padding: 16px 36px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #a882e6;
            }
            #logoLabel {
                margin-bottom: 32px;
            }
            #titleLabel {
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 16px;
                color: #bd93f9;
            }
            #subtitleLabel {
                font-size: 20px;
                margin-bottom: 40px;
                color: #e6e6e6;
            }
        """)
        
        # Configura a interface
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface da tela de boas-vindas."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        self.logo_label = QLabel()
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setAlignment(Qt.AlignCenter)
        
        # Carrega o logo se existir
        if self.logo_path and os.path.exists(self.logo_path):
            pixmap = QPixmap(self.logo_path)
            pixmap = pixmap.scaled(220, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            # Logo de fallback (texto)
            self.logo_label.setText("THE COLLECTOR BINARIE")
            self.logo_label.setFont(QFont("Arial", 32, QFont.Bold))
        
        main_layout.addWidget(self.logo_label)
        
        # Título
        self.title_label = QLabel("The Collector Binarie")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 32, QFont.Bold))
        main_layout.addWidget(self.title_label)
        
        # Subtítulo
        self.subtitle_label = QLabel("IDE para Desenvolvimento em Código Binário")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setFont(QFont("Arial", 20))
        main_layout.addWidget(self.subtitle_label)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Botão para criar novo arquivo
        self.new_file_button = QPushButton("Novo Arquivo")
        self.new_file_button.setFont(QFont("Arial", 16))
        self.new_file_button.setMinimumSize(200, 56)
        buttons_layout.addWidget(self.new_file_button)
        
        # Botão para abrir arquivo
        self.open_file_button = QPushButton("Abrir Arquivo")
        self.open_file_button.setFont(QFont("Arial", 16))
        self.open_file_button.setMinimumSize(200, 56)
        buttons_layout.addWidget(self.open_file_button)
        
        main_layout.addLayout(buttons_layout)
    
    def get_new_file_button(self):
        """
        Obtém o botão de novo arquivo.
        
        Returns:
            Botão de novo arquivo
        """
        return self.new_file_button
    
    def get_open_file_button(self):
        """
        Obtém o botão de abrir arquivo.
        
        Returns:
            Botão de abrir arquivo
        """
        return self.open_file_button
    
    def set_logo(self, logo_path):
        """
        Define o logo da tela de boas-vindas.
        
        Args:
            logo_path: Caminho para o arquivo de logo
        """
        if logo_path and os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Redimensiona para um tamanho razoável
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
            self.logo_path = logo_path
