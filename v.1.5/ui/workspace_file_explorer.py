"""
Módulo para implementação do painel de navegação de arquivos estilo workspace.
Este módulo fornece uma interface para navegação e gerenciamento de arquivos e pastas
dentro de um workspace específico, similar ao VSCode.
"""

import os
import shutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTreeView, QFileSystemModel, QFrame, QLineEdit, QMenu,
    QAction, QToolButton, QSizePolicy, QInputDialog, QMessageBox,
    QFileDialog
)
from PyQt5.QtCore import Qt, QDir, QModelIndex, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QColor

class WorkspaceFileExplorer(QWidget):
    """
    Painel de navegação de arquivos e pastas em estilo workspace.
    """
    
    # Sinais
    file_selected = pyqtSignal(str)  # Emitido quando um arquivo é selecionado
    file_opened = pyqtSignal(str)    # Emitido quando um arquivo é aberto
    
    def __init__(self, parent=None):
        """
        Inicializa o painel de navegação de arquivos.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações de estilo
        self.setObjectName("workspaceFileExplorer")
        self.setStyleSheet("""
            #workspaceFileExplorer {
                background-color: #181a20;
                border-radius: 14px;
            }
            QTreeView {
                background-color: #181a20;
                border: none;
                color: #e6e6e6;
                font-size: 14px;
            }
            QTreeView::item {
                padding: 6px;
                border-radius: 6px;
            }
            QTreeView::item:selected {
                background-color: #2d2d5a;
            }
            QTreeView::item:hover {
                background-color: #23272e;
            }
            QPushButton {
                background-color: #bd93f9;
                color: #23272e;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #a882e6;
            }
            QLabel {
                color: #bd93f9;
                font-weight: bold;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #23272e;
                color: #e6e6e6;
                border-radius: 10px;
                padding: 8px;
                border: 1px solid #bd93f9;
                font-size: 15px;
            }
        """)
        
        # Inicializa variáveis
        self.current_workspace = None
        
        # Configura o layout
        self._setup_ui()
        
        # Inicializa o modelo de sistema de arquivos
        self._setup_file_system_model()
    
    def _setup_ui(self):
        """Configura a interface do painel de navegação."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Área de cabeçalho
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)
        
        # Título do painel
        self.title_label = QLabel("Arquivos")
        self.title_label.setFont(QFont("Arial", 10, QFont.Bold))
        header_layout.addWidget(self.title_label)
        
        # Botão de atualização
        self.refresh_button = QToolButton()
        self.refresh_button.setText("⟳")
        self.refresh_button.setToolTip("Atualizar")
        self.refresh_button.clicked.connect(self._refresh_view)
        header_layout.addWidget(self.refresh_button)
        
        # Adiciona o cabeçalho ao layout principal
        main_layout.addLayout(header_layout)
        
        # Botão para abrir workspace
        self.open_workspace_button = QPushButton("Abrir Workspace")
        self.open_workspace_button.clicked.connect(self._open_workspace)
        main_layout.addWidget(self.open_workspace_button)
        
        # Campo de pesquisa
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Pesquisar arquivos...")
        self.search_field.textChanged.connect(self._filter_files)
        main_layout.addWidget(self.search_field)
        
        # Árvore de arquivos
        self.file_tree = QTreeView()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setAnimated(True)
        self.file_tree.setIndentation(15)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setEditTriggers(QTreeView.NoEditTriggers)
        self.file_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self._show_context_menu)
        self.file_tree.clicked.connect(self._on_item_clicked)
        self.file_tree.doubleClicked.connect(self._on_item_double_clicked)
        main_layout.addWidget(self.file_tree)
        
        # Área de botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)
        
        # Botão para criar nova pasta
        self.new_folder_button = QPushButton("Nova Pasta")
        self.new_folder_button.clicked.connect(self._create_new_folder)
        buttons_layout.addWidget(self.new_folder_button)
        
        # Botão para criar novo arquivo
        self.new_file_button = QPushButton("Novo Arquivo")
        self.new_file_button.clicked.connect(self._create_new_file)
        buttons_layout.addWidget(self.new_file_button)
        
        # Adiciona os botões ao layout principal
        main_layout.addLayout(buttons_layout)
    
    def _setup_file_system_model(self):
        """Configura o modelo de sistema de arquivos."""
        self.file_model = QFileSystemModel()
        self.file_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        
        # Define o modelo na árvore
        self.file_tree.setModel(self.file_model)
        
        # Oculta colunas desnecessárias
        for i in range(1, self.file_model.columnCount()):
            self.file_tree.hideColumn(i)
        
        # Inicialmente, não há workspace aberto
        self.file_tree.setRootIndex(QModelIndex())
    
    def _open_workspace(self):
        """Abre um diretório como workspace."""
        directory = QFileDialog.getExistingDirectory(
            self, "Selecionar Workspace", 
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if directory:
            self.set_workspace(directory)
    
    def set_workspace(self, path):
        """
        Define o diretório do workspace.
        
        Args:
            path: Caminho do diretório do workspace
        """
        if not os.path.exists(path):
            QMessageBox.warning(self, "Aviso", f"O diretório {path} não existe.")
            return
        
        self.current_workspace = path
        self.file_model.setRootPath(path)
        self.file_tree.setRootIndex(self.file_model.index(path))
        self.title_label.setText(f"Workspace: {os.path.basename(path)}")
    
    def _refresh_view(self):
        """Atualiza a visualização da árvore de arquivos."""
        if self.current_workspace:
            self.file_model.setRootPath(self.current_workspace)
            self.file_tree.setRootIndex(self.file_model.index(self.current_workspace))
    
    def _filter_files(self, text):
        """
        Filtra os arquivos com base no texto de pesquisa.
        
        Args:
            text: Texto de pesquisa
        """
        if not text:
            self.file_model.setNameFilters([])
        else:
            self.file_model.setNameFilters([f"*{text}*"])
        self.file_model.setNameFilterDisables(False)
    
    def _on_item_clicked(self, index):
        """
        Manipula o clique em um item da árvore.
        
        Args:
            index: Índice do item clicado
        """
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            # Se for um diretório, não faz nada especial
            pass
        else:
            # Se for um arquivo, emite o sinal de seleção
            self.file_selected.emit(path)
    
    def _on_item_double_clicked(self, index):
        """
        Manipula o duplo clique em um item da árvore.
        
        Args:
            index: Índice do item clicado
        """
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            # Se for um diretório, expande ou colapsa
            if self.file_tree.isExpanded(index):
                self.file_tree.collapse(index)
            else:
                self.file_tree.expand(index)
        else:
            # Se for um arquivo, emite o sinal de abertura
            self.file_opened.emit(path)
    
    def _show_context_menu(self, position):
        """
        Exibe o menu de contexto para o item selecionado.
        
        Args:
            position: Posição do clique
        """
        if not self.current_workspace:
            return
            
        index = self.file_tree.indexAt(position)
        
        # Cria o menu de contexto
        context_menu = QMenu(self)
        
        if index.isValid():
            path = self.file_model.filePath(index)
            is_dir = self.file_model.isDir(index)
            
            if is_dir:
                # Ações para diretórios
                open_action = QAction("Abrir", self)
                open_action.triggered.connect(lambda: self._expand_directory(index))
                context_menu.addAction(open_action)
                
                new_file_action = QAction("Novo Arquivo", self)
                new_file_action.triggered.connect(lambda: self._create_new_file(path))
                context_menu.addAction(new_file_action)
                
                new_folder_action = QAction("Nova Pasta", self)
                new_folder_action.triggered.connect(lambda: self._create_new_folder(path))
                context_menu.addAction(new_folder_action)
            else:
                # Ações para arquivos
                open_action = QAction("Abrir", self)
                open_action.triggered.connect(lambda: self.file_opened.emit(path))
                context_menu.addAction(open_action)
            
            # Ações comuns
            context_menu.addSeparator()
            
            rename_action = QAction("Renomear", self)
            rename_action.triggered.connect(lambda: self._rename_item(index))
            context_menu.addAction(rename_action)
            
            delete_action = QAction("Excluir", self)
            delete_action.triggered.connect(lambda: self._delete_item(index))
            context_menu.addAction(delete_action)
        else:
            # Menu de contexto para área vazia
            new_file_action = QAction("Novo Arquivo", self)
            new_file_action.triggered.connect(lambda: self._create_new_file(self.current_workspace))
            context_menu.addAction(new_file_action)
            
            new_folder_action = QAction("Nova Pasta", self)
            new_folder_action.triggered.connect(lambda: self._create_new_folder(self.current_workspace))
            context_menu.addAction(new_folder_action)
        
        # Exibe o menu
        context_menu.exec_(self.file_tree.viewport().mapToGlobal(position))
    
    def _expand_directory(self, index):
        """
        Expande um diretório na árvore.
        
        Args:
            index: Índice do diretório
        """
        self.file_tree.expand(index)
    
    def _create_new_file(self, parent_path=None):
        """
        Cria um novo arquivo.
        
        Args:
            parent_path: Caminho do diretório pai (opcional)
        """
        if not self.current_workspace:
            QMessageBox.warning(self, "Aviso", "Nenhum workspace aberto.")
            return
            
        if not parent_path:
            parent_path = self.current_workspace
            
        file_name, ok = QInputDialog.getText(
            self, "Novo Arquivo", "Nome do arquivo:"
        )
        
        if ok and file_name:
            file_path = os.path.join(parent_path, file_name)
            
            # Verifica se o arquivo já existe
            if os.path.exists(file_path):
                QMessageBox.warning(self, "Aviso", f"O arquivo {file_name} já existe.")
                return
                
            try:
                # Cria o arquivo vazio
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass
                    
                # Atualiza a visualização
                self._refresh_view()
                
                # Emite o sinal de abertura do arquivo
                self.file_opened.emit(file_path)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar o arquivo:\n{str(e)}")
    
    def _create_new_folder(self, parent_path=None):
        """
        Cria uma nova pasta.
        
        Args:
            parent_path: Caminho do diretório pai (opcional)
        """
        if not self.current_workspace:
            QMessageBox.warning(self, "Aviso", "Nenhum workspace aberto.")
            return
            
        if not parent_path:
            parent_path = self.current_workspace
            
        folder_name, ok = QInputDialog.getText(
            self, "Nova Pasta", "Nome da pasta:"
        )
        
        if ok and folder_name:
            folder_path = os.path.join(parent_path, folder_name)
            
            # Verifica se a pasta já existe
            if os.path.exists(folder_path):
                QMessageBox.warning(self, "Aviso", f"A pasta {folder_name} já existe.")
                return
                
            try:
                # Cria a pasta
                os.makedirs(folder_path)
                
                # Atualiza a visualização
                self._refresh_view()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar a pasta:\n{str(e)}")
    
    def _rename_item(self, index):
        """
        Renomeia um item.
        
        Args:
            index: Índice do item
        """
        if not index.isValid():
            return
            
        path = self.file_model.filePath(index)
        old_name = os.path.basename(path)
        parent_dir = os.path.dirname(path)
        
        new_name, ok = QInputDialog.getText(
            self, "Renomear", "Novo nome:", text=old_name
        )
        
        if ok and new_name and new_name != old_name:
            new_path = os.path.join(parent_dir, new_name)
            
            # Verifica se o novo nome já existe
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Aviso", f"Já existe um item com o nome {new_name}.")
                return
                
            try:
                # Renomeia o item
                os.rename(path, new_path)
                
                # Atualiza a visualização
                self._refresh_view()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao renomear:\n{str(e)}")
    
    def _delete_item(self, index):
        """
        Exclui um item.
        
        Args:
            index: Índice do item
        """
        if not index.isValid():
            return
            
        path = self.file_model.filePath(index)
        name = os.path.basename(path)
        is_dir = self.file_model.isDir(index)
        
        # Confirmação
        if is_dir:
            message = f"Tem certeza que deseja excluir a pasta '{name}' e todo o seu conteúdo?"
        else:
            message = f"Tem certeza que deseja excluir o arquivo '{name}'?"
            
        reply = QMessageBox.question(
            self, "Confirmar Exclusão", message,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Exclui o item
                if is_dir:
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                    
                # Atualiza a visualização
                self._refresh_view()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir:\n{str(e)}")
