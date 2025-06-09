from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import configparser
import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") or "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"

class BinaryAIDialog(QDialog):
    """
    Diálogo de IA Binária: responde perguntas e gera código binário de acordo com o pedido do usuário.
    """
    def __init__(self, binary_interpreter, parent=None):
        super().__init__(parent)
        self.binary_interpreter = binary_interpreter

        # Detecta idioma do usuário
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "user_settings.ini")
        self.user_name = "Usuário"
        self.language = "pt"
        if os.path.exists(config_path):
            config = configparser.ConfigParser()
            config.read(config_path, encoding="utf-8")
            self.user_name = config.get("User", "name", fallback="Usuário")
            self.language = config.get("User", "language", fallback="pt")
        # Textos multilíngues
        self.texts = {
            "pt": {
                "title": "IA Binária",
                "ask_label": "Pergunte algo para a IA (ex: faça um programa de soma):",
                "placeholder": "Exemplo: faça um programa de soma",
                "ask_btn": "Perguntar",
                "copy_btn": "Copiar Código",
                "welcome": "Olá, {name}! Como posso ajudar você hoje? 😊\n",
                "warn_empty": "Digite uma pergunta para a IA.",
                "not_supported": "# Desculpe, ainda não sei responder isso em binário. Tente pedir um programa simples de soma, subtração, multiplicação, divisão, par ou ímpar, maior/menor, tabuada, fatorial, média.",
                "done": "Tarefa finalizada, {name}! Aqui está o código solicitado:\n\n"
            },
            "en": {
                "title": "Binary AI",
                "ask_label": "Ask something to the AI (e.g.: make a sum program):",
                "placeholder": "Example: make a sum program",
                "ask_btn": "Ask",
                "copy_btn": "Copy Code",
                "welcome": "Hello, {name}! How can I help you today? 😊\n",
                "warn_empty": "Please 'enter a question for the AI.",
                "not_supported": "# Sorry, I don't know how to answer this in binary yet. Try asking for a simple sum, subtraction, multiplication, division, even/odd, greater/smaller, multiplication table, factorial, or average program.",
                "done": "Task completed, {name}! Here is the requested code:\n\n"
            }
        }
        t = self.texts[self.language]
        self.setWindowTitle(t["title"])
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

        layout = QVBoxLayout(self)
        self.label = QLabel(t["ask_label"])
        layout.addWidget(self.label)
        self.input = QLineEdit()
        self.input.setPlaceholderText(t["placeholder"])
        layout.addWidget(self.input)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #181a20; color: #e6e6e6; font-family: 'Consolas'; font-size: 15px; border-radius: 6px;")
        layout.addWidget(self.output)
        btn_layout = QHBoxLayout()
        self.ask_btn = QPushButton(t["ask_btn"])
        self.ask_btn.clicked.connect(self._ask_ai)
        btn_layout.addWidget(self.ask_btn)
        self.copy_btn = QPushButton(t["copy_btn"])
        self.copy_btn.clicked.connect(self._copy_code)
        btn_layout.addWidget(self.copy_btn)
        layout.addLayout(btn_layout)

        # Mensagem de boas-vindas
        self.output.setPlainText(t["welcome"].format(name=self.user_name))

    def _ask_ai(self):
        t = self.texts[self.language]
        question = self.input.text().strip().lower()
        if not question:
            QMessageBox.warning(self, t["title"], t["warn_empty"])
            return

        # Exemplos multilíngues
        examples = [
            # Soma / Sum
            (["soma", "somar", "adicionar", "sum", "add"], 
            {
                "pt": 'num1 = float(input("Digite o primeiro valor: "))\n'
                      'num2 = float(input("Digite o segundo valor: "))\n'
                      'print("A soma é:", num1 + num2)\n',
                "en": 'num1 = float(input("Enter the first value: "))\n'
                      'num2 = float(input("Enter the second value: "))\n'
                      'print("The sum is:", num1 + num2)\n'
            }),
            # Subtração / Subtraction
            (["subtra", "diminuir", "subtract", "minus"], 
            {
                "pt": 'num1 = float(input("Digite o primeiro valor: "))\n'
                      'num2 = float(input("Digite o segundo valor: "))\n'
                      'print("A diferença é:", num1 - num2)\n',
                "en": 'num1 = float(input("Enter the first value: "))\n'
                      'num2 = float(input("Enter the second value: "))\n'
                      'print("The difference is:", num1 - num2)\n'
            }),
            # Multiplicação / Multiplication
            (["multiplic", "vezes", "multiply", "times"], 
            {
                "pt": 'num1 = float(input("Digite o primeiro valor: "))\n'
                      'num2 = float(input("Digite o segundo valor: "))\n'
                      'print("O produto é:", num1 * num2)\n',
                "en": 'num1 = float(input("Enter the first value: "))\n'
                      'num2 = float(input("Enter the second value: "))\n'
                      'print("The product is:", num1 * num2)\n'
            }),
            # Divisão / Division
            (["divis", "dividir", "divide", "division"], 
            {
                "pt": 'num1 = float(input("Digite o primeiro valor: "))\n'
                      'num2 = float(input("Digite o segundo valor: "))\n'
                      'if num2 != 0:\n'
                      '    print("O resultado é:", num1 / num2)\n'
                      'else:\n'
                      '    print("Divisão por zero não é permitida.")\n',
                "en": 'num1 = float(input("Enter the first value: "))\n'
                      'num2 = float(input("Enter the second value: "))\n'
                      'if num2 != 0:\n'
                      '    print("The result is:", num1 / num2)\n'
                      'else:\n'
                      '    print("Division by zero is not allowed.")\n'
            }),
            # Par ou ímpar / Even or Odd
            (["par ou ímpar", "par ou impar", "even or odd", "even", "odd"], 
            {
                "pt": 'num = int(input("Digite um número: "))\n'
                      'if num % 2 == 0:\n'
                      '    print("É par")\n'
                      'else:\n'
                      '    print("É ímpar")\n',
                "en": 'num = int(input("Enter a number: "))\n'
                      'if num % 2 == 0:\n'
                      '    print("It is even")\n'
                      'else:\n'
                      '    print("It is odd")\n'
            }),
            # Maior/Menor / Greater/Smaller
            (["maior", "menor", "greater", "smaller", "max", "min"], 
            {
                "pt": 'a = float(input("Digite o primeiro valor: "))\n'
                      'b = float(input("Digite o segundo valor: "))\n'
                      'if a > b:\n'
                      '    print("O maior é:", a)\n'
                      'elif b > a:\n'
                      '    print("O maior é:", b)\n'
                      'else:\n'
                      '    print("Os valores são iguais")\n',
                "en": 'a = float(input("Enter the first value: "))\n'
                      'b = float(input("Enter the second value: "))\n'
                      'if a > b:\n'
                      '    print("The greater is:", a)\n'
                      'elif b > a:\n'
                      '    print("The greater is:", b)\n'
                      'else:\n'
                      '    print("The values are equal")\n'
            }),
            # Tabuada / Multiplication Table
            (["tabuada", "multiplication table"], 
            {
                "pt": 'num = int(input("Digite um número para ver a tabuada: "))\n'
                      'for i in range(1, 11):\n'
                      '    print(f"{num} x {i} = {num * i}")\n',
                "en": 'num = int(input("Enter a number to see the multiplication table: "))\n'
                      'for i in range(1, 11):\n'
                      '    print(f"{num} x {i} = {num * i}")\n'
            }),
            # Fatorial / Factorial
            (["fatorial", "factorial"], 
            {
                "pt": 'num = int(input("Digite um número para calcular o fatorial: "))\n'
                      'f = 1\n'
                      'for i in range(2, num+1):\n'
                      '    f *= i\n'
                      'print("O fatorial é:", f)\n',
                "en": 'num = int(input("Enter a number to calculate the factorial: "))\n'
                      'f = 1\n'
                      'for i in range(2, num+1):\n'
                      '    f *= i\n'
                      'print("The factorial is:", f)\n'
            }),
            # Média / Average
            (["média", "media", "average"], 
            {
                "pt": 'n = int(input("Quantos números? "))\n'
                      'soma = 0\n'
                      'for i in range(n):\n'
                      '    valor = float(input(f"Digite o valor {i+1}: "))\n'
                      '    soma += valor\n'
                      'print("A média é:", soma / n)\n',
                "en": 'n = int(input("How many numbers? "))\n'
                      'total = 0\n'
                      'for i in range(n):\n'
                      '    value = float(input(f"Enter value {i+1}: "))\n'
                      '    total += value\n'
                      'print("The average is:", total / n)\n'
            }),
        ]

        code = None
        for keywords, example_dict in examples:
            if any(k in question for k in keywords):
                code = example_dict[self.language]
                break

        if not code:
            code = t["not_supported"]

        if not code.startswith("#"):
            code_lines = []
            for line in code.splitlines():
                parts = [part.strip() for part in line.split(';') if part.strip()]
                code_lines.extend(parts)
            code = "\n".join(code_lines)
            if not code.endswith('\n'):
                code += '\n'
            bin_code = self.binary_interpreter.converter_para_binario(code)
            self.output.setPlainText(
                f"{self.output.toPlainText().strip()}\n\n{t['done'].format(name=self.user_name)}{bin_code}"
            )
        else:
            self.output.setPlainText(code)

    def _copy_code(self):
        code = self.output.toPlainText()
        if code:
            QApplication.clipboard().setText(code)
