"""
Módulo para implementação do terminal integrado estilo Windows.
Este módulo fornece uma interface de terminal com aparência e funcionalidades
semelhantes ao terminal do Windows (cmd.exe).
"""

import os
import sys
import subprocess
import threading
import queue
import time
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QDialog, QScrollBar, QFrame, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt, QProcess, pyqtSignal, QTimer, QEvent
from PyQt5.QtGui import QFont, QColor, QTextCursor, QKeyEvent, QTextCharFormat

class WindowsStyleTerminal(QDialog):
    """
    Terminal integrado com estilo visual e funcionalidades do terminal do Windows.
    """
    
    # Sinais
    command_executed = pyqtSignal(str, str)  # comando, saída
    
    def __init__(self, parent=None, working_directory=None):
        """
        Inicializa o terminal estilo Windows.
        
        Args:
            parent: Widget pai
            working_directory: Diretório de trabalho inicial
        """
        super().__init__(parent)
        
        # Configurações básicas
        self.setWindowTitle("Terminal")
        self.setMinimumSize(600, 400)
        self.setModal(False)
        
        # Diretório de trabalho
        self.working_directory = working_directory or os.getcwd()
        
        # Histórico de comandos
        self.command_history = []
        self.history_index = -1
        
        # Processo do terminal
        self.process = None
        self.process_running = False
        
        # Filas para comunicação com o processo
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        
        # Configurações de estilo
        self.setObjectName("windowsTerminal")
        self.setStyleSheet("""
            #windowsTerminal {
                background-color: #0c0c0c;
                border: 1px solid #323232;
            }
            
            QTextEdit {
                background-color: #0c0c0c;
                color: #cccccc;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                selection-background-color: #264f78;
            }
            
            QLineEdit {
                background-color: #0c0c0c;
                color: #cccccc;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                selection-background-color: #264f78;
            }
            
            QPushButton {
                background-color: #323232;
                color: #cccccc;
                border: 1px solid #4d4d4d;
                padding: 5px 10px;
            }
            
            QPushButton:hover {
                background-color: #3e3e3e;
            }
            
            QPushButton:pressed {
                background-color: #505050;
            }
            
            QScrollBar:vertical {
                background-color: #0c0c0c;
                width: 14px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #323232;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #4d4d4d;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #0c0c0c;
            }
        """)
        
        # Configura a interface
        self._setup_ui()
        
        # Inicia o processo do terminal
        self._start_process()
    
    def _setup_ui(self):
        """Configura a interface do terminal."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Área de saída do terminal
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setLineWrapMode(QTextEdit.NoWrap)
        self.output_area.setFont(QFont("Consolas", 10))
        
        # Configura as cores do texto
        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QColor("#cccccc"))
        
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("#ff6b68"))
        
        self.success_format = QTextCharFormat()
        self.success_format.setForeground(QColor("#6ad468"))
        
        self.prompt_format = QTextCharFormat()
        self.prompt_format.setForeground(QColor("#f0c674"))
        
        # Adiciona a área de saída ao layout
        main_layout.addWidget(self.output_area)
        
        # Layout para entrada de comando
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(5, 5, 5, 5)
        input_layout.setSpacing(5)
        
        # Prompt de comando
        self.prompt_label = QLabel(f"{self.working_directory}>")
        self.prompt_label.setFont(QFont("Consolas", 10))
        self.prompt_label.setStyleSheet("color: #f0c674;")
        input_layout.addWidget(self.prompt_label)
        
        # Campo de entrada de comando
        self.command_input = QLineEdit()
        self.command_input.setFont(QFont("Consolas", 10))
        self.command_input.returnPressed.connect(self._execute_command)
        self.command_input.installEventFilter(self)
        input_layout.addWidget(self.command_input)
        
        # Adiciona o layout de entrada ao layout principal
        main_layout.addLayout(input_layout)
        
        # Foca no campo de entrada
        self.command_input.setFocus()
        
        # Exibe a mensagem de boas-vindas
        self._display_welcome_message()
    
    def _display_welcome_message(self):
        """Exibe a mensagem de boas-vindas do terminal."""
        welcome_text = (
            "Microsoft Windows [Versão 10.0.19045.3693]\n"
            "(c) Microsoft Corporation. Todos os direitos reservados.\n\n"
        )
        
        self._append_output(welcome_text)
        self._update_prompt()
    
    def _start_process(self):
        """Inicia o processo do terminal."""
        # Cria um novo processo
        self.process = QProcess()
        self.process.setWorkingDirectory(self.working_directory)
        
        # Conecta os sinais
        self.process.readyReadStandardOutput.connect(self._handle_stdout)
        self.process.readyReadStandardError.connect(self._handle_stderr)
        self.process.finished.connect(self._process_finished)
        
        # Inicia o shell com o ambiente do sistema
        # Não usamos setEnvironment, pois não está disponível em todas as versões do PyQt5
        if sys.platform == 'win32':
            self.process.start("cmd.exe")
        else:
            # Em sistemas não-Windows, emula o comportamento do CMD
            self.process.start("/bin/bash")
        
        self.process_running = True
    
    def _handle_stdout(self):
        """Manipula a saída padrão do processo."""
        data = self.process.readAllStandardOutput().data().decode('utf-8', errors='replace')
        self._append_output(data)
    
    def _handle_stderr(self):
        """Manipula a saída de erro do processo."""
        data = self.process.readAllStandardError().data().decode('utf-8', errors='replace')
        self._append_output(data, error=True)
    
    def _process_finished(self, exit_code, exit_status):
        """
        Manipula o término do processo.
        
        Args:
            exit_code: Código de saída
            exit_status: Status de saída
        """
        self.process_running = False
        
        # Reinicia o processo se necessário
        if exit_code != 0:
            self._append_output(f"\nProcesso encerrado com código {exit_code}.\n", error=True)
            self._start_process()
        else:
            self._append_output("\nProcesso encerrado.\n")
    
    def _execute_command(self):
        """Executa o comando digitado pelo usuário."""
        command = self.command_input.text().strip()
        if not command:
            return
        
        # Adiciona o comando ao histórico
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Exibe o comando na área de saída
        self._append_output(f"{self.prompt_label.text()} {command}\n")
        
        # Limpa o campo de entrada
        self.command_input.clear()
        
        # Comandos especiais
        if command.lower() == "cls" or command.lower() == "clear":
            self.output_area.clear()
            self._display_welcome_message()
            return
        
        if command.lower().startswith("cd "):
            # Muda o diretório de trabalho
            new_dir = command[3:].strip()
            
            # Expande o caminho
            if new_dir.startswith("~"):
                new_dir = os.path.expanduser(new_dir)
            
            # Verifica se o diretório existe
            if os.path.isdir(new_dir):
                self.working_directory = os.path.abspath(new_dir)
                self._update_prompt()
            else:
                self._append_output(f"O sistema não pode encontrar o caminho especificado: {new_dir}\n", error=True)
            
            return
        
        # Envia o comando para o processo
        if self.process_running:
            self.process.write(f"{command}\n".encode('utf-8'))
    
    def _append_output(self, text, error=False):
        """
        Adiciona texto à área de saída.
        
        Args:
            text: Texto a ser adicionado
            error: Se True, usa a formatação de erro
        """
        # Salva a posição atual do cursor
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # Define o formato
        if error:
            cursor.setCharFormat(self.error_format)
        else:
            cursor.setCharFormat(self.default_format)
        
        # Insere o texto
        cursor.insertText(text)
        
        # Rola para o final
        self.output_area.setTextCursor(cursor)
        self.output_area.ensureCursorVisible()
    
    def _update_prompt(self):
        """Atualiza o prompt de comando com o diretório atual."""
        self.prompt_label.setText(f"{self.working_directory}>")
    
    def eventFilter(self, obj, event):
        """
        Filtra eventos para o campo de entrada.
        
        Args:
            obj: Objeto que gerou o evento
            event: Evento
            
        Returns:
            True se o evento foi tratado, False caso contrário
        """
        if obj is self.command_input and event.type() == QEvent.KeyPress:
            key_event = QKeyEvent(event)
            
            # Navega pelo histórico de comandos
            if key_event.key() == Qt.Key_Up:
                self._navigate_history(-1)
                return True
            
            if key_event.key() == Qt.Key_Down:
                self._navigate_history(1)
                return True
        
        return super().eventFilter(obj, event)
    
    def _navigate_history(self, direction):
        """
        Navega pelo histórico de comandos.
        
        Args:
            direction: Direção da navegação (1 para frente, -1 para trás)
        """
        if not self.command_history:
            return
        
        # Atualiza o índice
        self.history_index += direction
        
        # Limita o índice
        if self.history_index < 0:
            self.history_index = 0
        elif self.history_index >= len(self.command_history):
            self.history_index = len(self.command_history)
            self.command_input.clear()
            return
        
        # Define o comando
        self.command_input.setText(self.command_history[self.history_index])
        self.command_input.selectAll()
    
    def closeEvent(self, event):
        """
        Manipula o evento de fechamento da janela.
        
        Args:
            event: Evento de fechamento
        """
        # Encerra o processo
        if self.process_running:
            self.process.terminate()
            self.process.waitForFinished(1000)
            
            if self.process.state() != QProcess.NotRunning:
                self.process.kill()
        
        event.accept()
    
    def set_working_directory(self, directory):
        """
        Define o diretório de trabalho.
        
        Args:
            directory: Novo diretório de trabalho
        """
        if os.path.isdir(directory):
            self.working_directory = os.path.abspath(directory)
            self._update_prompt()
            
            # Atualiza o diretório do processo
            if self.process_running:
                self.process.setWorkingDirectory(self.working_directory)
                self.process.write(f"cd {self.working_directory}\n".encode('utf-8'))
    
    def execute_command_programmatically(self, command):
        """
        Executa um comando programaticamente.
        
        Args:
            command: Comando a ser executado
        """
        # Define o comando no campo de entrada
        self.command_input.setText(command)
        
        # Executa o comando
        self._execute_command()
