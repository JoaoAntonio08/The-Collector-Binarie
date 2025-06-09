"""
Módulo para implementação de terminal estilo Windows simplificado.
Versão v7 com logging detalhado e correção de inicialização.
"""

import os
import sys
import subprocess
import io
import traceback
import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPlainTextEdit,
    QLineEdit, QPushButton, QLabel, QSplitter, QApplication
)
from PyQt5.QtGui import QFont, QTextCursor, QIcon
from PyQt5.QtCore import Qt, QProcess, pyqtSignal, QTimer, QProcessEnvironment
from datetime import datetime

# Definição da classe StringCapture
class StringCapture(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, s):
        if isinstance(s, bytes):
            encoding = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
            s = s.decode(encoding, errors="replace")
        super().write(str(s))

class WindowsStyleTerminalSimplified(QDialog):
    """
    Terminal estilo Windows com I/O interativo (v7 - Logging Corrigido).
    """

    def __init__(self, parent=None):
        logging.info("WindowsStyleTerminalSimplified: __init__ chamado")
        super().__init__(parent)

        self.command_history = []
        self.history_index = 0
        self.is_python_mode = False
        self.process = None
        self.partial_output_buffer = ""

        self._setup_ui()
        logging.info("WindowsStyleTerminalSimplified: UI configurada")
        self._start_process()
        logging.info("WindowsStyleTerminalSimplified: Processo do terminal iniciado")
        self._setup_logging()

        logging.info("Inicializando Terminal v7 (Logging Corrigido)")
        self.setWindowTitle("Terminal")
        self.setGeometry(100, 100, 800, 500)
        self.setModal(False)

    def _setup_logging(self):
        """Configura o logging para o arquivo."""
        log_filename = "terminal_raw_output.log"
        # Remove handlers existentes para evitar duplicação se a classe for instanciada múltiplas vezes
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_filename, mode="w", encoding="utf-8"),
                # logging.StreamHandler() # Descomente para ver logs no console também
            ]
        )
        logging.info("Logging configurado.")

    def showEvent(self, event):
        logging.info("WindowsStyleTerminalSimplified: showEvent chamado (tela aberta)")
        super().showEvent(event)

    def closeEvent(self, event):
        logging.info("WindowsStyleTerminalSimplified: closeEvent chamado (tela fechada)")
        if self.process and self.process.state() == QProcess.Running:
            logging.debug("Matando processo do terminal...")
            self.process.kill()
            self.process.waitForFinished(1000)
            logging.debug("Processo do terminal finalizado.")
        event.accept()

    def _setup_ui(self):
        logging.debug("Configurando UI do terminal")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        self.output_area = QPlainTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #181a20;
                color: #e6e6e6;
                border: 1px solid #282a36;
                font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace;
                font-size: 16px;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        layout.addWidget(self.output_area)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(5)

        self.prompt_label = QLabel(">")
        self.prompt_label.setStyleSheet("QLabel { color: #bd93f9; font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace; font-size: 16px; }")
        input_layout.addWidget(self.prompt_label)

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #23272e;
                color: #e6e6e6;
                border: 1px solid #282a36;
                font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace;
                font-size: 16px;
                border-radius: 10px;
                padding: 8px 14px;
            }
        """)
        self.input_field.returnPressed.connect(self._send_command)
        input_layout.addWidget(self.input_field)

        layout.addLayout(input_layout)
        self.input_field.installEventFilter(self)
        self.setStyleSheet("QDialog { background-color: #23272e; color: #e6e6e6; border-radius: 14px; }")
        logging.debug("UI do terminal configurada")

    def _start_process(self):
        logging.info("Tentando iniciar processo do terminal...")
        if self.process and self.process.state() == QProcess.Running:
            logging.warning("Processo já estava em execução.")
            return

        try:
            self.process = QProcess(self)
            self.process.readyReadStandardOutput.connect(self._handle_stdout)
            self.process.readyReadStandardError.connect(self._handle_stderr)
            self.process.finished.connect(self._handle_process_finished)

            env = QProcessEnvironment.systemEnvironment()
            self.process.setProcessEnvironment(env)
            logging.debug(f"Ambiente do processo definido.")

            if sys.platform == "win32":
                executable = "cmd.exe"
                self.process.start(executable)
                prompt = "Terminal Windows iniciado."
            else:
                executable = "/bin/bash"
                try:
                    self.process.start(executable)
                    prompt = "Terminal Bash iniciado."
                except Exception:
                    executable = "/bin/sh"
                    self.process.start(executable)
                    prompt = "Terminal Shell iniciado."
            logging.info(f"Executável do terminal: {executable}")

            if not self.process.waitForStarted(3000):
                error_msg = self.process.errorString()
                logging.error(f"Erro ao iniciar o terminal: {error_msg}")
                self.output_area.appendPlainText(f"Erro ao iniciar o terminal: {error_msg}\n")
                self._fallback_to_python_mode()
            else:
                logging.info("Processo do terminal iniciado com sucesso.")
                self.output_area.appendPlainText(prompt + "\n")
                self.is_python_mode = False
                self.prompt_label.setText(">")
                self._append_prompt()

        except Exception as e:
            logging.exception("Exceção ao iniciar o terminal")
            self.output_area.appendPlainText(f"Exceção ao iniciar o terminal: {str(e)}\n")
            self._fallback_to_python_mode()

    def _fallback_to_python_mode(self):
        logging.warning("Falha ao iniciar terminal, usando modo Python interativo.")
        self.output_area.appendPlainText("Usando Python interativo como fallback.\n")
        self.output_area.appendPlainText(f"Python {sys.version}\n")
        self.output_area.appendPlainText("Digite comandos Python diretamente.\n")
        self.is_python_mode = True
        self.prompt_label.setText(">>>")
        self._append_prompt()

    def _send_command(self):
        logging.info("WindowsStyleTerminalSimplified: _send_command chamado")
        command = self.input_field.text().strip()
        logging.info(f"Comando recebido do usuário: {repr(command)}")
        if not command:
            return

        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = len(self.command_history)

        prompt = ">>>" if self.is_python_mode else ">"
        self.input_field.clear()

        if self.is_python_mode:
            logging.debug("Executando comando no modo Python interativo")
            self.output_area.appendPlainText(f"{prompt} {command}")
            self.output_area.appendPlainText("")
            QApplication.processEvents()
            if command.lower() in ["clear", "cls"]:
                self.clear_terminal()
            elif command.startswith("pip install"):
                self._run_pip_install(command)
            else:
                self._execute_python_command(command)
        else:
            logging.debug("Enviando comando para o processo do terminal")
            if self.process and self.process.state() == QProcess.Running:
                try:
                    encoding = sys.getdefaultencoding() or "utf-8"
                    encoded_command = (command + "\n").encode(encoding, errors="replace")
                    logging.debug(f"Enviando bytes: {repr(encoded_command)}")
                    self.process.write(encoded_command)
                    self.process.write((command + "\n").encode(encoding, errors="replace"))
                except Exception as e:
                    logging.exception("Erro ao enviar comando para o terminal")
                    self.output_area.appendPlainText(f"Erro ao enviar comando para o terminal: {str(e)}")
            else:
                logging.error("Tentativa de enviar comando, mas processo não está em execução.")
                self.output_area.appendPlainText("Erro: Processo do terminal não está em execução.")
                self._start_process()

    def _run_pip_install(self, command):
        logging.info(f"Executando pip install: {command}")
        self.output_area.appendPlainText(f"Executando: {command}")
        self.output_area.appendPlainText("")
        self.output_area.moveCursor(QTextCursor.End)
        QApplication.processEvents()

        try:
            pip_command = [sys.executable, "-m"] + command.split()
            result = subprocess.run(pip_command, capture_output=True, text=True, check=False, encoding="utf-8", errors="replace")
            logging.debug(f"Resultado pip (stdout): {result.stdout}")
            logging.debug(f"Resultado pip (stderr): {result.stderr}")
            logging.debug(f"Resultado pip (returncode): {result.returncode}")

            if result.stdout:
                self.output_area.appendPlainText(result.stdout.strip())
                self.output_area.appendPlainText("")
            if result.stderr:
                self.output_area.appendPlainText(f"Saída de erro pip:\n{result.stderr.strip()}")
                self.output_area.appendPlainText("")
                self.output_area.appendPlainText(
                f"Instalação {'concluída' if result.returncode == 0 else 'falhou'} (código: {result.returncode})."
                )
                self.output_area.appendPlainText("")

        except FileNotFoundError:
             logging.error(f"Erro pip: Executável Python '{sys.executable}' ou 'pip' não encontrado.")
             self.output_area.appendPlainText(f"Erro: O executável Python '{sys.executable}' ou o módulo 'pip' não foi encontrado.")
             self.output_area.appendPlainText("")
        except Exception as e:
            logging.exception("Erro ao executar pip install")
            self.output_area.appendPlainText(f"Erro ao executar pip install: {str(e)}")
            self.output_area.appendPlainText("")
        finally:
            self._append_prompt()

    def _execute_python_command(self, command):
        logging.info(f"Executando comando Python interativo: {command}")
        old_stdout, old_stderr = sys.stdout, sys.stderr
        redirected_stdout, redirected_stderr = StringCapture(), StringCapture()
        sys.stdout, sys.stderr = redirected_stdout, redirected_stderr
        try:
            try:
                code = compile(command, "<stdin>", "eval")
                result = eval(code, globals())
                if result is not None: print(repr(result))
            except SyntaxError:
                code = compile(command, "<stdin>", "exec")
                exec(code, globals())
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
            output, error = redirected_stdout.getvalue(), redirected_stderr.getvalue()
            logging.debug(f"Python stdout: {repr(output)}")
            logging.debug(f"Python stderr: {repr(error)}")
            if output:
                self.output_area.appendPlainText(output.rstrip())
                self.output_area.appendPlainText("")
            if error:
                self.output_area.appendPlainText(error.rstrip())
                self.output_area.appendPlainText("")
            self._append_prompt()

    def _process_output_data(self, data_bytes, source="stdout"):
        logging.debug(f"_process_output_data chamado para {source}")
        """Decodifica e LOGA dados brutos, depois tenta exibir de forma simples."""
        if not data_bytes:
            return

        try:
            # Tenta decodificar com o encoding do sistema, fallback para utf-8
            try:
                locale_encoding = sys.getfilesystemencoding() or "utf-8"
                data = data_bytes.data().decode(locale_encoding, errors="replace")
            except Exception:
                data = data_bytes.data().decode("utf-8", errors="replace")

            # *** LOGGING DA SAÍDA BRUTA ***
            logging.debug(f"RAW {source.upper()}: {repr(data)}")

            # Exibição simples: apenas adiciona o que foi recebido
            self.output_area.insertPlainText(data)
            self.output_area.moveCursor(QTextCursor.End)
            QApplication.processEvents()

        except Exception as e:
            logging.exception(f"Erro ao processar dados de {source}")

    def _handle_stdout(self):
        logging.debug("Recebido readyReadStandardOutput")
        if not self.process: return
        data_bytes = self.process.readAllStandardOutput()
        self._process_output_data(data_bytes, source="stdout")

    def _handle_stderr(self):
        logging.debug("Recebido readyReadStandardError")
        if not self.process: return
        data_bytes = self.process.readAllStandardError()
        self._process_output_data(data_bytes, source="stderr")

    def _handle_process_finished(self, exit_code, exit_status):
        logging.info(f"Processo do terminal finalizado. Código: {exit_code}, Status: {exit_status}")
        status_map = {QProcess.NormalExit: "normalmente", QProcess.CrashExit: "com erro"}
        status_text = status_map.get(exit_status, "inesperadamente")
        self.output_area.appendPlainText(f"\nProcesso do terminal finalizado {status_text} (código: {exit_code}).")
        self._append_prompt()

    def _append_prompt(self):
        logging.debug("Adicionando prompt ao final")
        current_text = self.output_area.toPlainText()
        if current_text and not current_text.endswith("\n"):
            self.output_area.appendPlainText("")

        prompt = (">>> " if self.is_python_mode else "> ")
        self.output_area.appendPlainText(prompt.strip())
        self.output_area.moveCursor(QTextCursor.End)
        self.input_field.setFocus()

    def eventFilter(self, obj, event):
        logging.debug(f"eventFilter chamado: obj={obj}, event={event}")
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

    def clear_terminal(self):
        logging.info("Limpando terminal")
        self.output_area.clear()
        if self.is_python_mode:
            self.output_area.appendPlainText(f"Terminal limpo. Python {sys.version}\n")
        else:
            prompt_text = "Terminal Windows limpo." if sys.platform == "win32" else "Terminal Bash/Shell limpo."
            self.output_area.appendPlainText(prompt_text + "\n")
        self._append_prompt()

    def execute_python_script(self, script_path):
        logging.info(f"Executando script Python: {script_path}")
        self.clear_terminal()

        if not self.process or self.process.state() != QProcess.Running:
            logging.warning("Processo do terminal não ativo ao tentar executar script. Tentando iniciar...")
            self.output_area.appendPlainText("Erro: Processo do terminal não está ativo. Tentando iniciar...")
            self.output_area.appendPlainText("")
            self._start_process()
            if not self.process or not self.process.waitForStarted(1500):
                logging.error("Falha ao iniciar processo do terminal para execução do script.")
                self.output_area.appendPlainText("Falha ao iniciar o processo do terminal para execução do script.")
                self.output_area.appendPlainText("")
                self._append_prompt()
                return
            logging.info("Processo do terminal iniciado para execução do script.")
            self.output_area.appendPlainText("Processo do terminal iniciado. Executando script...")
            self.output_area.appendPlainText("")

        python_executable = sys.executable
        if not python_executable:
             logging.error("Não foi possível determinar o caminho do executável Python.")
             self.output_area.appendPlainText("Erro: Não foi possível determinar o caminho do executável Python.")
             self.output_area.appendPlainText("")
             self._append_prompt()
             return

        normalized_script_path = os.path.normpath(script_path)
        command_to_run = f'"{python_executable}" -u "{normalized_script_path}"'
        logging.info(f"Comando de execução a ser enviado: {command_to_run}")
        self.output_area.appendPlainText(f"> Executando: {command_to_run}")
        self.output_area.appendPlainText("") # Linha em branco após "Executando"
        self.output_area.moveCursor(QTextCursor.End)
        QApplication.processEvents()

        try:
            encoding = sys.getdefaultencoding() or "utf-8"
            encoded_command = (command_to_run + "\n").encode(encoding, errors="replace")
            logging.debug(f"Enviando bytes para execução: {repr(encoded_command)}")
            bytes_written = self.process.write(encoded_command)
            bytes_written = self.process.write((command_to_run + "\n").encode(encoding, errors="replace"))
            if bytes_written == -1:
                logging.error("Falha ao escrever comando de execução no processo do terminal.")
                self.output_area.appendPlainText("Erro: Falha ao escrever comando no processo do terminal.")
                self.output_area.appendPlainText("")
                self._append_prompt()
                return
            logging.debug(f"Bytes escritos para execução: {bytes_written}")
        except Exception as e:
            logging.exception("Erro ao enviar comando de execução para o terminal")
            self.output_area.appendPlainText(f"Erro ao enviar comando de execução para o terminal: {str(e)}")
            self.output_area.appendPlainText("")
            self._append_prompt()

if __name__ == "__main__":
    logging.info("Iniciando QApplication principal do terminal")
    app = QApplication(sys.argv)
    terminal = WindowsStyleTerminalSimplified()
    terminal.show()
    logging.info("Terminal principal exibido")
    sys.exit(app.exec_())

