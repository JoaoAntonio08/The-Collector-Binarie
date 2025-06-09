"""
Módulo principal integrado e simplificado para o The Collector Binarie.
Versão final sem diagnósticos.
"""

import os
import sys
import tempfile
import traceback
import configparser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox,
    QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QWidget, QSplitter,
    QLabel, QHBoxLayout, QMenu, QMenuBar, QFrame, QStackedWidget,
    QPushButton, QPlainTextEdit, QDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal

# Importa os módulos necessários
try:
    from ui.three_panel_layout import ThreePanelLayout
    from ui.workspace_file_explorer import WorkspaceFileExplorer
    from ui.binary_reference_guide_fixed import BinaryReferenceGuide
    from ui.welcome_screen_simplified import WelcomeScreen
    from ui.windows_style_terminal_simplified import WindowsStyleTerminalSimplified
    from ui.binary_interpreter_fixed import BinaryInterpreterFixed
    from ui.code_editor import CodeEditor
    from ui.theme_manager import ThemeManager
    from ui.about_dialog import AboutDialog
    from ui.binary_code_executor_fixed import BinaryCodeExecutorFixed
except ImportError as e:
    error_details = traceback.format_exc()
    print(f"Não foi possível importar um módulo necessário: {e}\nDetalhes: {error_details}")
    sys.exit(1)
except Exception as e:
    error_details = traceback.format_exc()
    print(f"Ocorreu um erro inesperado durante a inicialização: {e}\nDetalhes: {error_details}")
    sys.exit(1)

# Função auxiliar para obter caminho de recursos
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class MainAppWindowFixed(QMainWindow):
    """
    Janela principal final.
    """

    def __init__(self):
        super().__init__()
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "user_settings.ini")
        self.config = self._load_or_create_config()
        self.user_name = self.config.get("User", "name", fallback="Usuário")
        self.language = self.config.get("User", "language", fallback="pt")
        self.code_color = self.config.get("Editor", "code_color", fallback="#ff79c6")
        self.font_size = int(self.config.get("Editor", "font_size", fallback="16"))
        self.theme = self.config.get("App", "theme", fallback=ThemeManager.DARK_BLUE)

        self.setWindowTitle("The Collector Binarie")
        self.setGeometry(100, 100, 1200, 800)

        self.logo_path = None
        try:
            logo_resource = resource_path(os.path.join("resources", "logo.png"))
            icon_resource = resource_path(os.path.join("resources", "logo.ico"))
            if os.path.exists(icon_resource):
                self.setWindowIcon(QIcon(icon_resource))
                if os.path.exists(logo_resource):
                    self.logo_path = logo_resource
            elif os.path.exists(logo_resource):
                self.setWindowIcon(QIcon(logo_resource))
                self.logo_path = logo_resource
        except Exception as e:
            print(f"Aviso: Erro ao carregar logo: {e}", flush=True)

        self.binary_interpreter = BinaryInterpreterFixed()
        self.code_executor = BinaryCodeExecutorFixed(self.binary_interpreter)
        self.theme_manager = ThemeManager()
        self.terminal = None # Inicializa como None

        self._setup_ui()
        self._apply_theme(self.theme)
        self._apply_font_size(self.font_size)
        self._apply_code_color(self.code_color)
        self._apply_language(self.language)

    def _load_or_create_config(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_path):
            from ui.initial_setup_dialog import InitialSetupDialog
            dialog = InitialSetupDialog()
            if dialog.exec_() == QDialog.Accepted:
                config["User"] = {
                    "name": dialog.name,
                    "language": dialog.language
                }
                config["App"] = {
                    "theme": dialog.theme
                }
                config["Editor"] = {
                    "font_size": str(dialog.font_size)
                }
                with open(self.config_path, "w", encoding="utf-8") as f:
                    config.write(f)
            else:
                # Defaults
                config["User"] = {"name": "Usuário", "language": "pt"}
                config["App"] = {"theme": ThemeManager.DARK_BLUE}
                config["Editor"] = {"font_size": "16"}
                with open(self.config_path, "w", encoding="utf-8") as f:
                    config.write(f)
        else:
            config.read(self.config_path, encoding="utf-8")
        return config

    def _setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.custom_menu_bar = self._create_custom_menu_bar()
        main_layout.addWidget(self.custom_menu_bar)

        self.three_panel_layout = ThreePanelLayout()
        main_layout.addWidget(self.three_panel_layout)

        self.file_explorer = WorkspaceFileExplorer()
        self.file_explorer.file_opened.connect(self._open_file)
        self.three_panel_layout.set_left_panel_widget(self.file_explorer)

        self.central_stack = QStackedWidget()
        self.welcome_screen = WelcomeScreen(logo_path=self.logo_path)
        self.welcome_screen.get_new_file_button().clicked.connect(self._new_file)
        self.welcome_screen.get_open_file_button().clicked.connect(self._open_file_dialog)
        self.central_stack.addWidget(self.welcome_screen)

        self.editor_widget = QWidget()
        editor_layout = QVBoxLayout(self.editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: none; background-color: #181a20; border-radius: 14px; }
            QTabBar::tab { background-color: #23272e; color: #e6e6e6; border-top-left-radius: 10px; border-top-right-radius: 10px; padding: 10px 32px; margin-right: 4px; font-size: 15px; max-width: 350px; }
            QTabBar::tab:selected { background-color: #2d2d5a; border-bottom: 3px solid #bd93f9; }
            QTabBar::tab:hover { background-color: #3e3e5e; }
            QTabBar::close-button { subcontrol-position: right; border-radius: 6px; padding: 2px; }
            QTabBar::close-button:hover { background-color: #ff5555; }
            QTabBar QToolButton { width: 24px; height: 24px; }
        """)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.setUsesScrollButtons(True)
        editor_layout.addWidget(self.tabs)
        self.central_stack.addWidget(self.editor_widget)
        self.three_panel_layout.set_center_panel_widget(self.central_stack)

        self.reference_guide = BinaryReferenceGuide()
        self.reference_guide.code_selected.connect(self._insert_binary_code)
        self.three_panel_layout.set_right_panel_widget(self.reference_guide)

        self.central_stack.setCurrentWidget(self.welcome_screen)

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar { background-color: #181a20; color: #bd93f9; border-top: 1px solid #282a36; font-size: 15px; }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")

    def _create_custom_menu_bar(self):
        menu_bar = QFrame()
        menu_bar.setObjectName("customMenuBar")
        menu_bar.setStyleSheet("""
            #customMenuBar { background-color: #23272e; border-bottom: 1px solid #282a36; min-height: 54px; max-height: 54px; }
            QPushButton { background-color: transparent; color: #e6e6e6; border: none; padding: 12px 22px; font-weight: bold; font-size: 15px; border-radius: 10px; }
            QPushButton:hover { background-color: #2d2d5a; }
            QPushButton#runButton { background-color: #00aa00; color: #fff; border-radius: 10px; font-size: 16px; }
            QPushButton#runButton:hover { background-color: #00cc00; }
            QPushButton#terminalButton { background-color: #23272e; border-radius: 10px; font-size: 16px; }
            QPushButton#terminalButton:hover { background-color: #2d2d5a; }
            QPushButton#aiButton { background-color: #bd93f9; color: #23272e; border-radius: 10px; font-size: 16px; }
            QPushButton#aiButton:hover { background-color: #a882e6; }
            QMenu { background-color: #23272e; color: #e6e6e6; border: 1px solid #282a36; border-radius: 10px; }
            QMenu::item { padding: 12px 28px; font-size: 15px; }
            QMenu::item:selected { background-color: #2d2d5a; }
        """)
        menu_layout = QHBoxLayout(menu_bar)
        menu_layout.setContentsMargins(24, 0, 24, 0)
        menu_layout.setSpacing(12)

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

        self.run_button = self._create_action_button("▶ Run", "runButton")
        self.run_button.clicked.connect(self._run_code)
        menu_layout.addWidget(self.run_button)

        self.terminal_button = self._create_action_button("⌨ Terminal", "terminalButton")
        self.terminal_button.clicked.connect(self._show_terminal)
        menu_layout.addWidget(self.terminal_button)

        self.ai_button = self._create_action_button("🤖 IA Binária", "aiButton")
        self.ai_button.clicked.connect(self._show_binary_ai)
        menu_layout.addWidget(self.ai_button)

        menu_layout.addStretch()
        return menu_bar

    def _populate_arquivo_menu(self):
        new_action = QAction("Novo Arquivo", self); new_action.setShortcut("Ctrl+Shift+N"); new_action.triggered.connect(self._new_file); self.arquivo_menu.addAction(new_action)
        open_action = QAction("Abrir Arquivo", self); open_action.setShortcut("Ctrl+Shift+A"); open_action.triggered.connect(self._open_file_dialog); self.arquivo_menu.addAction(open_action)
        open_folder_action = QAction("Abrir Pasta", self); open_folder_action.setShortcut("Ctrl+Shift+P"); open_folder_action.triggered.connect(self._open_workspace); self.arquivo_menu.addAction(open_folder_action)
        self.arquivo_menu.addSeparator()
        save_action = QAction("Salvar", self); save_action.setShortcut("Ctrl+S"); save_action.triggered.connect(self._save_file); self.arquivo_menu.addAction(save_action)
        save_as_action = QAction("Salvar Como", self); save_as_action.setShortcut("Ctrl+Shift+S"); save_as_action.triggered.connect(lambda: self._save_file(as_new=True)); self.arquivo_menu.addAction(save_as_action)
        self.arquivo_menu.addSeparator()
        exit_action = QAction("Sair", self); exit_action.triggered.connect(self.close); self.arquivo_menu.addAction(exit_action)

    def _populate_traducao_menu(self):
        text_to_binary_action = QAction("Texto → Binário", self); text_to_binary_action.triggered.connect(self._text_to_binary); self.traducao_menu.addAction(text_to_binary_action)
        binary_to_text_action = QAction("Binário → Texto", self); binary_to_text_action.triggered.connect(self._binary_to_text); self.traducao_menu.addAction(binary_to_text_action)

    def _populate_config_menu(self):
        theme_menu = QMenu("Tema", self)
        dark_blue_action = QAction("Dark Blue", self); dark_blue_action.triggered.connect(lambda: self._apply_theme(ThemeManager.DARK_BLUE)); theme_menu.addAction(dark_blue_action)
        dark_action = QAction("Dark", self); dark_action.triggered.connect(lambda: self._apply_theme(ThemeManager.DARK)); theme_menu.addAction(dark_action)
        white_action = QAction("White", self); white_action.triggered.connect(lambda: self._apply_theme(ThemeManager.WHITE)); theme_menu.addAction(white_action)
        self.config_menu.addMenu(theme_menu)
        about_action = QAction("Sobre Nós", self); about_action.triggered.connect(self._show_about_dialog); self.config_menu.addAction(about_action)

    def _create_menu_button(self, text):
        button = QPushButton(text); button.setFont(QFont("Arial", 10)); return button

    def _create_action_button(self, text, object_name):
        button = QPushButton(text); button.setObjectName(object_name); button.setFont(QFont("Arial", 10, QFont.Bold)); return button

    def _apply_theme(self, theme_name=None):
        style = self.theme_manager.get_theme_style(theme_name)
        QApplication.instance().setStyleSheet(style)
        self.setStyleSheet(style)
        self.central_widget.setStyleSheet(style)
        self.editor_widget.setStyleSheet(style)
        self.tabs.setStyleSheet(style)
        self.custom_menu_bar.setStyleSheet(style)
        self.status_bar.setStyleSheet(style)
        if self.terminal and self.terminal.isVisible():
            terminal_style = self.theme_manager.get_terminal_style(theme_name)
            self.terminal.setStyleSheet(terminal_style)
        if theme_name:
            self.theme_manager.set_theme(theme_name)

    def _apply_font_size(self, font_size):
        # Aplica o tamanho da fonte nos editores abertos e padrão
        self.default_editor_style = f"""
            QPlainTextEdit {{
                background-color: #181a20;
                color: #e6e6e6;
                border: none;
                font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace;
                font-size: {font_size}px;
                selection-background-color: #2d2d5a;
                border-radius: 10px;
                padding: 10px;
            }}
            QPlainTextEdit:focus {{ border: none; }}
        """

    def _apply_code_color(self, color):
        # Atualiza cor dos códigos (palavra-chave) no highlighter
        from ui.syntax_highlighter_enhanced import BinarySyntaxHighlighterEnhanced
        BinarySyntaxHighlighterEnhanced.DEFAULT_KEYWORD_COLOR = color

    def _apply_language(self, lang):
        self.language = lang
        if lang == "en":
            self.setWindowTitle("The Collector Binarie")
            self.arquivo_button.setText("File")
            self.traducao_button.setText("Translate")
            self.config_button.setText("Settings")
            self.run_button.setText("▶ Run")
            self.terminal_button.setText("⌨ Terminal")
            self.ai_button.setText("🤖 Binary AI")
            self.status_bar.showMessage("Ready")
            # Menus
            self._update_menu_texts_en()
            # Welcome screen
            if hasattr(self.welcome_screen, "set_language"):
                self.welcome_screen.set_language("en")
        else:
            self.setWindowTitle("The Collector Binarie")
            self.arquivo_button.setText("Arquivo")
            self.traducao_button.setText("Tradução")
            self.config_button.setText("Configurações")
            self.run_button.setText("▶ Run")
            self.terminal_button.setText("⌨ Terminal")
            self.ai_button.setText("🤖 IA Binária")
            self.status_bar.showMessage("Pronto")
            self._update_menu_texts_pt()
            if hasattr(self.welcome_screen, "set_language"):
                self.welcome_screen.set_language("pt")

    def _update_menu_texts_en(self):
        # Arquivo
        self.arquivo_menu.actions()[0].setText("New File")
        self.arquivo_menu.actions()[0].setShortcut("Ctrl+Shift+N")
        self.arquivo_menu.actions()[1].setText("Open File")
        self.arquivo_menu.actions()[1].setShortcut("Ctrl+Shift+A")
        self.arquivo_menu.actions()[2].setText("Open Folder")
        self.arquivo_menu.actions()[2].setShortcut("Ctrl+Shift+P")
        self.arquivo_menu.actions()[4].setText("Save")
        self.arquivo_menu.actions()[4].setShortcut("Ctrl+S")
        self.arquivo_menu.actions()[5].setText("Save As")
        self.arquivo_menu.actions()[5].setShortcut("Ctrl+Shift+S")
        self.arquivo_menu.actions()[7].setText("Exit")
        # Tradução
        self.traducao_menu.actions()[0].setText("Text → Binary")
        self.traducao_menu.actions()[1].setText("Binary → Text")
        # Configurações
        self.config_menu.actions()[0].menu().setTitle("Theme")
        self.config_menu.actions()[0].menu().actions()[0].setText("Dark Blue")
        self.config_menu.actions()[0].menu().actions()[1].setText("Dark")
        self.config_menu.actions()[0].menu().actions()[2].setText("White")
        self.config_menu.actions()[1].setText("About Us")

    def _update_menu_texts_pt(self):
        # Arquivo
        self.arquivo_menu.actions()[0].setText("Novo Arquivo")
        self.arquivo_menu.actions()[1].setText("Abrir Arquivo")
        self.arquivo_menu.actions()[2].setText("Abrir Pasta")
        self.arquivo_menu.actions()[4].setText("Salvar")
        self.arquivo_menu.actions()[5].setText("Salvar Como")
        self.arquivo_menu.actions()[7].setText("Sair")
        # Tradução
        self.traducao_menu.actions()[0].setText("Texto → Binário")
        self.traducao_menu.actions()[1].setText("Binário → Texto")
        # Configurações
        self.config_menu.actions()[0].menu().setTitle("Tema")
        self.config_menu.actions()[0].menu().actions()[0].setText("Dark Blue")
        self.config_menu.actions()[0].menu().actions()[1].setText("Dark")
        self.config_menu.actions()[0].menu().actions()[2].setText("White")
        self.config_menu.actions()[1].setText("Sobre Nós")

    def _new_file(self):
        self.central_stack.setCurrentWidget(self.editor_widget)
        editor = CodeEditor()
        editor.setStyleSheet(self.default_editor_style)
        index = self.tabs.addTab(editor, "Sem título")
        self.tabs.setCurrentIndex(index)
        editor.setFocus()
        self.status_bar.showMessage("Novo arquivo criado")

    def _open_file_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Todos os Arquivos (*)")
        if filename: self._open_file(filename)

    def _open_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file: content = file.read()
            self.central_stack.setCurrentWidget(self.editor_widget)
            editor = CodeEditor()
            editor.setStyleSheet("""
                QPlainTextEdit {
                    background-color: #181a20;
                    color: #e6e6e6;
                    border: none;
                    font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace;
                    font-size: 16px;
                    selection-background-color: #2d2d5a;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPlainTextEdit:focus { border: none; }
            """)
            editor.setPlainText(content)
            title = os.path.basename(filename)
            index = self.tabs.addTab(editor, title)
            self.tabs.setCurrentIndex(index)
            editor.setProperty("filepath", filename)
            editor.setFocus()
            self.status_bar.showMessage(f"Arquivo aberto: {filename}")
        except Exception as e: QMessageBox.critical(self, "Erro", f"Erro ao abrir o arquivo:\n{str(e)}")

    def _open_workspace(self):
        if hasattr(self, 'file_explorer') and hasattr(self.file_explorer, '_open_workspace'): self.file_explorer._open_workspace()
        else: QMessageBox.warning(self, "Aviso", "Explorador de arquivos não inicializado corretamente.")

    def _save_file(self, as_new=False):
        if self.tabs.count() == 0: self.status_bar.showMessage("Nenhuma aba aberta para salvar."); return False
        current_editor = self.tabs.currentWidget()
        if not isinstance(current_editor, CodeEditor): self.status_bar.showMessage("A aba atual não é um editor."); return False
        filepath = current_editor.property("filepath")
        if as_new or not filepath:
            filename, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo Como", filepath or "", "Todos os Arquivos (*)")
            if not filename: return False
            filepath = filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file: file.write(current_editor.toPlainText())
            title = os.path.basename(filepath)
            self.tabs.setTabText(self.tabs.currentIndex(), title)
            current_editor.setProperty("filepath", filepath)
            self.status_bar.showMessage(f"Arquivo salvo: {filepath}"); return True
        except Exception as e: QMessageBox.critical(self, "Erro", f"Erro ao salvar o arquivo:\n{str(e)}"); return False

    def _close_tab(self, index):
        widget_to_close = self.tabs.widget(index)
        # TODO: Adicionar verificação de alterações não salvas
        self.tabs.removeTab(index)
        if self.tabs.count() == 0: self.central_stack.setCurrentWidget(self.welcome_screen)
        self.status_bar.showMessage("Aba fechada")

    def _text_to_binary(self):
        if self.tabs.count() == 0: return
        current_editor = self.tabs.currentWidget();
        if not isinstance(current_editor, CodeEditor): return
        cursor = current_editor.textCursor(); text = cursor.selectedText() if cursor.hasSelection() else current_editor.toPlainText()
        if not text: self.status_bar.showMessage("Nada para converter."); return
        try:
            binary = self.binary_interpreter.converter_para_binario(text)
            self._new_file(); new_editor = self.tabs.currentWidget(); new_editor.setPlainText(binary)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido para Binário")
            self.status_bar.showMessage("Texto convertido para binário.")
        except Exception as e: QMessageBox.critical(self, "Erro de Conversão", f"Erro ao converter para binário:\n{str(e)}")

    def _binary_to_text(self):
        if self.tabs.count() == 0: return
        current_editor = self.tabs.currentWidget();
        if not isinstance(current_editor, CodeEditor): return
        cursor = current_editor.textCursor(); binary = cursor.selectedText() if cursor.hasSelection() else current_editor.toPlainText()
        if not binary: self.status_bar.showMessage("Nada para traduzir."); return
        try:
            text = self.binary_interpreter.traduzir_binario(binary)
            self._new_file(); new_editor = self.tabs.currentWidget(); new_editor.setPlainText(text)
            self.tabs.setTabText(self.tabs.currentIndex(), "Traduzido para Texto")
            self.status_bar.showMessage("Binário traduzido para texto.")
        except Exception as e: QMessageBox.critical(self, "Erro de Tradução", f"Erro ao traduzir binário:\n{str(e)}")

    def _run_code(self):
        if self.tabs.count() == 0:
            QMessageBox.warning(self, "Aviso", "Nenhuma aba aberta para executar.")
            return
        current_editor = self.tabs.currentWidget()
        if not isinstance(current_editor, CodeEditor):
            QMessageBox.warning(self, "Aviso", "A aba atual não contém um editor de código.")
            return

        binary_code = current_editor.toPlainText()
        if not binary_code.strip():
            QMessageBox.warning(self, "Aviso", "O editor está vazio. Nada para executar.")
            return

        try:
            # Chama o executor interativo, que já exibe o resultado em um QDialog estilizado
            self.code_executor.execute_binary_code(binary_code, parent=self)
            self.status_bar.showMessage("Execução concluída.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao executar o código:\n{str(e)}")

    def _show_binary_ai(self):
        from ui.binary_ai_dialog import BinaryAIDialog
        dialog = BinaryAIDialog(self.binary_interpreter, parent=self)
        dialog.exec_()

    def _ensure_terminal(self):
        """Garante que a instância do terminal exista."""
        if self.terminal is None:
            try:
                self.terminal = WindowsStyleTerminalSimplified(self)
                self.terminal.finished.connect(self._terminal_closed)
                terminal_style = self.theme_manager.get_terminal_style()
                self.terminal.setStyleSheet(terminal_style)
            except Exception as e:
                error_details = traceback.format_exc()
                QMessageBox.critical(self, "Erro Fatal", f"Erro crítico ao criar o terminal:\n{str(e)}\nDetalhes: {error_details}")
                self.terminal = None
                return None
        return self.terminal

    def _show_terminal(self):
        """Cria (se necessário) e exibe a janela do terminal."""
        terminal_instance = self._ensure_terminal()
        if terminal_instance:
            try:
                terminal_instance.show()
                terminal_instance.raise_()
                terminal_instance.activateWindow()
                if hasattr(terminal_instance, 'input_field'):
                    terminal_instance.input_field.setFocus()
                self.status_bar.showMessage("Terminal aberto.")
            except Exception as e:
                error_details = traceback.format_exc()
                QMessageBox.critical(self, "Erro", f"Erro ao tentar exibir o terminal:\n{str(e)}\nDetalhes: {error_details}")
                self.status_bar.showMessage("Erro ao exibir o terminal.")
        else:
            self.status_bar.showMessage("Falha ao abrir o terminal.")

    def _terminal_closed(self):
        """Slot chamado quando o QDialog do terminal é fechado."""
        self.terminal = None
        self.status_bar.showMessage("Terminal fechado.")

    def _insert_binary_code(self, code):
        if self.tabs.count() == 0: self._new_file()
        current_editor = self.tabs.currentWidget()
        if isinstance(current_editor, CodeEditor):
            cursor = current_editor.textCursor(); cursor.insertText(code); current_editor.setTextCursor(cursor); current_editor.setFocus()
            self.status_bar.showMessage("Código binário inserido.")
        else: self.status_bar.showMessage("Abra uma aba de edição para inserir código.")

    def _show_about_dialog(self):
        about_dialog = AboutDialog(self)
        theme_style = self.theme_manager.get_theme_style()
        about_dialog.setStyleSheet(theme_style)
        about_dialog.exec_()

    def closeEvent(self, event):
        # TODO: Melhorar verificação de salvamento
        if self.tabs.count() > 0:
            reply = QMessageBox.question(self, "Sair", "Deseja salvar as alterações antes de sair?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Cancel: event.ignore(); return
            elif reply == QMessageBox.Yes:
                for i in range(self.tabs.count()): self.tabs.setCurrentIndex(i); self._save_file()

        if self.terminal:
            self.terminal.close()
        event.accept()

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainAppWindowFixed()
    window.show()
    sys.exit(app.exec_())

