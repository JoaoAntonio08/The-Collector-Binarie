"""
Módulo principal integrado para o The Collector Binarie.
Este módulo implementa a janela principal com todas as correções e melhorias solicitadas.
"""

import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMessageBox,
    QTabWidget, QToolBar, QStatusBar, QVBoxLayout, QWidget, QSplitter,
    QLabel, QHBoxLayout, QMenu, QMenuBar, QFrame, QStackedWidget
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal

# Importa os módulos personalizados
try:
    # Tenta importar da pasta ui
    from ui.three_panel_layout import ThreePanelLayout
    from ui.file_explorer_panel import FileExplorerPanel
    from ui.binary_reference_guide_fixed import BinaryReferenceGuide
    from ui.welcome_screen import WelcomeScreen
    from ui.windows_style_terminal_fixed import WindowsStyleTerminal
    from ui.bugs_panel import BugsPanel
    from ui.binary_interpreter_v2 import BinaryInterpreterV2
    from ui.binary_code_executor import BinaryCodeExecutor
    from ui.code_editor import CodeEditor
except ImportError:
    # Se falhar, tenta importar do diretório atual
    from three_panel_layout import ThreePanelLayout
    from file_explorer_panel import FileExplorerPanel
    from binary_reference_guide_fixed import BinaryReferenceGuide
    from welcome_screen import WelcomeScreen
    from windows_style_terminal_fixed import WindowsStyleTerminal
    from bugs_panel import BugsPanel
    from binary_interpreter_v2 import BinaryInterpreterV2
    from binary_code_executor import BinaryCodeExecutor
    from code_editor import CodeEditor

class ModernMainWindow(QMainWindow):
    """
    Janela principal moderna para o The Collector Binarie.
    """
    
    def __init__(self):
        """Inicializa a janela principal moderna."""
        super().__init__()
        
        # Configurações básicas
        self.setWindowTitle("The Collector Binarie")
        self.setGeometry(100, 100, 1200, 800)
        
        # Caminho para o logo
        self.logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        
        # Inicializa componentes
        self.binary_interpreter = BinaryInterpreterV2()
        self.code_executor = BinaryCodeExecutor(self.binary_interpreter)
        
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
                image: url(close.png);
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
        
        # Inicializa os painéis adicionais
        self._setup_terminal()
        self._setup_bugs_panel()
    
    def _create_custom_menu_bar(self):
        """
        Cria uma barra de menu personalizada conforme a imagem de referência.
        
        Returns:
            Widget contendo a barra de menu personalizada
        """
        menu_bar = QFrame()
        menu_bar.setObjectName("customMenuBar")
        menu_bar.setStyleSheet("""
            #customMenuBar {
                background-color: #0a0a23;
                border-bottom: 1px solid #1e1e3f;
                min-height: 40px;
                max-height: 40px;
            }
            
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 8px 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #1e1e3f;
                border-radius: 5px;
            }
            
            QPushButton#runButton {
                background-color: #00aa00;
                border-radius: 5px;
                padding: 8px 12px;
            }
            
            QPushButton#runButton:hover {
                background-color: #00cc00;
            }
            
            QPushButton#terminalButton {
                background-color: #1e1e3f;
                border-radius: 5px;
                padding: 8px 12px;
            }
            
            QPushButton#terminalButton:hover {
                background-color: #2d2d5a;
            }
            
            QPushButton#bugsButton {
                background-color: #aa0000;
                border-radius: 5px;
                padding: 8px 12px;
            }
            
            QPushButton#bugsButton:hover {
                background-color: #cc0000;
            }
        """)
        
        # Layout da barra de menu
        menu_layout = QHBoxLayout(menu_bar)
        menu_layout.setContentsMargins(10, 0, 10, 0)
        menu_layout.setSpacing(5)
        
        # Menus principais
        self.arquivo_button = self._create_menu_button("Arquivo")
        self.arquivo_menu = QMenu(self)
        self.arquivo_menu.setStyleSheet("""
            QMenu {
                background-color: #0a0a23;
                color: #ffffff;
                border: 1px solid #1e1e3f;
                border-radius: 5px;
            }
            
            QMenu::item {
                padding: 8px 20px;
            }
            
            QMenu::item:selected {
                background-color: #1e1e3f;
            }
        """)
        
        # Ações do menu Arquivo
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
        
        self.arquivo_button.setMenu(self.arquivo_menu)
        menu_layout.addWidget(self.arquivo_button)
        
        # Menu Tradução
        self.traducao_button = self._create_menu_button("Tradução")
        self.traducao_menu = QMenu(self)
        self.traducao_menu.setStyleSheet(self.arquivo_menu.styleSheet())
        
        # Ações do menu Tradução
        text_to_binary_action = QAction("Texto → Binário", self)
        text_to_binary_action.triggered.connect(self._text_to_binary)
        self.traducao_menu.addAction(text_to_binary_action)
        
        binary_to_text_action = QAction("Binário → Texto", self)
        binary_to_text_action.triggered.connect(self._binary_to_text)
        self.traducao_menu.addAction(binary_to_text_action)
        
        self.traducao_button.setMenu(self.traducao_menu)
        menu_layout.addWidget(self.traducao_button)
        
        # Menu Configurações
        self.config_button = self._create_menu_button("Configurações")
        self.config_menu = QMenu(self)
        self.config_menu.setStyleSheet(self.arquivo_menu.styleSheet())
        
        # Ações do menu Configurações
        theme_action = QAction("Tema", self)
        self.config_menu.addAction(theme_action)
        
        font_action = QAction("Fonte", self)
        self.config_menu.addAction(font_action)
        
        self.config_button.setMenu(self.config_menu)
        menu_layout.addWidget(self.config_button)
        
        # Espaçador
        menu_layout.addStretch()
        
        # Botões de ação
        self.run_button = self._create_action_button("▶ Run", "runButton")
        self.run_button.clicked.connect(self._run_code)
        menu_layout.addWidget(self.run_button)
        
        self.terminal_button = self._create_action_button("⌨ Terminal", "terminalButton")
        self.terminal_button.clicked.connect(self._show_terminal)
        menu_layout.addWidget(self.terminal_button)
        
        self.bugs_button = self._create_action_button("⚠ Bugs", "bugsButton")
        self.bugs_button.clicked.connect(self._show_bugs_panel)
        menu_layout.addWidget(self.bugs_button)
        
        # Espaçador
        menu_layout.addStretch()
        
        # Botões de controle da janela
        self.minimize_button = self._create_window_button("−", self.showMinimized)
        menu_layout.addWidget(self.minimize_button)
        
        self.maximize_button = self._create_window_button("□", self._toggle_maximize)
        menu_layout.addWidget(self.maximize_button)
        
        self.close_button = self._create_window_button("×", self.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffffff;
                border: none;
                padding: 8px 12px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #aa0000;
                border-radius: 5px;
            }
        """)
        menu_layout.addWidget(self.close_button)
        
        return menu_bar
    
    def _create_menu_button(self, text):
        """
        Cria um botão de menu personalizado.
        
        Args:
            text: Texto do botão
            
        Returns:
            Botão de menu
        """
        from PyQt5.QtWidgets import QPushButton
        
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10))
        
        return button
    
    def _create_action_button(self, text, object_name):
        """
        Cria um botão de ação personalizado.
        
        Args:
            text: Texto do botão
            object_name: Nome do objeto para estilização
            
        Returns:
            Botão de ação
        """
        from PyQt5.QtWidgets import QPushButton
        
        button = QPushButton(text)
        button.setObjectName(object_name)
        button.setFont(QFont("Arial", 10, QFont.Bold))
        
        return button
    
    def _create_window_button(self, text, slot):
        """
        Cria um botão de controle da janela.
        
        Args:
            text: Texto do botão
            slot: Função a ser chamada quando o botão for clicado
            
        Returns:
            Botão de controle da janela
        """
        from PyQt5.QtWidgets import QPushButton
        
        button = QPushButton(text)
        button.setFont(QFont("Arial", 10, QFont.Bold))
        button.clicked.connect(slot)
        
        return button
    
    def _toggle_maximize(self):
        """Alterna entre janela maximizada e normal."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    
    def _setup_terminal(self):
        """Configura o terminal estilo Windows."""
        self.terminal = None  # Será criado sob demanda
    
    def _setup_bugs_panel(self):
        """Configura o painel de bugs."""
        self.bugs_panel = None  # Será criado sob demanda
    
    def _apply_modern_dark_theme(self):
        """Aplica o tema escuro moderno à interface."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a23;
                color: #ffffff;
            }
            
            QWidget {
                background-color: #0a0a23;
                color: #ffffff;
            }
            
            QSplitter::handle {
                background-color: #1e1e3f;
                width: 2px;
                height: 2px;
            }
            
            QSplitter::handle:hover {
                background-color: #3e3e5e;
            }
            
            QScrollBar:vertical {
                background-color: #0a0a23;
                width: 14px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #1e1e3f;
                min-height: 20px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #3e3e5e;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #0a0a23;
            }
            
            QScrollBar:horizontal {
                background-color: #0a0a23;
                height: 14px;
                margin: 0px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #1e1e3f;
                min-width: 20px;
                border-radius: 7px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #3e3e5e;
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background-color: #0a0a23;
            }
        """)
    
    def _new_file(self):
        """Cria um novo arquivo."""
        # Muda para o widget de editor
        self.central_stack.setCurrentWidget(self.editor_widget)
        
        # Cria um novo editor
        editor = CodeEditor()
        editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0f0f2d;
                color: #ffffff;
                border: none;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: #2d2d5a;
            }
            
            QPlainTextEdit:focus {
                border: none;
            }
        """)
        
        # Adiciona a aba
        index = self.tabs.addTab(editor, "Sem título")
        self.tabs.setCurrentIndex(index)
        
        # Foca no editor
        editor.setFocus()
        
        # Atualiza a barra de status
        self.status_bar.showMessage("Novo arquivo criado")
    
    def _open_file_dialog(self):
        """Abre um diálogo para selecionar um arquivo."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo", "", "Todos os Arquivos (*)"
        )
        
        if filename:
            self._open_file(filename)
    
    def _open_file(self, filename):
        """
        Abre um arquivo.
        
        Args:
            filename: Caminho do arquivo a ser aberto
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Muda para o widget de editor
            self.central_stack.setCurrentWidget(self.editor_widget)
            
            # Cria um novo editor
            editor = CodeEditor()
            editor.setStyleSheet("""
                QPlainTextEdit {
                    background-color: #0f0f2d;
                    color: #ffffff;
                    border: none;
                    font-family: 'Consolas', 'Courier New', monospace;
                    font-size: 14px;
                    selection-background-color: #2d2d5a;
                }
                
                QPlainTextEdit:focus {
                    border: none;
                }
            """)
            
            # Define o conteúdo
            editor.setPlainText(content)
            
            # Adiciona a aba
            title = os.path.basename(filename)
            index = self.tabs.addTab(editor, title)
            self.tabs.setCurrentIndex(index)
            
            # Armazena o caminho completo como propriedade do editor
            editor.setProperty("filepath", filename)
            
            # Foca no editor
            editor.setFocus()
            
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
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Obtém o caminho do arquivo atual
        filepath = current_editor.property("filepath")
        
        # Se for "Salvar Como" ou se o arquivo não tiver caminho
        if as_new or not filepath:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo", "", "Todos os Arquivos (*)"
            )
            
            if not filename:
                return
            
            filepath = filename
        
        try:
            # Salva o conteúdo
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(current_editor.toPlainText())
            
            # Atualiza o título da aba
            title = os.path.basename(filepath)
            self.tabs.setTabText(self.tabs.currentIndex(), title)
            
            # Armazena o caminho completo como propriedade do editor
            current_editor.setProperty("filepath", filepath)
            
            # Atualiza a barra de status
            self.status_bar.showMessage(f"Arquivo salvo: {filepath}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar o arquivo:\n{str(e)}")
    
    def _close_tab(self, index):
        """
        Fecha uma aba.
        
        Args:
            index: Índice da aba a ser fechada
        """
        # Remove a aba
        self.tabs.removeTab(index)
        
        # Se não houver mais abas, exibe a tela de boas-vindas
        if self.tabs.count() == 0:
            self.central_stack.setCurrentWidget(self.welcome_screen)
        
        # Atualiza a barra de status
        self.status_bar.showMessage("Aba fechada")
    
    def _text_to_binary(self):
        """Converte o texto selecionado para binário."""
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Obtém o texto selecionado ou todo o texto
        cursor = current_editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
        else:
            text = current_editor.toPlainText()
        
        # Converte para binário
        try:
            binary = self.binary_interpreter.converter_para_binario(text)
            
            # Cria um novo arquivo com o resultado
            self._new_file()
            new_editor = self.tabs.currentWidget()
            new_editor.setPlainText(binary)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido para Binário")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para binário:\n{str(e)}")
    
    def _binary_to_text(self):
        """Converte o código binário para texto."""
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Obtém o texto selecionado ou todo o texto
        cursor = current_editor.textCursor()
        if cursor.hasSelection():
            binary = cursor.selectedText()
        else:
            binary = current_editor.toPlainText()
        
        # Converte para texto
        try:
            text = self.binary_interpreter.traduzir_binario(binary)
            
            # Cria um novo arquivo com o resultado
            self._new_file()
            new_editor = self.tabs.currentWidget()
            new_editor.setPlainText(text)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido para Texto")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter para texto:\n{str(e)}")
    
    def _run_code(self):
        """Executa o código atual."""
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Obtém o código
        code = current_editor.toPlainText()
        
        # Executa o código usando o executor aprimorado
        try:
            result = self.code_executor.execute_binary_code(code)
            
            # Exibe o resultado no terminal
            self._show_terminal(result)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao executar o código:\n{str(e)}")
    
    def _show_terminal(self, initial_text=None):
        """
        Exibe o terminal.
        
        Args:
            initial_text: Texto inicial a ser exibido no terminal
        """
        # Cria o terminal se não existir
        if not self.terminal:
            try:
                self.terminal = WindowsStyleTerminal(self)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar o terminal:\n{str(e)}")
                return
        
        # Define o texto inicial se fornecido
        if initial_text:
            self.terminal.output_area.clear()
            self.terminal.output_area.insertPlainText(initial_text)
        
        # Exibe o terminal
        self.terminal.show()
        self.terminal.raise_()
        self.terminal.activateWindow()
    
    def _show_bugs_panel(self):
        """Exibe o painel de bugs."""
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            QMessageBox.information(self, "Aviso", "Não há código aberto para analisar.")
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Obtém o código
        code = current_editor.toPlainText()
        
        # Cria o painel de bugs se não existir
        if not self.bugs_panel:
            self.bugs_panel = BugsPanel(self)
            self.bugs_panel.navigate_to_error.connect(self._navigate_to_error)
            self.bugs_panel.fix_error.connect(self._fix_error)
        
        # Analisa o código em busca de bugs
        bugs = self._analyze_code_for_bugs(code)
        
        # Define os bugs no painel
        self.bugs_panel.set_bugs(bugs)
        
        # Exibe o painel
        self.bugs_panel.show()
        self.bugs_panel.raise_()
        self.bugs_panel.activateWindow()
    
    def _analyze_code_for_bugs(self, code):
        """
        Analisa o código em busca de bugs.
        
        Args:
            code: Código a ser analisado
            
        Returns:
            Lista de bugs no formato [(tipo, linha, coluna, mensagem, descrição, sugestão)]
        """
        bugs = []
        
        # Verifica se o código está vazio
        if not code.strip():
            return bugs
        
        # Valida o código binário
        valid, error_msg = self.binary_interpreter.validar_codigo_binario(code)
        if not valid:
            bugs.append((
                "Erro",
                1,
                1,
                "Código binário inválido",
                error_msg,
                "Corrija os tokens binários inválidos para que tenham 8 dígitos."
            ))
            return bugs
        
        # Analisa cada linha do código
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Ignora linhas vazias e comentários
            if not line or line.startswith('//'):
                continue
            
            # Verifica tokens binários incompletos
            tokens = line.split()
            for j, token in enumerate(tokens):
                if token.startswith('//'):
                    break
                
                if all(c in '01' for c in token) and len(token) != 8:
                    bugs.append((
                        "Erro",
                        i + 1,
                        line.find(token) + 1,
                        f"Token binário inválido: '{token}'",
                        f"O token '{token}' tem {len(token)} dígitos, mas deveria ter 8.",
                        f"Corrija para um token binário válido de 8 dígitos."
                    ))
            
            # Verifica tokens binários desconhecidos
            for j, token in enumerate(tokens):
                if token.startswith('//'):
                    break
                
                if all(c in '01' for c in token) and len(token) == 8:
                    if token not in self.binary_interpreter.binary_to_text:
                        bugs.append((
                            "Aviso",
                            i + 1,
                            line.find(token) + 1,
                            f"Token binário desconhecido: '{token}'",
                            f"O token '{token}' não está definido no dicionário de tradução.",
                            f"Verifique se o token está correto ou adicione-o ao dicionário."
                        ))
        
        return bugs
    
    def _navigate_to_error(self, line, column):
        """
        Navega para a posição do erro.
        
        Args:
            line: Número da linha (baseado em 1)
            column: Número da coluna (baseado em 1)
        """
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            return
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Ajusta para índices baseados em 0
        line_index = line - 1
        column_index = column - 1
        
        # Cria um cursor na posição do erro
        cursor = current_editor.textCursor()
        cursor.movePosition(cursor.Start)
        cursor.movePosition(cursor.Down, cursor.MoveAnchor, line_index)
        cursor.movePosition(cursor.Right, cursor.MoveAnchor, column_index)
        
        # Define o cursor no editor
        current_editor.setTextCursor(cursor)
        
        # Garante que a linha seja visível
        current_editor.centerCursor()
        
        # Foca no editor
        current_editor.setFocus()
    
    def _fix_error(self, line, column, suggestion):
        """
        Corrige um erro no código.
        
        Args:
            line: Número da linha (baseado em 1)
            column: Número da coluna (baseado em 1)
            suggestion: Sugestão de correção
        """
        # Implementação a ser adicionada
        pass
    
    def _insert_binary_code(self, code):
        """
        Insere código binário no editor atual.
        
        Args:
            code: Código binário a ser inserido (já com espaço adicionado)
        """
        # Verifica se há abas abertas
        if self.tabs.count() == 0:
            self._new_file()
        
        # Obtém o editor atual
        current_editor = self.tabs.currentWidget()
        if not current_editor:
            return
        
        # Insere o código na posição atual do cursor
        cursor = current_editor.textCursor()
        cursor.insertText(code)
        
        # Define o cursor no editor
        current_editor.setTextCursor(cursor)
        
        # Foca no editor
        current_editor.setFocus()
    
    def closeEvent(self, event):
        """
        Manipula o evento de fechamento da janela.
        
        Args:
            event: Evento de fechamento
        """
        # Pergunta ao usuário se deseja salvar as alterações
        if self.tabs.count() > 0:
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
    window = ModernMainWindow()
    window.show()
    sys.exit(app.exec_())
