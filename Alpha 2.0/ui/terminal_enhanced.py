"""
Terminal interativo aprimorado para execução de comandos binários e Python.
Este módulo estende o terminal popup original para permitir a execução interativa
de comandos em formato binário e Python, com histórico e formatação avançada.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton, 
    QLineEdit, QComboBox, QLabel, QCheckBox, QSplitter, QTabWidget
)
from PyQt5.QtGui import QFont, QTextCursor, QColor, QTextCharFormat
from PyQt5.QtCore import Qt, QTimer

from binary_runner_enhanced import BinaryRunner

class TerminalEnhanced(QDialog):
    def __init__(self, initial_output="", parent=None):
        """
        Inicializa o terminal interativo aprimorado.
        
        Args:
            initial_output: Texto inicial a ser exibido no terminal
            parent: Widget pai
        """
        super().__init__(parent)
        self.setWindowTitle("Terminal Interativo")
        self.resize(700, 500)
        
        # Inicializa o executor de comandos
        self.runner = BinaryRunner()
        
        # Layout principal
        main_layout = QVBoxLayout()
        
        # Abas para diferentes modos
        self.tabs = QTabWidget()
        
        # Aba de terminal
        terminal_widget = QWidget()
        terminal_layout = QVBoxLayout(terminal_widget)
        
        # Área de saída do terminal
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(QFont("Consolas", 10))
        self.output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
            }
        """)
        
        if initial_output:
            self.output_area.setPlainText(initial_output)
            self.output_area.moveCursor(QTextCursor.End)
        
        # Layout para entrada de comando
        input_layout = QHBoxLayout()
        
        # Prompt do terminal
        self.prompt_label = QLabel(">>>")
        self.prompt_label.setFont(QFont("Consolas", 10))
        self.prompt_label.setStyleSheet("color: #50fa7b;")
        
        # Campo de entrada
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Consolas", 10))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
                padding: 2px;
            }
        """)
        self.input_field.setPlaceholderText("Digite um comando...")
        self.input_field.returnPressed.connect(self.executar_comando)
        
        # Checkbox para modo binário
        self.binary_mode = QCheckBox("Modo Binário")
        self.binary_mode.setStyleSheet("color: #bd93f9;")
        
        # Botão de execução
        self.execute_button = QPushButton("Executar")
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #6afa96;
            }
            QPushButton:pressed {
                background-color: #3fa65b;
            }
        """)
        self.execute_button.clicked.connect(self.executar_comando)
        
        # Adiciona widgets ao layout de entrada
        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.binary_mode)
        input_layout.addWidget(self.execute_button)
        
        # Adiciona widgets ao layout do terminal
        terminal_layout.addWidget(self.output_area)
        terminal_layout.addLayout(input_layout)
        
        # Aba de histórico
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        
        # Lista de histórico
        self.history_area = QPlainTextEdit()
        self.history_area.setReadOnly(True)
        self.history_area.setFont(QFont("Consolas", 10))
        self.history_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
            }
        """)
        
        # Botão para limpar histórico
        self.clear_history_button = QPushButton("Limpar Histórico")
        self.clear_history_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: #f8f8f2;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #ff6e6e;
            }
            QPushButton:pressed {
                background-color: #e64545;
            }
        """)
        self.clear_history_button.clicked.connect(self.limpar_historico)
        
        # Adiciona widgets ao layout de histórico
        history_layout.addWidget(self.history_area)
        history_layout.addWidget(self.clear_history_button)
        
        # Adiciona abas
        self.tabs.addTab(terminal_widget, "Terminal")
        self.tabs.addTab(history_widget, "Histórico")
        
        # Adiciona abas ao layout principal
        main_layout.addWidget(self.tabs)
        
        # Define o layout principal
        self.setLayout(main_layout)
        
        # Histórico de comandos para navegação com setas
        self.command_history = []
        self.history_index = -1
        
        # Atualiza o histórico ao iniciar
        self.atualizar_historico()
        
        # Foca no campo de entrada
        self.input_field.setFocus()
    
    def executar_comando(self):
        """Executa o comando digitado no campo de entrada."""
        comando = self.input_field.text().strip()
        if not comando:
            return
        
        # Adiciona o comando ao histórico de navegação
        self.command_history.append(comando)
        self.history_index = len(self.command_history)
        
        # Exibe o comando no terminal
        is_binary = self.binary_mode.isChecked()
        prompt = ">>> " if not is_binary else "BIN> "
        self.output_area.appendPlainText(f"{prompt}{comando}")
        
        # Executa o comando
        resultado = self.runner.executar_comando(comando, is_binary)
        
        # Exibe o resultado
        if resultado:
            self.output_area.appendPlainText(resultado)
        
        # Adiciona uma linha em branco para separar
        self.output_area.appendPlainText("")
        
        # Limpa o campo de entrada
        self.input_field.clear()
        
        # Atualiza o histórico
        self.atualizar_historico()
        
        # Rola para o final
        self.output_area.moveCursor(QTextCursor.End)
    
    def atualizar_historico(self):
        """Atualiza a exibição do histórico de execução."""
        self.history_area.clear()
        
        history = self.runner.get_history()
        if not history:
            self.history_area.setPlainText("Nenhum comando executado ainda.")
            return
        
        for i, (comando, resultado) in enumerate(history, 1):
            # Formata o histórico com cores
            self.history_area.appendPlainText(f"--- Comando {i} ---")
            self.history_area.appendPlainText(f">>> {comando}")
            self.history_area.appendPlainText(resultado)
            self.history_area.appendPlainText("")
    
    def limpar_historico(self):
        """Limpa o histórico de execução."""
        self.runner.clear_history()
        self.atualizar_historico()
        self.output_area.clear()
        self.output_area.setPlainText("Terminal limpo.")
    
    def keyPressEvent(self, event):
        """Trata eventos de teclado para navegação no histórico."""
        if self.input_field.hasFocus():
            if event.key() == Qt.Key_Up:
                # Navega para o comando anterior
                if self.command_history and self.history_index > 0:
                    self.history_index -= 1
                    self.input_field.setText(self.command_history[self.history_index])
                return
            elif event.key() == Qt.Key_Down:
                # Navega para o próximo comando
                if self.command_history and self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    self.input_field.setText(self.command_history[self.history_index])
                else:
                    # Se estiver no final do histórico, limpa o campo
                    self.history_index = len(self.command_history)
                    self.input_field.clear()
                return
        
        # Passa o evento para a classe pai
        super().keyPressEvent(event)
