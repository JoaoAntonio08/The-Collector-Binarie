"""
Módulo para implementação do painel de navegação de arquivos.
Este módulo fornece uma interface para navegação e gerenciamento de arquivos e pastas.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTreeView, QFileSystemModel, QFrame, QLineEdit, QMenu,
    QAction, QToolButton, QSizePolicy
)
from PyQt5.QtCore import Qt, QDir, QModelIndex, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QColor

class FileExplorerPanel(QWidget):
    """
    Painel de navegação de arquivos e pastas.
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
        self.setObjectName("fileExplorerPanel")
        self.setStyleSheet("""
            #fileExplorerPanel {
                background-color: #0f0f2d;
                border-radius: 10px;
            }
            
            QTreeView {
                background-color: #0f0f2d;
                border: none;
                color: #ffffff;
                font-size: 14px;
            }
            
            QTreeView::item {
                padding: 4px;
                border-radius: 4px;
            }
            
            QTreeView::item:selected {
                background-color: #2d2d5a;
            }
            
            QTreeView::item:hover {
                background-color: #1e1e3f;
            }
            
            QPushButton {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2d2d5a;
            }
            
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
            
            QLineEdit {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 4px;
                border: 1px solid #2d2d5a;
            }
        """)
        
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
        self.file_model.setRootPath(QDir.homePath())
        self.file_model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)
        
        # Define o modelo na árvore
        self.file_tree.setModel(self.file_model)
        
        # Oculta colunas desnecessárias
        for i in range(1, self.file_model.columnCount()):
            self.file_tree.hideColumn(i)
        
        # Define o diretório raiz
        self.set_root_directory(QDir.homePath())
    
    def set_root_directory(self, path):
        """
        Define o diretório raiz para navegação.
        
        Args:
            path: Caminho do diretório raiz
        """
        index = self.file_model.index(path)
        self.file_tree.setRootIndex(index)
    
    def _refresh_view(self):
        """Atualiza a visualização da árvore de arquivos."""
        current_index = self.file_tree.rootIndex()
        path = self.file_model.filePath(current_index)
        self.file_model.setRootPath(path)
        self.file_tree.setRootIndex(self.file_model.index(path))
    
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
        index = self.file_tree.indexAt(position)
        if not index.isValid():
            return
        
        path = self.file_model.filePath(index)
        is_dir = self.file_model.isDir(index)
        
        # Cria o menu de contexto
        context_menu = QMenu(self)
        
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
        # Implementação a ser adicionada
        pass
    
    def _create_new_folder(self, parent_path=None):
        """
        Cria uma nova pasta.
        
        Args:
            parent_path: Caminho do diretório pai (opcional)
        """
        # Implementação a ser adicionada
        pass
    
    def _rename_item(self, index):
        """
        Renomeia um item.
        
        Args:
            index: Índice do item
        """
        # Implementação a ser adicionada
        pass
    
    def _delete_item(self, index):
        """
        Exclui um item.
        
        Args:
            index: Índice do item
        """
        # Implementação a ser adicionada
        pass
