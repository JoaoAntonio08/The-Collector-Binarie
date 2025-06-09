from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QPushButton, QSpinBox
)
from PyQt5.QtCore import Qt

class InitialSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuração Inicial")
        self.setMinimumSize(440, 420)
        self.setStyleSheet("""
            QDialog {
                background-color: #23272e;
                border-radius: 16px;
            }
            QLabel {
                color: #bd93f9;
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 2px;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #181a20;
                color: #e6e6e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                min-width: 220px;
                border: 1px solid #bd93f9;
                margin-bottom: 8px;
            }
            QPushButton {
                background-color: #bd93f9;
                color: #23272e;
                border-radius: 10px;
                padding: 12px 28px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #a882e6;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(18)

        # Textos multilíngues
        self.texts = {
            "pt": {
                "title": "Configuração Inicial",
                "welcome": "Bem-vindo ao The Collector Binarie!",
                "subtitle": "Configure sua experiência inicial:",
                "name_label": "Seu nome:",
                "theme_label": "Tema:",
                "font_label": "Tamanho da fonte:",
                "lang_label": "Idioma do aplicativo:",
                "ok_btn": "Salvar e continuar",
                "cancel_btn": "Cancelar"
            },
            "en": {
                "title": "Initial Setup",
                "welcome": "Welcome to The Collector Binarie!",
                "subtitle": "Set up your initial experience:",
                "name_label": "Your name:",
                "theme_label": "Theme:",
                "font_label": "Font size:",
                "lang_label": "Application language:",
                "ok_btn": "Save and continue",
                "cancel_btn": "Cancel"
            }
        }
        self.language = "pt"

        # Título
        title = QLabel(self.texts[self.language]["welcome"])
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; color: #bd93f9; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Subtítulo
        subtitle = QLabel(self.texts[self.language]["subtitle"])
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 15px; color: #e6e6e6; margin-bottom: 18px;")
        layout.addWidget(subtitle)

        # Nome do usuário
        name_label = QLabel(self.texts[self.language]["name_label"])
        name_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome" if self.language == "pt" else "Enter your name")
        layout.addWidget(self.name_input)

        # Tema
        layout.addWidget(QLabel(self.texts[self.language]["theme_label"]))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Blue", "Dark", "White"])
        layout.addWidget(self.theme_combo)

        # Fonte
        layout.addWidget(QLabel(self.texts[self.language]["font_label"]))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 32)
        self.font_size_spin.setValue(16)
        layout.addWidget(self.font_size_spin)

        # Idioma
        layout.addWidget(QLabel(self.texts[self.language]["lang_label"]))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Português", "English"])
        layout.addWidget(self.lang_combo)

        # Botões
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton(self.texts[self.language]["ok_btn"])
        self.ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.ok_btn)
        self.cancel_btn = QPushButton(self.texts[self.language]["cancel_btn"])
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    @property
    def name(self):
        return self.name_input.text().strip() or "Usuário"

    @property
    def theme(self):
        idx = self.theme_combo.currentIndex()
        return ["dark_blue", "dark", "white"][idx]

    @property
    def font_size(self):
        return self.font_size_spin.value()

    @property
    def language(self):
        return "pt" if self.lang_combo.currentIndex() == 0 else "en"
