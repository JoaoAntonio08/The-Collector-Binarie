from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QLineEdit
from ui.binary_runner import BinariosInterpreter

class TerminalPopup(QDialog):
    def __init__(self, saida):
        super().__init__()
        self.setWindowTitle("Terminal")

        # Layout principal
        layout = QVBoxLayout()

        # Área de texto para exibir saída
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)  # Somente leitura
        self.output_area.setPlainText(saida)

        # Campo de entrada do usuário
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Digite um comando...")

        # Botão para enviar comando
        self.send_button = QPushButton("Executar")
        self.send_button.clicked.connect(self.executar_comando)

        # Adiciona widgets ao layout
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_field)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def executar_comando(self):
        comando = self.input_field.text()
        if comando:
            self.output_area.appendPlainText(f"> {comando}")
            # Aqui você pode conectar o interpretador para processar a entrada
            resultado = BinariosInterpreter().executar_codigo(comando)
            self.output_area.appendPlainText(resultado)
