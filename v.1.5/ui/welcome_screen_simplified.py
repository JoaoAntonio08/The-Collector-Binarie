"""
Módulo para implementação da tela de boas-vindas com logo.
Este módulo fornece uma interface inicial quando não há abas abertas.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WelcomeScreen(QWidget):
    """
    Tela de boas-vindas exibida quando não há abas abertas.
    """
    def __init__(self, logo_path=None, parent=None):
        super().__init__(parent)
        self.logo_path = logo_path
        self._current_lang = "pt"
        self._setup_ui()
        self.set_language(self._current_lang)

    def set_language(self, lang):
        self._current_lang = lang
        if lang == "en":
            self.title_label.setText("The Collector Binarie")
            self.subtitle_label.setText("IDE for Binary Code Development")
            self.new_file_button.setText("New File")
            self.open_file_button.setText("Open File")
        else:
            self.title_label.setText("The Collector Binarie")
            self.subtitle_label.setText("IDE para Desenvolvimento em Código Binário")
            self.new_file_button.setText("Novo Arquivo")
            self.open_file_button.setText("Abrir Arquivo")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addStretch()

        # Logo centralizada e redimensionada
        if self.logo_path:
            logo_layout = QHBoxLayout()
            logo_layout.setAlignment(Qt.AlignCenter)
            logo_label = QLabel()
            pixmap = QPixmap(self.logo_path)
            # Redimensiona para no máximo 320x220 (igual à imagem 2)
            pixmap = pixmap.scaled(320, 220, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_layout.addWidget(logo_label)
            main_layout.addLayout(logo_layout)

        # Título
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #bd93f9; margin-bottom: 8px;")
        main_layout.addWidget(self.title_label)

        # Subtítulo
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setStyleSheet("font-size: 20px; color: #e6e6e6; margin-bottom: 20px;")
        main_layout.addWidget(self.subtitle_label)

        main_layout.addSpacing(10)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_layout.setSpacing(24)
        self.new_file_button = QPushButton()
        self.new_file_button.setObjectName("newFileButton")
        self.new_file_button.setMinimumWidth(160)
        self.new_file_button.setMinimumHeight(46)
        self.open_file_button = QPushButton()
        self.open_file_button.setObjectName("openFileButton")
        self.open_file_button.setMinimumWidth(160)
        self.open_file_button.setMinimumHeight(46)
        buttons_layout.addWidget(self.new_file_button)
        buttons_layout.addWidget(self.open_file_button)
        main_layout.addLayout(buttons_layout)

        main_layout.addStretch()

    def get_new_file_button(self):
        return self.new_file_button

    def get_open_file_button(self):
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
