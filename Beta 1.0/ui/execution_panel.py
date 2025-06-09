"""
Módulo para integrar o interpretador binário ao botão de execução da interface gráfica.
Este módulo estende a funcionalidade do botão de execução para suportar a execução
direta de código binário, com feedback visual e tratamento de erros.
"""

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, 
    QProgressBar, QMessageBox, QToolButton, QMenu, QAction
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from binary_runner_enhanced import BinaryRunner
from terminal_enhanced import TerminalEnhanced

class ExecutionPanel(QWidget):
    """
    Painel de execução com botão integrado para executar código binário.
    """
    
    # Sinais para comunicação com outros componentes
    execution_started = pyqtSignal()
    execution_finished = pyqtSignal(str)
    execution_error = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Inicializa o executor de código binário
        self.runner = BinaryRunner()
        
        # Configura a interface
        self._setup_ui()
        
        # Estado de execução
        self.is_executing = False
        
    def _setup_ui(self):
        """Configura a interface do painel de execução."""
        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Botão de execução com menu dropdown
        self.run_button = QToolButton(self)
        self.run_button.setText("Executar")
        self.run_button.setToolTip("Executar código (F5)")
        self.run_button.setPopupMode(QToolButton.MenuButtonPopup)
        self.run_button.setStyleSheet("""
            QToolButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #6afa96;
            }
            QToolButton:pressed {
                background-color: #3fa65b;
            }
            QToolButton::menu-button {
                border: none;
                width: 16px;
            }
        """)
        
        # Menu de opções de execução
        run_menu = QMenu(self.run_button)
        
        # Ação: Executar como Python
        self.action_run_python = QAction("Executar como Python", self)
        self.action_run_python.triggered.connect(lambda: self.execute_code(as_binary=False))
        run_menu.addAction(self.action_run_python)
        
        # Ação: Executar como Binário
        self.action_run_binary = QAction("Executar como Binário", self)
        self.action_run_binary.triggered.connect(lambda: self.execute_code(as_binary=True))
        run_menu.addAction(self.action_run_binary)
        
        # Ação: Traduzir Binário → Python
        self.action_translate = QAction("Traduzir Binário → Python", self)
        self.action_translate.triggered.connect(self.translate_binary)
        run_menu.addAction(self.action_translate)
        
        # Configura o menu no botão
        self.run_button.setMenu(run_menu)
        self.run_button.clicked.connect(self.execute_code)
        
        # Barra de progresso para indicar execução
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #44475a;
                color: #f8f8f2;
                border: none;
                border-radius: 2px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #bd93f9;
                border-radius: 2px;
            }
        """)
        
        # Label para status
        self.status_label = QLabel("Pronto", self)
        self.status_label.setStyleSheet("color: #f8f8f2;")
        
        # Adiciona widgets ao layout
        layout.addWidget(self.run_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label, 1)  # 1 = stretch factor
        
        # Timer para animação durante execução
        self.execution_timer = QTimer(self)
        self.execution_timer.timeout.connect(self._update_execution_animation)
        
        # Contador para animação
        self.animation_counter = 0
        
    def execute_code(self, checked=False, as_binary=True):
        """
        Executa o código atual, interpretando-o como binário ou Python conforme especificado.
        
        Args:
            checked: Parâmetro ignorado (usado pelo sistema de sinais do Qt)
            as_binary: Se True, interpreta o código como binário; caso contrário, como Python
        """
        if self.is_executing:
            return
        
        # Obtém o código do editor atual
        code = self._get_current_code()
        if not code:
            self.status_label.setText("Nenhum código para executar")
            return
        
        # Inicia a execução
        self.is_executing = True
        self.execution_started.emit()
        
        # Atualiza a interface
        self.progress_bar.setVisible(True)
        self.status_label.setText("Executando...")
        self.run_button.setEnabled(False)
        
        # Inicia a animação
        self.execution_timer.start(100)
        
        # Executa o código em um timer para não bloquear a interface
        QTimer.singleShot(100, lambda: self._perform_execution(code, as_binary))
    
    def _perform_execution(self, code, as_binary):
        """
        Realiza a execução do código e atualiza a interface.
        
        Args:
            code: Código a ser executado
            as_binary: Se True, interpreta o código como binário; caso contrário, como Python
        """
        try:
            # Executa o código
            if as_binary:
                result = self.runner.executar_binario(code)
            else:
                result = self.runner.executar_codigo(code)
            
            # Exibe o resultado no terminal
            self._show_terminal(result)
            
            # Emite sinal de conclusão
            self.execution_finished.emit(result)
            
        except Exception as e:
            # Em caso de erro, exibe mensagem
            error_msg = f"Erro durante a execução: {str(e)}"
            self.status_label.setText(error_msg)
            self.execution_error.emit(error_msg)
            
            # Exibe o erro no terminal
            self._show_terminal(error_msg)
            
        finally:
            # Finaliza a execução
            self.is_executing = False
            self.progress_bar.setVisible(False)
            self.run_button.setEnabled(True)
            self.execution_timer.stop()
            self.status_label.setText("Pronto")
    
    def translate_binary(self):
        """
        Traduz o código binário atual para Python e exibe em uma nova aba.
        """
        # Obtém o código do editor atual
        code = self._get_current_code()
        if not code:
            self.status_label.setText("Nenhum código para traduzir")
            return
        
        try:
            # Traduz o código binário para Python
            translated = self.runner.interpretar(code)
            
            # Emite sinal para criar uma nova aba com o código traduzido
            self.execution_finished.emit(translated)
            
            # Atualiza o status
            self.status_label.setText("Tradução concluída")
            
        except Exception as e:
            # Em caso de erro, exibe mensagem
            error_msg = f"Erro durante a tradução: {str(e)}"
            self.status_label.setText(error_msg)
            self.execution_error.emit(error_msg)
    
    def _get_current_code(self):
        """
        Obtém o código do editor atual.
        
        Returns:
            String contendo o código ou None se não houver editor atual
        """
        # Esta função deve ser implementada pela classe que utiliza o ExecutionPanel
        # Aqui apenas definimos a interface
        return None
    
    def _show_terminal(self, output):
        """
        Exibe o terminal com a saída da execução.
        
        Args:
            output: String contendo a saída da execução
        """
        terminal = TerminalEnhanced(output, self)
        terminal.exec_()
    
    def _update_execution_animation(self):
        """Atualiza a animação durante a execução."""
        self.animation_counter += 1
        dots = "." * (self.animation_counter % 4)
        self.status_label.setText(f"Executando{dots}")
    
    def set_get_code_callback(self, callback):
        """
        Define a função de callback para obter o código do editor atual.
        
        Args:
            callback: Função que retorna o código do editor atual
        """
        self._get_current_code = callback
