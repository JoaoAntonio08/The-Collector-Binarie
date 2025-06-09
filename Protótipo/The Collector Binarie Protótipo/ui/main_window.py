import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox,
    QTabWidget, QToolBar, QStatusBar, QApplication
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.code_editor import CodeEditor
from ui.binario_interpreter import BinarioInterpreter
from ui.binary_runner import BinariosInterpreter
from ui.terminal_popup import TerminalPopup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Collector Binarie")
        self.setGeometry(100, 100, 1000, 700)

        self.binario_interpreter = BinarioInterpreter()  # Para tradução de binário
        self.binarios_interpreter = BinariosInterpreter()  # Para execução de código binário

        # Criação das abas
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        self.setCentralWidget(self.tabs)

        # Barra de ferramentas
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.create_actions()

        # Barra de status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")

        # Menu
        self._create_menu()

        # Primeira aba em branco
        self._new_tab()

        # Estilo escuro
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
            }
            QTabBar::tab:selected {
                background: #44445a;
            }
        """)

    def create_actions(self):
        pass

    def _create_menu(self):
        menubar = self.menuBar()

        # MENU ARQUIVO
        file_menu = menubar.addMenu("Arquivo")

        novo_arquivo = QAction("Novo Arquivo", self)
        novo_arquivo.setShortcut("Ctrl+Shift+N")
        novo_arquivo.triggered.connect(self._new_tab)

        nova_pasta = QAction("Nova Pasta", self)
        nova_pasta.setShortcut("Ctrl+Shift+O")
        nova_pasta.triggered.connect(self._nova_pasta)

        abrir_arquivo = QAction("Abrir Arquivo", self)
        abrir_arquivo.setShortcut("Ctrl+A")
        abrir_arquivo.triggered.connect(self._open_file)

        abrir_pasta = QAction("Abrir Pasta", self)
        abrir_pasta.setShortcut("Ctrl+P")
        abrir_pasta.triggered.connect(self._abrir_pasta)

        salvar = QAction("Salvar", self)
        salvar.setShortcut("Ctrl+S")
        salvar.triggered.connect(self._save_file)

        salvar_como = QAction("Salvar Como", self)
        salvar_como.setShortcut("Ctrl+Shift+S")
        salvar_como.triggered.connect(self._save_file)

        file_menu.addAction(novo_arquivo)
        file_menu.addAction(nova_pasta)
        file_menu.addAction(abrir_arquivo)
        file_menu.addAction(abrir_pasta)
        file_menu.addSeparator()
        file_menu.addAction(salvar)
        file_menu.addAction(salvar_como)

        # MENU TRADUÇÃO
        translate_menu = menubar.addMenu("Tradução")

        texto_para_binario = QAction("Texto → Binário", self)
        texto_para_binario.triggered.connect(self.converter_texto_para_binario)

        binario_para_texto = QAction("Binário → Texto", self)
        binario_para_texto.triggered.connect(self.rodar_codigo_binario)

        translate_menu.addAction(texto_para_binario)
        translate_menu.addAction(binario_para_texto)

        # MENU EXECUÇÃO (Nova linha para Run, Terminal e Bugs)
        exec_menu = menubar.addMenu("Execução")

        run_action = QAction("Run ▶", self)
        run_action.triggered.connect(self.executar_codigo_binario)

        terminal_action = QAction("Terminal", self)
        terminal_action.triggered.connect(lambda: self.abrir_terminal("Terminal vazio"))

        bugs_action = QAction("Bugs 🐞", self)
        bugs_action.triggered.connect(lambda: self.abrir_bugs("Sem erros no momento"))

        exec_menu.addAction(run_action)
        exec_menu.addAction(terminal_action)
        exec_menu.addAction(bugs_action)


    def _nova_pasta(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar local para nova pasta")
        if dir_path:
            nome, ok = QFileDialog.getSaveFileName(self, "Nome da nova pasta", dir_path)
            if nome:
                try:
                    os.makedirs(nome, exist_ok=True)
                    QMessageBox.information(self, "Sucesso", f"Pasta criada em: {nome}")
                except Exception as e:
                    QMessageBox.critical(self, "Erro", f"Não foi possível criar a pasta.\n{e}")

    def _abrir_pasta(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Abrir Pasta")
        if dir_path:
            QMessageBox.information(self, "Pasta Selecionada", f"Caminho: {dir_path}")

    def _new_tab(self, content="", checked=False):
        if isinstance(content, bool):  # Se o primeiro parâmetro for o 'checked', troca por ""
            content = ""
        editor = CodeEditor()
        editor.setPlainText(str(content))
        index = self.tabs.addTab(editor, "Sem título")
        self.tabs.setCurrentIndex(index)
        self.status_bar.showMessage("Nova aba criada", 2000)

    def _close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
            self.status_bar.showMessage("Aba fechada", 2000)
        else:
            QMessageBox.warning(self, "Aviso", "Você não pode fechar a última aba.")

    def get_current_editor(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget, CodeEditor):
            return current_widget
        return None

    def rodar_codigo_binario(self):
        editor = self.get_current_editor()
        if editor is None:
            QMessageBox.warning(self, "Aviso", "Nenhum editor aberto.")
            return

        codigo_binario = editor.toPlainText()
        resultado = self.binario_interpreter.traduzir_binario(codigo_binario)  # Usa BinarioInterpreter
        self._new_tab(resultado)
        self.tabs.setTabText(self.tabs.currentIndex(), "Interpretado")

    def converter_texto_para_binario(self):
        editor = self.get_current_editor()
        if editor is None:
            QMessageBox.warning(self, "Aviso", "Nenhum editor aberto.")
            return

        texto = editor.toPlainText()
        try:
            binario = self.binario_interpreter.converter_para_binario(texto)  # Corrigido para binario_interpreter
            self._new_tab(binario)
            self.tabs.setTabText(self.tabs.currentIndex(), "Convertido")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter texto para binário:\n{e}")

    def executar_codigo_binario(self):
        aba_atual = self.tabs.currentWidget()
        if aba_atual and hasattr(aba_atual, 'toPlainText'):
            binario = aba_atual.toPlainText()
            resultado = self.binarios_interpreter.interpretar(binario)  # Usa BinariosInterpreter
            
            if "Erro" in resultado or not resultado.strip():
                self.abrir_bugs("Comando desconhecido ou erro ao converter binário.")
                return

            saida = self.binarios_interpreter.executar_codigo(resultado)  # Usa BinariosInterpreter
            self.abrir_terminal(saida)
        else:
            self.abrir_bugs("Nenhuma aba válida selecionada.")

    def abrir_terminal(self, saida):
        self.popup_terminal = TerminalPopup(saida)
        self.popup_terminal.exec_()

    def abrir_bugs(self, mensagem):
        self.popup_bugs = TerminalPopup(mensagem)
        self.popup_bugs.setWindowTitle("Bugs")
        self.popup_bugs.exec_()


    def _open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo", "", "Arquivos de Texto (*.txt *.py)")
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self._new_tab(content)
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(filename))
            self.status_bar.showMessage(f"Abrindo: {filename}", 3000)

    def _save_file(self):
        current_editor = self.get_current_editor()
        if not current_editor:
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", "", "Arquivos de Texto (*.txt *.py)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(current_editor.toPlainText())
            self.tabs.setTabText(self.tabs.currentIndex(), os.path.basename(filename))
            self.status_bar.showMessage(f"Salvo em: {filename}", 3000)
