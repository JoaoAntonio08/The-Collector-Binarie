"""
Módulo para implementação de terminal estilo Windows simplificado.
Esta versão corrige problemas de compatibilidade e suporte a entrada de dados.
"""

import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit, 
    QLineEdit, QPushButton, QLabel, QSplitter
)
from PyQt5.QtGui import QFont, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QProcess, pyqtSignal, QTimer

class WindowsStyleTerminalSimplified(QDialog):
    """
    Terminal estilo Windows com suporte a comandos Python e interatividade.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa o terminal.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações da janela
        self.setWindowTitle("Terminal")
        self.setGeometry(100, 100, 800, 500)
        self.setModal(False)
        
        # Histórico de comandos
        self.command_history = []
        self.history_index = 0
        
        # Configuração da interface
        self._setup_ui()
        
        # Inicia o processo do terminal
        self._start_process()
    
    def _setup_ui(self):
        """Configura a interface do terminal."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Área de saída
        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0C0C0C;
                color: #CCCCCC;
                border: 1px solid #333333;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.output_area)
        
        # Layout para entrada de comando
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(5)
        
        # Prompt
        self.prompt_label = QLabel(">")
        self.prompt_label.setStyleSheet("QLabel { color: #CCCCCC; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }")
        input_layout.addWidget(self.prompt_label)
        
        # Campo de entrada
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #0C0C0C;
                color: #CCCCCC;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self._send_command)
        input_layout.addWidget(self.input_field)
        
        layout.addLayout(input_layout)
        
        # Configura eventos de teclado para histórico
        self.input_field.installEventFilter(self)
        
        # Estilo da janela
        self.setStyleSheet("""
            QDialog {
                background-color: #0C0C0C;
                color: #CCCCCC;
            }
        """)
    
    def _start_process(self):
        """Inicia o processo do terminal."""
        try:
            # Cria o processo
            self.process = QProcess(self)
            
            # Conecta sinais
            self.process.readyReadStandardOutput.connect(self._handle_stdout)
            self.process.readyReadStandardError.connect(self._handle_stderr)
            self.process.finished.connect(self._handle_finished)
            
            # Configura ambiente
            # Usa systemEnvironment() em vez de setEnvironment()
            env = QProcess.systemEnvironment()
            
            # Inicia o processo
            if sys.platform == 'win32':
                self.process.start('cmd.exe')
                self.output_area.appendPlainText("Terminal Windows iniciado.\n")
            else:
                self.process.start('/bin/bash')
                self.output_area.appendPlainText("Terminal Bash iniciado.\n")
            
            # Verifica se o processo iniciou
            if not self.process.waitForStarted(1000):
                self.output_area.appendPlainText("Erro ao iniciar o terminal.\n")
                # Fallback para execução direta de Python
                self.output_area.appendPlainText("Usando Python interativo como fallback.\n")
                self.output_area.appendPlainText("Python " + sys.version + "\n")
                self.output_area.appendPlainText("Digite comandos Python diretamente.\n\n>>> ")
                self.is_python_mode = True
            else:
                self.is_python_mode = False
        
        except Exception as e:
            self.output_area.appendPlainText(f"Erro ao iniciar o terminal: {str(e)}\n")
            self.output_area.appendPlainText("Usando Python interativo como fallback.\n")
            self.output_area.appendPlainText("Python " + sys.version + "\n")
            self.output_area.appendPlainText("Digite comandos Python diretamente.\n\n>>> ")
            self.is_python_mode = True
    
    def _send_command(self):
        """Envia o comando digitado para o processo."""
        command = self.input_field.text()
        if not command:
            return
        
        # Adiciona ao histórico
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Exibe o comando na área de saída
        if self.is_python_mode:
            self.output_area.appendPlainText(f">>> {command}")
        else:
            self.output_area.appendPlainText(f"> {command}")
        
        # Envia o comando para o processo
        if self.is_python_mode:
            # Executa o comando Python diretamente
            try:
                # Captura a saída
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = stdout_capture = StringCapture()
                sys.stderr = stderr_capture = StringCapture()
                
                try:
                    # Tenta executar como expressão (para mostrar o resultado)
                    result = eval(command, globals())
                    if result is not None:
                        print(repr(result))
                except:
                    # Se falhar, executa como statement
                    exec(command, globals())
                
                # Obtém a saída capturada
                output = stdout_capture.getvalue()
                error = stderr_capture.getvalue()
                
                # Exibe a saída
                if output:
                    self.output_area.appendPlainText(output)
                if error:
                    self.output_area.appendPlainText(f"Erro: {error}")
                
            except Exception as e:
                self.output_area.appendPlainText(f"Erro: {str(e)}")
            
            finally:
                # Restaura stdout e stderr
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
                # Adiciona o prompt para o próximo comando
                self.output_area.appendPlainText(">>> ")
        
        else:
            # Envia para o processo do terminal
            try:
                self.process.write((command + "\n").encode())
            except Exception as e:
                self.output_area.appendPlainText(f"Erro ao enviar comando: {str(e)}")
        
        # Limpa o campo de entrada
        self.input_field.clear()
        
        # Rola para o final
        self.output_area.moveCursor(QTextCursor.End)
    
    def _handle_stdout(self):
        """Manipula a saída padrão do processo."""
        data = self.process.readAllStandardOutput().data().decode(errors='replace')
        self.output_area.appendPlainText(data.rstrip())
        self.output_area.moveCursor(QTextCursor.End)
    
    def _handle_stderr(self):
        """Manipula a saída de erro do processo."""
        data = self.process.readAllStandardError().data().decode(errors='replace')
        self.output_area.appendPlainText(data.rstrip())
        self.output_area.moveCursor(QTextCursor.End)
    
    def _handle_finished(self, exit_code, exit_status):
        """Manipula o término do processo."""
        self.output_area.appendPlainText(f"\nProcesso finalizado com código {exit_code}.")
        self.output_area.moveCursor(QTextCursor.End)
    
    def eventFilter(self, obj, event):
        """Filtra eventos para manipular teclas especiais."""
        if obj is self.input_field and event.type() == event.KeyPress:
            key = event.key()
            
            # Seta para cima: comando anterior
            if key == Qt.Key_Up:
                if self.command_history and self.history_index > 0:
                    self.history_index -= 1
                    self.input_field.setText(self.command_history[self.history_index])
                return True
            
            # Seta para baixo: próximo comando
            elif key == Qt.Key_Down:
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    self.input_field.setText(self.command_history[self.history_index])
                else:
                    self.history_index = len(self.command_history)
                    self.input_field.clear()
                return True
        
        return super().eventFilter(obj, event)
    
    def closeEvent(self, event):
        """Manipula o fechamento da janela."""
        # Finaliza o processo se estiver em execução
        if hasattr(self, 'process') and self.process.state() == QProcess.Running:
            self.process.terminate()
            if not self.process.waitForFinished(1000):
                self.process.kill()
        
        event.accept()

class StringCapture:
    """Classe para capturar saída de texto."""
    
    def __init__(self):
        self.data = []
    
    def write(self, text):
        self.data.append(text)
    
    def getvalue(self):
        return ''.join(self.data)
    
    def flush(self):
        pass
