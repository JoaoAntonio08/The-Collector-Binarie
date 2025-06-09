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
                font-size: 17px;
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

        # Título
        title = QLabel("Bem-vindo ao The Collector Binarie!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; color: #bd93f9; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        # Subtítulo
        subtitle = QLabel("Configure sua experiência inicial:")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 15px; color: #e6e6e6; margin-bottom: 18px;")
        layout.addWidget(subtitle)

        # Nome do usuário
        name_label = QLabel("Seu nome:")
        name_label.setStyleSheet("margin-top: 10px;")
        layout.addWidget(name_label)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite seu nome")
        layout.addWidget(self.name_input)

        # Tema
        layout.addWidget(QLabel("Tema:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Blue", "Dark", "White"])
        layout.addWidget(self.theme_combo)

        # Fonte
        layout.addWidget(QLabel("Tamanho da fonte:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 32)
        self.font_size_spin.setValue(16)
        layout.addWidget(self.font_size_spin)

        # Idioma
        layout.addWidget(QLabel("Idioma do aplicativo:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Português", "English"])
        layout.addWidget(self.lang_combo)

        # Botões
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Salvar e continuar")
        self.ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.ok_btn)
        self.cancel_btn = QPushButton("Cancelar")
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
