"""
Módulo para execução de código binário de forma robusta com suporte a entrada de dados.
Esta versão corrige problemas na execução de comandos input() e print().
"""

import os
import sys
import subprocess
import tempfile
import io
import time
import threading
import queue
from contextlib import redirect_stdout, redirect_stderr
from PyQt5.QtWidgets import QInputDialog, QDialog, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel, QApplication
from PyQt5.QtCore import Qt

class BinaryCodeExecutorFixed:
    """
    Executor de código binário com suporte a execução real e interativa.
    """
    
    def __init__(self, interpreter):
        self.interpreter = interpreter
    
    def execute_binary_code(self, binary_code, parent=None):
        """
        Executa código binário traduzindo para Python e executando.
        Se houver input(), solicita ao usuário os valores.
        Exibe a saída simulando um terminal, mostrando os valores digitados.
        """
        try:
            python_code = self.interpreter.traduzir_binario(binary_code)
            python_code, terminal_lines = self._handle_inputs_terminal(python_code, parent)
            return self._show_result_dialog_terminal(self._execute_python_code(python_code), terminal_lines, parent)
        except Exception as e:
            return self._show_result_dialog_terminal(f"Erro ao executar código binário: {str(e)}", [], parent)

    def _handle_inputs_terminal(self, python_code, parent=None):
        """
        Detecta chamadas a input() e solicita ao usuário os valores.
        Retorna o código com inputs substituídos e uma lista de linhas para simular o terminal.
        """
        import re
        pattern = re.compile(r"input\s*\((.*?)\)")
        matches = list(pattern.finditer(python_code))
        if not matches:
            return python_code, []

        new_code = python_code
        offset = 0
        terminal_lines = []
        for match in matches:
            prompt = match.group(1).strip().strip('"').strip("'")
            prompt_display = prompt.replace("\\n", "\n") if prompt else ""
            # Simula prompt do terminal
            prompt_line = f">>>> {prompt_display}: " if prompt_display else ">>>> "
            value, ok = QInputDialog.getText(parent, "Entrada de Dados", prompt_display or "Digite um valor:")
            if not ok:
                value = ""
            # Mostra o que o usuário digitou após o prompt
            terminal_lines.append(f"{prompt_line}{value}")
            # Substitui input(...) pelo valor informado (como string literal)
            value_literal = f'"{value}"'
            start, end = match.start() + offset, match.end() + offset
            new_code = new_code[:start] + value_literal + new_code[end:]
            offset += len(value_literal) - (end - start)
        return new_code, terminal_lines

    def _show_result_dialog_terminal(self, output, terminal_lines, parent=None):
        """
        Exibe o resultado da execução em um QDialog estilizado simulando um terminal.
        """
        dialog = QDialog(parent)
        dialog.setWindowTitle("Terminal de Execução")
        dialog.setMinimumSize(650, 420)
        layout = QVBoxLayout(dialog)
        label = QLabel("<b>Terminal:</b>")
        layout.addWidget(label)
        output_area = QPlainTextEdit()
        output_area.setReadOnly(True)
        # Monta a simulação do terminal
        terminal_text = ""
        if terminal_lines:
            terminal_text += "\n".join(terminal_lines) + "\n\n"
        # Adiciona a saída do programa
        if output.strip():
            # Separa erros da saída normal
            if "\n--- Erros ---\n" in output:
                out, err = output.split("\n--- Erros ---\n", 1)
                if out.strip():
                    # Cada linha de saída também recebe >>>> para simular terminal
                    for line in out.strip().splitlines():
                        terminal_text += f">>>> {line}\n"
                if err.strip():
                    for line in err.strip().splitlines():
                        terminal_text += f">>>> {line}\n"
            else:
                for line in output.strip().splitlines():
                    terminal_text += f">>>> {line}\n"
        output_area.setPlainText(terminal_text.rstrip())
        output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #181a20;
                color: #e6e6e6;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 15px;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        layout.addWidget(output_area)
        btn = QPushButton("Fechar")
        btn.clicked.connect(dialog.accept)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2d8cf0;
                color: #fff;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1c6cb3;
            }
        """)
        layout.addWidget(btn, alignment=Qt.AlignRight)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #23272e;
            }
            QLabel {
                color: #fff;
                font-size: 15px;
            }
        """)
        dialog.exec_()
        return output

    def _execute_python_code(self, python_code):
        """
        Executa código Python de forma segura.
        """
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(python_code)
                temp_path = temp_file.name
            process = subprocess.Popen(
                [sys.executable, temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )
            stdout, stderr = process.communicate(timeout=10)
            output = stdout
            if stderr:
                output += f"\n--- Erros ---\n{stderr}"
            return output
        except subprocess.TimeoutExpired:
            process.kill()
            return "Erro: A execução do código excedeu o tempo limite."
        except Exception as e:
            return f"Erro ao executar o código: {str(e)}"
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
