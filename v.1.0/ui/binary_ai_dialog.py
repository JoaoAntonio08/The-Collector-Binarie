from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import configparser
import os

class BinaryAIDialog(QDialog):
    """
    Diálogo de IA Binária: responde perguntas e gera código binário de acordo com o pedido do usuário.
    """
    def __init__(self, binary_interpreter, parent=None):
        super().__init__(parent)
        self.setWindowTitle("IA Binária")
        self.setMinimumSize(650, 420)
        self.setStyleSheet("""
            QDialog { background-color: #23272e; }
            QLabel { color: #bd93f9; font-size: 18px; }
            QLineEdit {
                background-color: #181a20;
                color: #e6e6e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #bd93f9;
            }
            QPlainTextEdit {
                background-color: #181a20;
                color: #e6e6e6;
                font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace;
                font-size: 16px;
                border-radius: 10px;
                padding: 12px;
                border: 1px solid #282a36;
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
        self.binary_interpreter = binary_interpreter

        layout = QVBoxLayout(self)
        self.label = QLabel("Pergunte algo para a IA (ex: faça um programa de soma):")
        layout.addWidget(self.label)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Exemplo: faça um programa de soma")
        layout.addWidget(self.input)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #181a20; color: #e6e6e6; font-family: 'Consolas'; font-size: 15px; border-radius: 6px;")
        layout.addWidget(self.output)
        btn_layout = QHBoxLayout()
        self.ask_btn = QPushButton("Perguntar")
        self.ask_btn.clicked.connect(self._ask_ai)
        btn_layout.addWidget(self.ask_btn)
        self.copy_btn = QPushButton("Copiar Código")
        self.copy_btn.clicked.connect(self._copy_code)
        btn_layout.addWidget(self.copy_btn)
        layout.addLayout(btn_layout)

        # Carrega nome do usuário do .ini
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.ini")
        self.user_name = "Usuário"
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path, encoding="utf-8")
            self.user_name = config.get("User", "name", fallback="Usuário")
        # Mensagem de boas-vindas
        self.output.setPlainText(f"Olá, {self.user_name}! Como posso ajudar você hoje? 😊\n")

    def _ask_ai(self):
        question = self.input.text().strip().lower()
        if not question:
            QMessageBox.warning(self, "Aviso", "Digite uma pergunta para a IA.")
            return

        examples = [
            # Soma
            (["soma", "somar", "adicionar"], 
            'num1 = float(input("Digite o primeiro valor: "))\n'
            'num2 = float(input("Digite o segundo valor: "))\n'
            'print("A soma é:", num1 + num2)\n'),

            # Subtração
            (["subtra", "diminuir"], 
            'num1 = float(input("Digite o primeiro valor: "))\n'
            'num2 = float(input("Digite o segundo valor: "))\n'
            'print("A diferença é:", num1 - num2)\n'),

            # Multiplicação
            (["multiplic", "vezes"], 
            'num1 = float(input("Digite o primeiro valor: "))\n'
            'num2 = float(input("Digite o segundo valor: "))\n'
            'print("O produto é:", num1 * num2)\n'),

            # Divisão
            (["divis", "dividir"], 
            'num1 = float(input("Digite o primeiro valor: "))\n'
            'num2 = float(input("Digite o segundo valor: "))\n'
            'if num2 != 0:\n'
            '    print("O resultado é:", num1 / num2)\n'
            'else:\n'
            '    print("Divisão por zero não é permitida.")\n'),

            # Par ou ímpar
            (["par ou ímpar", "par ou impar"], 
            'num = int(input("Digite um número: "))\n'
            'if num % 2 == 0:\n'
            '    print("É par")\n'
            'else:\n'
            '    print("É ímpar")\n'),

            # Maior/Menor
            (["maior", "menor"], 
            'a = float(input("Digite o primeiro valor: "))\n'
            'b = float(input("Digite o segundo valor: "))\n'
            'if a > b:\n'
            '    print("O maior é:", a)\n'
            'elif b > a:\n'
            '    print("O maior é:", b)\n'
            'else:\n'
            '    print("Os valores são iguais")\n'),

            # Tabuada
            (["tabuada"], 
            'num = int(input("Digite um número para ver a tabuada: "))\n'
            'for i in range(1, 11):\n'
            '    print(f"{num} x {i} = {num * i}")\n'),

            # Fatorial
            (["fatorial"], 
            'num = int(input("Digite um número para calcular o fatorial: "))\n'
            'f = 1\n'
            'for i in range(2, num+1):\n'
            '    f *= i\n'
            'print("O fatorial é:", f)\n'),

            # Média
            (["média", "media"], 
            'n = int(input("Quantos números? "))\n'
            'soma = 0\n'
            'for i in range(n):\n'
            '    valor = float(input(f"Digite o valor {i+1}: "))\n'
            '    soma += valor\n'
            'print("A média é:", soma / n)\n'),
        ]

        code = None
        for keywords, example_code in examples:
            if any(k in question for k in keywords):
                code = example_code
                break

        if not code:
            code = "# Desculpe, ainda não sei responder isso em binário. Tente pedir um programa simples de soma, subtração, multiplicação, divisão, par ou ímpar, maior/menor, tabuada, fatorial, média."

        if not code.startswith("#"):
            # Suporte a ; como delimitador de comandos para garantir quebra de linha
            # Exemplo: "a=1; b=2; print(a+b)" vira:
            # a=1
            # b=2
            # print(a+b)
            code_lines = []
            for line in code.splitlines():
                # Se houver ;, quebra em vários comandos
                parts = [part.strip() for part in line.split(';') if part.strip()]
                code_lines.extend(parts)
            code = "\n".join(code_lines)
            if not code.endswith('\n'):
                code += '\n'
            bin_code = self.binary_interpreter.converter_para_binario(code)
            bin_code = bin_code.replace("<e>", "").replace("<é>", "")
            self.output.setPlainText(
                f"{self.output.toPlainText().strip()}\n\nTarefa finalizada, {self.user_name}! Aqui está o código solicitado:\n\n{bin_code}"
            )
        else:
            self.output.setPlainText(code)

    def _copy_code(self):
        code = self.output.toPlainText()
        if code:
            QApplication.clipboard().setText(code)
