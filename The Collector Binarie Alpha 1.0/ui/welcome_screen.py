"""
Módulo para implementação da tela de boas-vindas com logo.
Este módulo fornece uma interface para exibição quando não há abas abertas.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette

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
        
        # Configurações de estilo
        self.setObjectName("welcomeScreen")
        self.setStyleSheet("""
            #welcomeScreen {
                background-color: #0a0a23;
                border-radius: 10px;
            }
            
            QLabel {
                color: #ffffff;
            }
            
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
            }
            
            QLabel#subtitleLabel {
                font-size: 16px;
                color: #aaaaaa;
            }
            
            QPushButton {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 150px;
            }
            
            QPushButton:hover {
                background-color: #2d2d5a;
            }
            
            QPushButton#newFileButton {
                background-color: #00aa00;
            }
            
            QPushButton#newFileButton:hover {
                background-color: #00cc00;
            }
            
            QPushButton#openFileButton {
                background-color: #0066cc;
            }
            
            QPushButton#openFileButton:hover {
                background-color: #0088ff;
            }
        """)
        
        # Caminho para o logo
        self.logo_path = logo_path
        
        # Configura o layout
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface da tela de boas-vindas."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Espaçador superior
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Logo
        if self.logo_path:
            logo_layout = QHBoxLayout()
            logo_layout.setAlignment(Qt.AlignCenter)
            
            logo_label = QLabel()
            pixmap = QPixmap(self.logo_path)
            
            # Redimensiona o logo se for muito grande
            if pixmap.width() > 300 or pixmap.height() > 300:
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_layout.addWidget(logo_label)
            
            main_layout.addLayout(logo_layout)
        
        # Título
        title_label = QLabel("The Collector Binarie")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Editor e Interpretador de Código Binário")
        subtitle_label.setObjectName("subtitleLabel")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Espaçador
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(20)
        
        # Botão para novo arquivo
        self.new_file_button = QPushButton("Novo Arquivo")
        self.new_file_button.setObjectName("newFileButton")
        buttons_layout.addWidget(self.new_file_button)
        
        # Botão para abrir arquivo
        self.open_file_button = QPushButton("Abrir Arquivo")
        self.open_file_button.setObjectName("openFileButton")
        buttons_layout.addWidget(self.open_file_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Espaçador inferior
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
    
    def set_logo(self, logo_path):
        """
        Define o caminho para o arquivo de logo.
        
        Args:
            logo_path: Caminho para o arquivo de logo
        """
        self.logo_path = logo_path
        self._setup_ui()
    
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
