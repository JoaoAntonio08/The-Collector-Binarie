"""
Módulo para implementação de terminal estilo Windows simplificado.
Versão final com correção de ambiente e ajuste para I/O interativo.
"""

import os
import sys
import subprocess
import io
import traceback
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QLineEdit, QPushButton, QLabel, QSplitter, QApplication
)
from PyQt5.QtGui import QFont, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QProcess, pyqtSignal, QTimer, QProcessEnvironment

# Definição da classe StringCapture
class StringCapture(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, s):
        if isinstance(s, bytes):
            encoding = getattr(sys.stdout, 'encoding', 'utf-8') or 'utf-8'
            s = s.decode(encoding, errors='replace')
        super().write(str(s))

class WindowsStyleTerminalSimplified(QDialog):
    """
    Terminal estilo Windows com I/O interativo ajustado.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Terminal")
        self.setGeometry(100, 100, 800, 500)
        self.setModal(False)

        self.command_history = []
        self.history_index = 0
        self.is_python_mode = False
        self.process = None

        self._setup_ui()
        self._start_process()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

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

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(5)

        self.prompt_label = QLabel(">")
        self.prompt_label.setStyleSheet("QLabel { color: #CCCCCC; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }")
        input_layout.addWidget(self.prompt_label)

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
        self.input_field.installEventFilter(self)
        self.setStyleSheet("QDialog { background-color: #0C0C0C; color: #CCCCCC; }")

    def _start_process(self):
        if self.process and self.process.state() == QProcess.Running:
            return

        try:
            self.process = QProcess(self)
            self.process.readyReadStandardOutput.connect(self._handle_stdout)
            self.process.readyReadStandardError.connect(self._handle_stderr)
            self.process.finished.connect(self._handle_process_finished)

            env = QProcessEnvironment.systemEnvironment()
            self.process.setProcessEnvironment(env)

            if sys.platform == 'win32':
                executable = 'cmd.exe'
                self.process.start(executable)
                prompt = "Terminal Windows iniciado."
            else:
                executable = '/bin/bash'
                try:
                    self.process.start(executable)
                    prompt = "Terminal Bash iniciado."
                except Exception:
                    executable = '/bin/sh'
                    self.process.start(executable)
                    prompt = "Terminal Shell iniciado."

            if not self.process.waitForStarted(3000):
                error_msg = self.process.errorString()
                self.output_area.appendPlainText(f"Erro ao iniciar o terminal: {error_msg}\n")
                self._fallback_to_python_mode()
            else:
                self.output_area.appendPlainText(prompt + "\n")
                self.is_python_mode = False
                self.prompt_label.setText(">")
                self._append_prompt()

        except Exception as e:
            self.output_area.appendPlainText(f"Exceção ao iniciar o terminal: {str(e)}\n")
            self._fallback_to_python_mode()

    def _fallback_to_python_mode(self):
        self.output_area.appendPlainText("Usando Python interativo como fallback.\n")
        self.output_area.appendPlainText(f"Python {sys.version}\n")
        self.output_area.appendPlainText("Digite comandos Python diretamente.\n")
        self.is_python_mode = True
        self.prompt_label.setText(">>>")
        self._append_prompt()

    def _send_command(self):
        command = self.input_field.text().strip()
        if not command:
            return

        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = len(self.command_history)

        prompt = ">>>" if self.is_python_mode else ">"
        self.output_area.appendPlainText(f"{prompt} {command}")
        self.input_field.clear()

        if self.is_python_mode:
            if command.lower() in ['clear', 'cls']:
                self.clear_terminal()
            elif command.startswith("pip install"):
                self._run_pip_install(command)
            else:
                self._execute_python_command(command)
        else:
            if self.process and self.process.state() == QProcess.Running:
                try:
                    encoding = sys.getdefaultencoding() or 'utf-8'
                    self.process.write((command + "\n").encode(encoding, errors='replace'))
                except Exception as e:
                    self.output_area.appendPlainText(f"Erro ao enviar comando para o terminal: {str(e)}")
            else:
                self.output_area.appendPlainText("Erro: Processo do terminal não está em execução.")
                self._start_process()

        QTimer.singleShot(50, lambda: self.output_area.moveCursor(QTextCursor.End))

    def _run_pip_install(self, command):
        self.output_area.appendPlainText(f"Executando: {command}")
        self.output_area.moveCursor(QTextCursor.End)
        QApplication.processEvents()

        try:
            pip_command = [sys.executable, "-m"] + command.split()
            result = subprocess.run(pip_command, capture_output=True, text=True, check=False, encoding='utf-8', errors='replace')

            if result.stdout:
                self.output_area.appendPlainText(result.stdout.strip())
            if result.stderr:
                self.output_area.appendPlainText(f"Saída de erro pip:\n{result.stderr.strip()}")
            self.output_area.appendPlainText(f"Instalação {'concluída' if result.returncode == 0 else 'falhou'} (código: {result.returncode}).")

        except FileNotFoundError:
             self.output_area.appendPlainText(f"Erro: O executável Python '{sys.executable}' ou o módulo 'pip' não foi encontrado.")
        except Exception as e:
            self.output_area.appendPlainText(f"Erro ao executar pip install: {str(e)}")
        finally:
            self._append_prompt()

    def _execute_python_command(self, command):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        redirected_stdout, redirected_stderr = StringCapture(), StringCapture()
        sys.stdout, sys.stderr = redirected_stdout, redirected_stderr
        try:
            try:
                code = compile(command, '<stdin>', 'eval')
                result = eval(code, globals())
                if result is not None: print(repr(result))
            except SyntaxError:
                code = compile(command, '<stdin>', 'exec')
                exec(code, globals())
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
            output, error = redirected_stdout.getvalue(), redirected_stderr.getvalue()
            if output: self.output_area.appendPlainText(output.rstrip())
            if error: self.output_area.appendPlainText(error.rstrip())
            self._append_prompt()

    def _handle_stdout(self):
        if not self.process: return
        try:
            data_bytes = self.process.readAllStandardOutput()
            if data_bytes:
                try:
                    locale_encoding = sys.getfilesystemencoding() or 'utf-8'
                    data = data_bytes.data().decode(locale_encoding, errors='replace')
                except Exception:
                    data = data_bytes.data().decode('utf-8', errors='replace')
                self.output_area.insertPlainText(data)
                self.output_area.moveCursor(QTextCursor.End)
        except Exception as e:
             pass # Evita poluir o log

    def _handle_stderr(self):
        if not self.process: return
        try:
            data_bytes = self.process.readAllStandardError()
            if data_bytes:
                try:
                    locale_encoding = sys.getfilesystemencoding() or 'utf-8'
                    data = data_bytes.data().decode(locale_encoding, errors='replace')
                except Exception:
                    data = data_bytes.data().decode('utf-8', errors='replace')
                self.output_area.insertPlainText(data)
                self.output_area.moveCursor(QTextCursor.End)
        except Exception as e:
             pass # Evita poluir o log

    def _handle_process_finished(self, exit_code, exit_status):
        status_map = {QProcess.NormalExit: "normalmente", QProcess.CrashExit: "com erro"}
        status_text = status_map.get(exit_status, "inesperadamente")
        self.output_area.appendPlainText(f"\nProcesso do terminal finalizado {status_text} (código: {exit_code}).")
        self._append_prompt()

    def _append_prompt(self):
        current_text = self.output_area.toPlainText()
        prompt = (">>> " if self.is_python_mode else "> ")
        if not current_text.endswith(prompt) and (not current_text or current_text.endswith('\n')):
             self.output_area.appendPlainText(prompt.strip())
        self.output_area.moveCursor(QTextCursor.End)
        self.input_field.setFocus()

    def eventFilter(self, obj, event):
        if obj is self.input_field and event.type() == event.KeyPress:
            key = event.key()
            if key == Qt.Key_Up:
                if self.command_history and self.history_index > 0:
                    self.history_index -= 1
                    self.input_field.setText(self.command_history[self.history_index])
                    self.input_field.selectAll()
                return True
            elif key == Qt.Key_Down:
                if self.history_index < len(self.command_history):
                    self.history_index += 1
                    if self.history_index == len(self.command_history):
                        self.input_field.clear()
                    else:
                        self.input_field.setText(self.command_history[self.history_index])
                        self.input_field.selectAll()
                return True
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.process.waitForFinished(1000)
        event.accept()

    def clear_terminal(self):
        self.output_area.clear()
        if self.is_python_mode:
            self.output_area.appendPlainText(f"Terminal limpo. Python {sys.version}\n")
        else:
            prompt_text = "Terminal Windows limpo." if sys.platform == 'win32' else "Terminal Bash/Shell limpo."
            self.output_area.appendPlainText(prompt_text + "\n")
        self._append_prompt()

    def execute_python_script(self, script_path):
        self.clear_terminal()

        if not self.process or self.process.state() != QProcess.Running:
            self.output_area.appendPlainText("Erro: Processo do terminal não está ativo. Tentando iniciar...")
            self._start_process()
            if not self.process or not self.process.waitForStarted(1500):
                self.output_area.appendPlainText("Falha ao iniciar o processo do terminal para execução do script.")
                self._append_prompt()
                return
            self.output_area.appendPlainText("Processo do terminal iniciado. Executando script...")

        python_executable = sys.executable
        if not python_executable:
             self.output_area.appendPlainText("Erro: Não foi possível determinar o caminho do executável Python.")
             self._append_prompt()
             return

        normalized_script_path = os.path.normpath(script_path)
        # AJUSTE: Adiciona o flag -u para forçar saída sem buffer
        command_to_run = f'"{python_executable}" -u "{normalized_script_path}"'
        self.output_area.appendPlainText(f"> Executando: {command_to_run}")
        self.output_area.moveCursor(QTextCursor.End)
        QApplication.processEvents()

        try:
            encoding = sys.getdefaultencoding() or 'utf-8'
            bytes_written = self.process.write((command_to_run + "\n").encode(encoding, errors='replace'))
            if bytes_written == -1:
                self.output_area.appendPlainText("Erro: Falha ao escrever comando no processo do terminal.")
                self._append_prompt()
                return
        except Exception as e:
            self.output_area.appendPlainText(f"Erro ao enviar comando de execução para o terminal: {str(e)}")
            self._append_prompt()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    terminal = WindowsStyleTerminalSimplified()
    terminal.show()
    sys.exit(app.exec_())

