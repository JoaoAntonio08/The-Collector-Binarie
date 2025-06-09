"""
Módulo principal integrado e simplificado para o The Collector Binarie.
Esta versão integra o interpretador aprimorado para suportar scripts complexos.
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox,
    QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QWidget, QSplitter,
    QLabel, QHBoxLayout, QMenu, QMenuBar, QFrame, QStackedWidget,
    QPushButton, QPlainTextEdit
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal

# Importa os módulos necessários (assumindo que estão no mesmo diretório)
try:
    from three_panel_layout import ThreePanelLayout
    from file_explorer_panel import FileExplorerPanel
    from binary_reference_guide_fixed import BinaryReferenceGuide
    from welcome_screen_simplified import WelcomeScreen
    from windows_style_terminal_simplified import WindowsStyleTerminalSimplified
    from binary_interpreter_enhanced_v2 import BinaryInterpreterEnhancedV2
    from binary_code_executor_enhanced_v2 import BinaryCodeExecutorEnhancedV2
    from code_editor import CodeEditor
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Certifique-se de que todos os arquivos .py necessários estejam no mesmo diretório que main_app_enhanced_v2.py")
    sys.exit(1)

class MainAppWindowEnhancedV2(QMainWindow):
    """
    Janela principal integrada para o The Collector Binarie.
    """
    
    def __init__(self):
        """Inicializa a janela principal."""
        super().__init__()
        
        # Configurações básicas
        self.setWindowTitle("The Collector Binarie")
        self.setGeometry(100, 100, 1200, 800)
        
        # Caminho para o logo (assumindo que está no mesmo diretório)
        self.logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        if not os.path.exists(self.logo_path):
            print(f"Aviso: Arquivo logo.png não encontrado em {self.logo_path}")
            self.logo_path = None # Define como None se não encontrado

        # Inicializa componentes
        self.binary_interpreter = BinaryInterpreterEnhancedV2()
        self.code_executor = BinaryCodeExecutorEnhancedV2(self.binary_interpreter)
        
        # Configuração da interface
        self._setup_ui()
        
        # Configura o tema escuro moderno
        self._apply_modern_dark_theme()
    
    def _setup_ui(self):
        """Configura a interface do usuário."""
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Barra de menu personalizada
        self.custom_menu_bar = self._create_custom_menu_bar()
        main_layout.addWidget(self.custom_menu_bar)
        
        # Layout de três painéis
        self.three_panel_layout = ThreePanelLayout()
        main_layout.addWidget(self.three_panel_layout)
        
        # Configura o painel esquerdo (navegador de arquivos)
        self.file_explorer = FileExplorerPanel()
        self.file_explorer.file_opened.connect(self._open_file)
        self.three_panel_layout.set_left_panel_widget(self.file_explorer)
        
        # Configura o painel central (editor de código)
        self.central_stack = QStackedWidget()
        
        # Tela de boas-vindas
        self.welcome_screen = WelcomeScreen(logo_path=self.logo_path)
        self.welcome_screen.get_new_file_button().clicked.connect(self._new_file)
        self.welcome_screen.get_open_file_button().clicked.connect(self._open_file_dialog)
        self.central_stack.addWidget(self.welcome_screen)
        
        # Editor com abas
        self.editor_widget = QWidget()
        editor_layout = QVBoxLayout(self.editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #0f0f2d;
                border-radius: 10px;
            }
            QTabBar::tab {
                background-color: #1e1e3f;
                color: #ffffff;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #2d2d5a;
                border-bottom: 2px solid #bd93f9;
            }
            QTabBar::tab:hover {
                background-color: #3e3e5e;
            }
            QTabBar::close-button {
                /* image: url(close.png); */ /* Comentado para evitar erro se não existir */
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                background-color: #ff5555;
                border-radius: 4px;
            }
        """)
        
        editor_layout.addWidget(self.tabs)
        self.central_stack.addWidget(self.editor_widget)
        
        # Adiciona o stack ao painel central
        self.three_panel_layout.set_center_panel_widget(self.central_stack)
        
        # Configura o painel direito (guia de referência)
        self.reference_guide = BinaryReferenceGuide()
        self.reference_guide.code_selected.connect(self._insert_binary_code)
        self.three_panel_layout.set_right_panel_widget(self.reference_guide)
        
        # Exibe a tela de boas-vindas inicialmente
        self.central_stack.setCurrentWidget(self.welcome_screen)
        
        # Barra de status
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #0a0a23;
                color: #ffffff;
                border-top: 1px solid #1e1e3f;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
        # Inicializa o terminal
        self._setup_terminal()
    
    def _create_custom_menu_bar(self):
        """Cria a barra de menu personalizada."""
        menu_bar = QFrame()
        menu_bar.setObjectName("customMenuBar")
        menu_bar.setStyleSheet("""
            #customMenuBar { background-color: #0a0a23; border-bottom: 1px solid #1e1e3f; min-height: 40px; max-height: 40px; }
            QPushButton { background-color: transparent; color: #ffffff; border: none; padding: 8px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #1e1e3f; border-radius: 5px; }
            QPushButton#runButton { background-color: #00aa00; border-radius: 5px; padding: 8px 12px; }
            QPushButton#runButton:hover { background-color: #00cc00; }
            QPushButton#terminalButton { background-color: #1e1e3f; border-radius: 5px; padding: 8px 12px; }
            QPushButton#terminalButton:hover { background-color: #2d2d5a; }
        """)
        
        menu_layout = QHBoxLayout(menu_bar)
        menu_layout.setContentsMargins(10, 0, 10, 0)
        menu_layout.setSpacing(5)
        
        # Menus
        self.arquivo_button = self._create_menu_button("Arquivo")
        self.arquivo_menu = QMenu(self)
        self._populate_arquivo_menu()
        self.arquivo_button.setMenu(self.arquivo_menu)
        menu_layout.addWidget(self.arquivo_button)

        self.traducao_button = self._create_menu_button("Tradução")
        self.traducao_menu = QMenu(self)
        self._populate_traducao_menu()
        self.traducao_button.setMenu(self.traducao_menu)
        menu_layout.addWidget(self.traducao_button)

        self.config_button = self._create_menu_button("Configurações")
        self.config_menu = QMenu(self)
        self._populate_config_menu()
        self.config_button.setMenu(self.config_menu)
        menu_layout.addWidget(self.config_button)
        
        menu_layout.addStretch()
        
        # Botões de ação
        self.run_button = self._create_action_button("▶ Run", "runButton")
        self.run_button.clicked.connect(self._run_code)
        menu_layout.addWidget(self.run_button)
        
        self.terminal_button = self._create_action_button("⌨ Terminal", "terminalButton")
        self.terminal_button.clicked.connect(self._show_terminal)
        menu_layout.addWidget(self.terminal_button)
        
        menu_layout.addStretch()
        
        return menu_bar

    def _populate_arquivo_menu(self):
        self.arquivo_menu.setStyleSheet("QMenu { background-color: #0a0a23; color: #ffffff; border: 1px solid #1e1e3f; border-radius: 5px; } QMenu::item { padding: 8px 20px; } QMenu::item:selected { background-color: #1e1e3f; }")
        new_action = QAction("Novo Arquivo", self)
        new_action.triggered.connect(self._new_file)
        self.arquivo_menu.addAction(new_action)
        open_action = QAction("Abrir Arquivo", self)
        open_action.triggered.connect(self._open_file_dialog)
        self.arquivo_menu.addAction(open_action)
        self.arquivo_menu.addSeparator()
        save_action = QAction("Salvar", self)
        save_action.triggered.connect(self._save_file)
        self.arquivo_menu.addAction(save_action)
        save_as_action = QAction("Salvar Como", self)
        save_as_action.triggered.connect(lambda: self._save_file(as_new=True))
        self.arquivo_menu.addAction(save_as_action)
        self.arquivo_menu.addSeparator()
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        self.arquivo_menu.addAction(exit_action)

    def _populate_traducao_menu(self):
        self.traducao_menu.setStyleSheet(self.arquivo_menu.styleSheet())
        text_to_binary_action = QAction("Texto → Binário", self)
        text_to_binary_action.triggered.connect(self._text_to_binary)
        self.traducao_menu.addAction(text_to_binary_action)
        binary_to_text_action = QAction("Binário → Texto", self)
        binary_to_text_action.triggered.connect(self._binary_to_text)
        self.traducao_menu.addAction(binary_to_text_action)

    def _populate_config_menu(self):
        self.config_menu.setStyleSheet(self.arquivo_menu.styleSheet())
        theme_action = QAction("Tema (Não implementado)", self)
        self.config_menu.addAction(theme_action)
        font_action = QAction("Fonte (Não implementado)", self)
        self.config_menu.addAction(font_action)

    def _create_menu_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10))
        return button

    def _create_action_button(self, text, object_name):
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setFont(QFont("Arial", 10, QFont.Bold))
        return button

    def _setup_terminal(self):
        self.terminal = None # Será criado sob demanda

    def _apply_modern_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #0a0a23; color: #ffffff; }
            QWidget { background-color: #0a0a23; color: #ffffff; }
            QSplitter::handle { background-color: #1e1e3f; width: 2px; height: 2px; }
            QSplitter::handle:hover { background-color: #3e3e5e; }
            QScrollBar:vertical { background-color: #0a0a23; width: 14px; margin: 0px; }
            QScrollBar::handle:vertical { background-color: #1e1e3f; min-height: 20px; border-radius: 7px; }
            QScrollBar::handle:vertical:hover { background-color: #3e3e5e; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background-color: #0a0a23; }
            QScrollBar:horizontal { background-color: #0a0a23; height: 14px; margin: 0px; }
            QScrollBar::handle:horizontal { background-color: #1e1e3f; min-width: 20px; border-radius: 7px; }
            QScrollBar::handle:horizontal:hover { background-color: #3e3e5e; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background-color: #0a0a23; }
        """)

    def _new_file(self):
        self.central_stack.setCurrentWidget(self.editor_widget)
        editor = CodeEditor()
        editor.setStyleSheet("QPlainTextEdit { background-color: #0f0f2d; color: #ffffff; border: none; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; selection-background-color: #2d2d5a; } QPlainTextEdit:focus { border: none; }")
        index = self.tabs.addTab(editor, "Sem título")
        self.tabs.setCurrentIndex(index)
        editor.setFocus()
        self.status_bar.showMessage("Novo arquivo criado")

    def _open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*)")
        if filename:
            self._open_file(filename)

    def _open_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.central_stack.setCurrentWidget(self.editor_widget)
            editor = CodeEditor()
            editor.setStyleSheet("QPlainTextEdit { background-color: #0f0f2d; color: #ffffff; border: none; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; selection-background-color: #2d2d5a; } QPlainTextEdit:focus { border: none; }")
            editor.setPlainText(content)
            title = os.path.basename(filename)
            index = self.tabs.addTab(editor, title)
            self.tabs.setCurrentIndex(index)
            editor.setProperty("filepath", filename)
            editor.setFocus()
            self.status_bar.showMessage(f"Arquivo aberto: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir o arquivo:\n{str(e)}")

    def _save_file(self, as_new=False):
        if self.tabs.count() == 0:
            return
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        filepath = current_editor.property("filepath")
        if as_new or not filepath:
            filename, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Todos os Arquivos (*)")
            if not filename:
                return
            filepath = filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(current_editor.toPlainText())
            title = os.path.basename(filepath)
            self.tabs.setTabText(self.tabs.currentIndex(), title)
            current_editor.setProperty("filepath", filepath)
            self.status_bar.showMessage(f"Arquivo salvo: {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar o arquivo:\n{str(e)}")

    def _close_tab(self, index):
        self.tabs.removeTab(index)
        if self.tabs.count() == 0:
            self.central_stack.setCurrentWidget(self.welcome_screen)
        self.status_bar.showMessage("Aba fechada")

    def _text_to_binary(self):
        if self.tabs.count() == 0: return
        current_editor = self.tabs.currentWidget()
        if not current_editor: return
        cursor = current_editor.textCursor()
        text = cursor.selectedText() if cursor.hasSelection() else current_editor.toPlainText()
        try:
            binary = self.binary_interpreter.converter_para_binario(text)
            self._new_file()
            new_editor = self.tabs.currentWidget()
            new_editor.setPlainText(binary)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido para Binário")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para binário:\n{str(e)}")

    def _binary_to_text(self):
        if self.tabs.count() == 0: return
        current_editor = self.tabs.currentWidget()
        if not current_editor: return
        cursor = current_editor.textCursor()
        binary = cursor.selectedText() if cursor.hasSelection() else current_editor.toPlainText()
        try:
            text = self.binary_interpreter.traduzir_binario(binary)
            self._new_file()
            new_editor = self.tabs.currentWidget()
            new_editor.setPlainText(text)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido para Texto")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para texto:\n{str(e)}")

    def _run_code(self):
        if self.tabs.count() == 0: return
        current_editor = self.tabs.currentWidget()
        if not current_editor: return
        code = current_editor.toPlainText()
        try:
            result = self.code_executor.execute_binary_code(code)
            self._show_terminal(result)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao executar o código:\n{str(e)}")

    def _show_terminal(self, initial_text=None):
        if not self.terminal:
            try:
                self.terminal = WindowsStyleTerminalSimplified(self)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar o terminal:\n{str(e)}")
                return
        if initial_text:
            self.terminal.output_area.clear()
            self.terminal.output_area.insertPlainText(initial_text)
        self.terminal.show()
        self.terminal.raise_()
        self.terminal.activateWindow()

    def _insert_binary_code(self, code):
        if self.tabs.count() == 0:
            self._new_file()
        current_editor = self.tabs.currentWidget()
        if not current_editor: return
        cursor = current_editor.textCursor()
        cursor.insertText(code)
        current_editor.setTextCursor(cursor)
        current_editor.setFocus()

    def closeEvent(self, event):
        if self.tabs.count() > 0:
            reply = QMessageBox.question(self, "Sair", "Deseja salvar as alterações antes de sair?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Cancel:
                event.ignore()
                return
            if reply == QMessageBox.Yes:
                for i in range(self.tabs.count()):
                    self.tabs.setCurrentIndex(i)
                    self._save_file()
        event.accept()

if __name__ == "__main__":
    # Adiciona tratamento para o aviso de depreciação (opcional)
    # import sip
    # sip.setapi('QString', 2)
    # sip.setapi('QVariant', 2)
    
    app = QApplication(sys.argv)
    window = MainAppWindowEnhancedV2()
    window.show()
    sys.exit(app.exec_())
