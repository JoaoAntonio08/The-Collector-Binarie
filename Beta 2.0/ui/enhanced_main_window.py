"""
Script para integrar todas as melhorias implementadas e testar a experiência completa do usuário.
Este script cria uma versão aprimorada da janela principal com todas as novas funcionalidades.
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox,
    QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QWidget, QSplitter,
    QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer

# Importa os módulos aprimorados
from binary_syntax_parser import BinarySyntaxParser
from binario_interpreter_enhanced import BinarioInterpreterEnhanced
from binary_runner_enhanced import BinaryRunner
from terminal_enhanced import TerminalEnhanced
from execution_panel import ExecutionPanel
from code_validation import CodeValidationWidget
from temp_file_manager import TempFileManager

# Importa os módulos originais necessários
from ui.code_editor import CodeEditor
from syntax_highlighter_enhanced import BinarySyntaxHighlighterEnhanced

class EnhancedMainWindow(QMainWindow):
    """
    Janela principal aprimorada com todas as novas funcionalidades.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configurações básicas
        self.setWindowTitle("The Collector Binarie - Enhanced")
        self.setGeometry(100, 100, 1200, 800)
        
        # Inicializa componentes
        self.binario_interpreter = BinarioInterpreterEnhanced()
        self.binary_runner = BinaryRunner()
        self.temp_manager = TempFileManager()
        
        # Cria uma nova sessão para arquivos temporários
        self.session_id = self.temp_manager.create_session()
        
        # Configuração da interface
        self._setup_ui()
        
        # Configura o timer de salvamento automático
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self._autosave)
        self.autosave_timer.start(60000)  # 60 segundos
        
        # Verifica se há sessões para recuperar
        self._check_recoverable_sessions()
    
    def _setup_ui(self):
        """Configura a interface do usuário."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Painel de execução
        self.execution_panel = ExecutionPanel()
        self.execution_panel.set_get_code_callback(self._get_current_code)
        
        # Abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        
        # Conecta o sinal de mudança de aba
        self.tabs.currentChanged.connect(self._on_tab_changed)
        
        # Adiciona widgets ao layout principal
        main_layout.addWidget(self.execution_panel)
        main_layout.addWidget(self.tabs)
        
        # Barra de status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
        # Cria os menus
        self._create_menus()
        
        # Aplica o estilo escuro
        self._apply_dark_theme()
        
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            self._show_welcome_screen()
        else:
            self._new_tab()
    
    def _create_menus(self):
        """Cria os menus da aplicação."""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        new_file_action = QAction("Novo Arquivo", self)
        new_file_action.setShortcut("Ctrl+N")
        new_file_action.triggered.connect(self._new_tab)
        file_menu.addAction(new_file_action)
        
        open_file_action = QAction("Abrir Arquivo", self)
        open_file_action.setShortcut("Ctrl+O")
        open_file_action.triggered.connect(self._open_file)
        file_menu.addAction(open_file_action)
        
        file_menu.addSeparator()
        
        save_action = QAction("Salvar", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Salvar Como", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(lambda: self._save_file(as_new=True))
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Sair", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Editar
        edit_menu = menubar.addMenu("Editar")
        
        undo_action = QAction("Desfazer", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Refazer", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Recortar", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self._cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copiar", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self._copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Colar", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self._paste)
        edit_menu.addAction(paste_action)
        
        # Menu Tradução
        translate_menu = menubar.addMenu("Tradução")
        
        text_to_binary_action = QAction("Texto → Binário", self)
        text_to_binary_action.triggered.connect(self._text_to_binary)
        translate_menu.addAction(text_to_binary_action)
        
        binary_to_text_action = QAction("Binário → Texto", self)
        binary_to_text_action.triggered.connect(self._binary_to_text)
        translate_menu.addAction(binary_to_text_action)
        
        # Menu Execução
        exec_menu = menubar.addMenu("Execução")
        
        run_action = QAction("Executar", self)
        run_action.setShortcut("F5")
        run_action.triggered.connect(lambda: self.execution_panel.execute_code(as_binary=True))
        exec_menu.addAction(run_action)
        
        run_as_python_action = QAction("Executar como Python", self)
        run_as_python_action.setShortcut("Shift+F5")
        run_as_python_action.triggered.connect(lambda: self.execution_panel.execute_code(as_binary=False))
        exec_menu.addAction(run_as_python_action)
        
        exec_menu.addSeparator()
        
        terminal_action = QAction("Abrir Terminal", self)
        terminal_action.triggered.connect(self._open_terminal)
        exec_menu.addAction(terminal_action)
    
    def _apply_dark_theme(self):
        """Aplica o tema escuro à interface."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #282a36;
                color: #f8f8f2;
            }
            QMenuBar {
                background-color: #21222c;
                color: #f8f8f2;
            }
            QMenuBar::item:selected {
                background-color: #44475a;
            }
            QMenu {
                background-color: #21222c;
                color: #f8f8f2;
            }
            QMenu::item:selected {
                background-color: #44475a;
            }
            QPlainTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                selection-background-color: #44475a;
                font-family: Consolas;
                font-size: 14px;
            }
            QStatusBar {
                background-color: #21222c;
                color: #f8f8f2;
            }
            QWidget {
                background-color: #282a36;
                color: #f8f8f2;
            }
            QTabBar::tab {
                background: #2e2e3a;
                color: white;
                padding: 5px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #44445a;
                border-bottom: 2px solid #bd93f9;
            }
            QTabBar::tab:hover {
                background: #3a3a4a;
            }
            QTabWidget::pane {
                border: 1px solid #44475a;
            }
            QSplitter::handle {
                background-color: #44475a;
            }
            QLabel {
                color: #f8f8f2;
            }
        """)
    
    def _show_welcome_screen(self):
        """Exibe a tela de boas-vindas quando não há abas abertas."""
        # Cria um widget para a tela de boas-vindas
        welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(welcome_widget)
        
        # Carrega a logo
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            welcome_layout.addWidget(logo_label)
        
        # Título
        title_label = QLabel("Bem-vindo ao The Collector Binarie")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #bd93f9;")
        title_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(title_label)
        
        # Descrição
        desc_label = QLabel("Editor e interpretador de código binário")
        desc_label.setStyleSheet("font-size: 16px; color: #f8f8f2;")
        desc_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(desc_label)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # Botão Novo Arquivo
        new_file_button = QPushButton("Novo Arquivo")
        new_file_button.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                color: #282a36;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6afa96;
            }
        """)
        new_file_button.clicked.connect(self._new_tab)
        buttons_layout.addWidget(new_file_button)
        
        # Botão Abrir Arquivo
        open_file_button = QPushButton("Abrir Arquivo")
        open_file_button.setStyleSheet("""
            QPushButton {
                background-color: #bd93f9;
                color: #282a36;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #caa9fa;
            }
        """)
        open_file_button.clicked.connect(self._open_file)
        buttons_layout.addWidget(open_file_button)
        
        welcome_layout.addLayout(buttons_layout)
        welcome_layout.addStretch()
        
        # Adiciona o widget de boas-vindas como aba
        self.tabs.addTab(welcome_widget, "Início")
    
    def _new_tab(self, content="", title="Sem título"):
        """
        Cria uma nova aba com um editor de código.
        
        Args:
            content: Conteúdo inicial do editor
            title: Título da aba
        """
        # Remove a tela de boas-vindas se for a única aba
        if self.tabs.count() == 1 and self.tabs.tabText(0) == "Início":
            self.tabs.removeTab(0)
        
        # Cria um novo editor
        editor = CodeEditor()
        
        # Configura o realce de sintaxe aprimorado
        editor.highlighter = BinarySyntaxHighlighterEnhanced(editor.document())
        
        # Define o conteúdo inicial
        if content:
            editor.setPlainText(content)
        
        # Cria um widget de validação de código
        validation_widget = CodeValidationWidget(editor)
        
        # Adiciona a aba
        index = self.tabs.addTab(validation_widget, title)
        self.tabs.setCurrentIndex(index)
        
        # Atualiza a barra de status
        self.status_bar.showMessage(f"Nova aba criada: {title}")
        
        # Foca no editor
        editor.setFocus()
        
        return index
    
    def _close_tab(self, index):
        """
        Fecha uma aba.
        
        Args:
            index: Índice da aba a ser fechada
        """
        # Se for a última aba, exibe a tela de boas-vindas
        if self.tabs.count() == 1:
            self.tabs.removeTab(index)
            self._show_welcome_screen()
        else:
            self.tabs.removeTab(index)
        
        # Atualiza a barra de status
        self.status_bar.showMessage("Aba fechada")
    
    def _on_tab_changed(self, index):
        """
        Manipula a mudança de aba.
        
        Args:
            index: Índice da nova aba ativa
        """
        # Atualiza a barra de status
        if index >= 0:
            self.status_bar.showMessage(f"Aba atual: {self.tabs.tabText(index)}")
    
    def _get_current_editor(self):
        """
        Obtém o editor da aba atual.
        
        Returns:
            Editor de código ou None se não houver editor
        """
        current_widget = self.tabs.currentWidget()
        
        # Se for um widget de validação, obtém o editor
        if hasattr(current_widget, 'editor'):
            return current_widget.editor
        
        # Se for um editor diretamente
        if isinstance(current_widget, CodeEditor):
            return current_widget
        
        return None
    
    def _get_current_code(self):
        """
        Obtém o código do editor atual.
        
        Returns:
            String contendo o código ou None se não houver editor
        """
        editor = self._get_current_editor()
        if editor:
            return editor.toPlainText()
        return None
    
    def _open_file(self):
        """Abre um arquivo."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo", "", "Todos os Arquivos (*)"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Cria uma nova aba com o conteúdo do arquivo
            title = os.path.basename(filename)
            self._new_tab(content, title)
            
            # Atualiza a barra de status
            self.status_bar.showMessage(f"Arquivo aberto: {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o arquivo:\n{str(e)}")
    
    def _save_file(self, as_new=False):
        """
        Salva o conteúdo do editor atual em um arquivo.
        
        Args:
            as_new: Se True, sempre pede um novo nome de arquivo
        """
        editor = self._get_current_editor()
        if not editor:
            return
        
        current_tab_index = self.tabs.currentIndex()
        current_tab_title = self.tabs.tabText(current_tab_index)
        
        # Se for "Salvar Como" ou se o arquivo não tiver nome
        if as_new or current_tab_title == "Sem título":
            filename, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo", "", "Todos os Arquivos (*)"
            )
            
            if not filename:
                return
        else:
            # Usa o nome atual da aba
            filename = current_tab_title
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(editor.toPlainText())
            
            # Atualiza o título da aba
            title = os.path.basename(filename)
            self.tabs.setTabText(current_tab_index, title)
            
            # Atualiza a barra de status
            self.status_bar.showMessage(f"Arquivo salvo: {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar o arquivo:\n{str(e)}")
    
    def _undo(self):
        """Desfaz a última ação no editor atual."""
        editor = self._get_current_editor()
        if editor:
            editor.undo()
    
    def _redo(self):
        """Refaz a última ação desfeita no editor atual."""
        editor = self._get_current_editor()
        if editor:
            editor.redo()
    
    def _cut(self):
        """Recorta o texto selecionado no editor atual."""
        editor = self._get_current_editor()
        if editor:
            editor.cut()
    
    def _copy(self):
        """Copia o texto selecionado no editor atual."""
        editor = self._get_current_editor()
        if editor:
            editor.copy()
    
    def _paste(self):
        """Cola o texto da área de transferência no editor atual."""
        editor = self._get_current_editor()
        if editor:
            editor.paste()
    
    def _text_to_binary(self):
        """Converte o texto selecionado para binário."""
        editor = self._get_current_editor()
        if not editor:
            return
        
        # Obtém o texto selecionado ou todo o texto
        cursor = editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
        else:
            text = editor.toPlainText()
        
        # Converte para binário
        try:
            binary = self.binario_interpreter.converter_para_binario(text)
            
            # Cria uma nova aba com o resultado
            self._new_tab(binary, "Convertido para Binário")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para binário:\n{str(e)}")
    
    def _binary_to_text(self):
        """Converte o código binário para texto."""
        editor = self._get_current_editor()
        if not editor:
            return
        
        # Obtém o texto selecionado ou todo o texto
        cursor = editor.textCursor()
        if cursor.hasSelection():
            binary = cursor.selectedText()
        else:
            binary = editor.toPlainText()
        
        # Converte para texto
        try:
            text = self.binario_interpreter.traduzir_binario(binary)
            
            # Cria uma nova aba com o resultado
            self._new_tab(text, "Convertido para Texto")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para texto:\n{str(e)}")
    
    def _open_terminal(self):
        """Abre o terminal interativo."""
        terminal = TerminalEnhanced("Terminal Interativo\n", self)
        terminal.exec_()
    
    def _autosave(self):
        """Salva automaticamente o conteúdo de todas as abas."""
        for i in range(self.tabs.count()):
            # Ignora a tela de boas-vindas
            if self.tabs.tabText(i) == "Início":
                continue
            
            # Obtém o widget da aba
            tab_widget = self.tabs.widget(i)
            
            # Obtém o editor
            editor = None
            if hasattr(tab_widget, 'editor'):
                editor = tab_widget.editor
            elif isinstance(tab_widget, CodeEditor):
                editor = tab_widget
            
            if editor:
                # Salva o conteúdo
                content = editor.toPlainText()
                title = self.tabs.tabText(i)
                
                self.temp_manager.save_tab_content(
                    self.session_id, i, content, tab_title=title
                )
        
        # Atualiza a barra de status
        self.status_bar.showMessage("Salvamento automático concluído", 2000)
    
    def _check_recoverable_sessions(self):
        """Verifica se há sessões recuperáveis e pergunta ao usuário se deseja recuperá-las."""
        recoverable = self.temp_manager.get_recoverable_sessions()
        
        if not recoverable:
            return
        
        # Pergunta ao usuário se deseja recuperar a sessão mais recente
        latest_session = max(
            recoverable,
            key=lambda s: s["last_modified"]
        )
        
        reply = QMessageBox.question(
            self,
            "Recuperar Sessão",
            f"Encontrada uma sessão anterior com {len(latest_session['tabs'])} abas.\n"
            f"Deseja recuperá-la?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Recupera a sessão
            tabs = self.temp_manager.recover_session(latest_session["id"])
            
            # Remove a tela de boas-vindas
            if self.tabs.count() == 1 and self.tabs.tabText(0) == "Início":
                self.tabs.removeTab(0)
            
            # Cria as abas recuperadas
            for content, _, title in tabs:
                self._new_tab(content, title)
            
            # Atualiza a barra de status
            self.status_bar.showMessage(f"Sessão recuperada: {len(tabs)} abas")
    
    def closeEvent(self, event):
        """
        Manipula o evento de fechamento da janela.
        
        Args:
            event: Evento de fechamento
        """
        # Pergunta ao usuário se deseja salvar as alterações
        if self.tabs.count() > 0 and self.tabs.tabText(0) != "Início":
            reply = QMessageBox.question(
                self,
                "Sair",
                "Deseja salvar as alterações antes de sair?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Cancel:
                event.ignore()
                return
            
            if reply == QMessageBox.Yes:
                # Salva todas as abas
                for i in range(self.tabs.count()):
                    self.tabs.setCurrentIndex(i)
                    self._save_file()
        
        # Aceita o evento de fechamento
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnhancedMainWindow()
    window.show()
    sys.exit(app.exec_())
