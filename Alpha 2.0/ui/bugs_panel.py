"""
Módulo para implementação da tela de bugs.
Este módulo fornece uma interface para visualização, navegação e depuração de erros no código binário.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
    QTextEdit, QFrame, QToolButton, QMenu, QAction, QDialog,
    QCheckBox, QGroupBox, QRadioButton, QButtonGroup, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QTextCursor, QTextCharFormat

class BugsPanel(QWidget):
    """
    Painel para visualização e depuração de bugs no código binário.
    """
    
    # Sinais
    navigate_to_error = pyqtSignal(int, int)  # linha, coluna
    fix_error = pyqtSignal(int, int, str)  # linha, coluna, correção
    
    def __init__(self, parent=None):
        """
        Inicializa o painel de bugs.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações de estilo
        self.setObjectName("bugsPanel")
        self.setStyleSheet("""
            #bugsPanel {
                background-color: #0f0f2d;
                border-radius: 10px;
            }
            
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
            
            QTableWidget {
                background-color: #0a0a23;
                color: #ffffff;
                border: 1px solid #1e1e3f;
                gridline-color: #1e1e3f;
                border-radius: 5px;
            }
            
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #1e1e3f;
            }
            
            QTableWidget::item:selected {
                background-color: #2d2d5a;
            }
            
            QHeaderView::section {
                background-color: #1e1e3f;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #2d2d5a;
            }
            
            QTextEdit {
                background-color: #0a0a23;
                color: #ffffff;
                border: 1px solid #1e1e3f;
                border-radius: 5px;
            }
            
            QPushButton {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2d2d5a;
            }
            
            QPushButton#fixButton {
                background-color: #00aa00;
            }
            
            QPushButton#fixButton:hover {
                background-color: #00cc00;
            }
            
            QToolButton {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 4px;
            }
            
            QToolButton:hover {
                background-color: #2d2d5a;
            }
            
            QSplitter::handle {
                background-color: #1e1e3f;
            }
            
            QGroupBox {
                color: #ffffff;
                border: 1px solid #1e1e3f;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            
            QCheckBox, QRadioButton {
                color: #ffffff;
            }
        """)
        
        # Lista de bugs
        self.bugs = []
        
        # Configura a interface
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do painel de bugs."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Título do painel
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        
        self.title_label = QLabel("Bugs e Erros")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_layout.addWidget(self.title_label)
        
        # Botões de ação
        self.refresh_button = QToolButton()
        self.refresh_button.setText("⟳")
        self.refresh_button.setToolTip("Atualizar")
        self.refresh_button.clicked.connect(self._refresh_bugs)
        title_layout.addWidget(self.refresh_button)
        
        self.filter_button = QToolButton()
        self.filter_button.setText("⚙")
        self.filter_button.setToolTip("Filtrar")
        self.filter_button.clicked.connect(self._show_filter_dialog)
        title_layout.addWidget(self.filter_button)
        
        title_layout.addStretch()
        
        # Contador de bugs
        self.bug_count_label = QLabel("0 bugs encontrados")
        title_layout.addWidget(self.bug_count_label)
        
        main_layout.addLayout(title_layout)
        
        # Splitter para dividir a tabela de bugs e os detalhes
        self.splitter = QSplitter(Qt.Vertical)
        
        # Tabela de bugs
        self.bugs_table = QTableWidget()
        self.bugs_table.setColumnCount(4)
        self.bugs_table.setHorizontalHeaderLabels(["Tipo", "Linha", "Coluna", "Mensagem"])
        self.bugs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.bugs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.bugs_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.bugs_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.bugs_table.verticalHeader().setVisible(False)
        self.bugs_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bugs_table.setSelectionMode(QTableWidget.SingleSelection)
        self.bugs_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.bugs_table.itemSelectionChanged.connect(self._on_bug_selected)
        self.splitter.addWidget(self.bugs_table)
        
        # Painel de detalhes do bug
        self.details_frame = QFrame()
        details_layout = QVBoxLayout(self.details_frame)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(5)
        
        # Título dos detalhes
        self.details_title = QLabel("Detalhes do Bug")
        self.details_title.setFont(QFont("Arial", 10, QFont.Bold))
        details_layout.addWidget(self.details_title)
        
        # Descrição do bug
        self.bug_description = QTextEdit()
        self.bug_description.setReadOnly(True)
        self.bug_description.setMaximumHeight(100)
        details_layout.addWidget(self.bug_description)
        
        # Sugestão de correção
        self.fix_suggestion = QTextEdit()
        self.fix_suggestion.setReadOnly(True)
        self.fix_suggestion.setMaximumHeight(100)
        details_layout.addWidget(self.fix_suggestion)
        
        # Botões de ação para o bug selecionado
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        
        self.goto_button = QPushButton("Ir para o Erro")
        self.goto_button.clicked.connect(self._navigate_to_selected_bug)
        buttons_layout.addWidget(self.goto_button)
        
        self.fix_button = QPushButton("Corrigir Automaticamente")
        self.fix_button.setObjectName("fixButton")
        self.fix_button.clicked.connect(self._fix_selected_bug)
        buttons_layout.addWidget(self.fix_button)
        
        details_layout.addLayout(buttons_layout)
        
        self.splitter.addWidget(self.details_frame)
        
        # Define as proporções iniciais (70% tabela, 30% detalhes)
        self.splitter.setSizes([700, 300])
        
        main_layout.addWidget(self.splitter)
        
        # Desabilita os detalhes inicialmente
        self._enable_details(False)
    
    def set_bugs(self, bugs):
        """
        Define a lista de bugs.
        
        Args:
            bugs: Lista de bugs no formato [(tipo, linha, coluna, mensagem, descrição, sugestão)]
        """
        self.bugs = bugs
        self._populate_bugs_table()
        
        # Atualiza o contador de bugs
        self.bug_count_label.setText(f"{len(bugs)} bugs encontrados")
    
    def _populate_bugs_table(self):
        """Preenche a tabela de bugs com os dados atuais."""
        # Limpa a tabela
        self.bugs_table.setRowCount(0)
        
        # Adiciona os bugs
        for i, bug in enumerate(self.bugs):
            tipo, linha, coluna, mensagem, _, _ = bug
            
            self.bugs_table.insertRow(i)
            
            # Tipo
            tipo_item = QTableWidgetItem(tipo)
            if tipo.lower() == "erro":
                tipo_item.setForeground(QColor("#ff5555"))
            elif tipo.lower() == "aviso":
                tipo_item.setForeground(QColor("#ffb86c"))
            else:
                tipo_item.setForeground(QColor("#8be9fd"))
            self.bugs_table.setItem(i, 0, tipo_item)
            
            # Linha
            linha_item = QTableWidgetItem(str(linha))
            self.bugs_table.setItem(i, 1, linha_item)
            
            # Coluna
            coluna_item = QTableWidgetItem(str(coluna))
            self.bugs_table.setItem(i, 2, coluna_item)
            
            # Mensagem
            mensagem_item = QTableWidgetItem(mensagem)
            self.bugs_table.setItem(i, 3, mensagem_item)
    
    def _on_bug_selected(self):
        """Manipula a seleção de um bug na tabela."""
        selected_items = self.bugs_table.selectedItems()
        if not selected_items:
            self._enable_details(False)
            return
        
        # Obtém o índice da linha selecionada
        row = self.bugs_table.row(selected_items[0])
        
        # Obtém os detalhes do bug
        bug = self.bugs[row]
        _, _, _, _, descricao, sugestao = bug
        
        # Atualiza os detalhes
        self.bug_description.setText(descricao)
        self.fix_suggestion.setText(sugestao)
        
        # Habilita os detalhes
        self._enable_details(True)
    
    def _enable_details(self, enabled):
        """
        Habilita ou desabilita o painel de detalhes.
        
        Args:
            enabled: Se True, habilita o painel; caso contrário, desabilita
        """
        self.details_title.setEnabled(enabled)
        self.bug_description.setEnabled(enabled)
        self.fix_suggestion.setEnabled(enabled)
        self.goto_button.setEnabled(enabled)
        self.fix_button.setEnabled(enabled)
    
    def _navigate_to_selected_bug(self):
        """Navega para o bug selecionado."""
        selected_items = self.bugs_table.selectedItems()
        if not selected_items:
            return
        
        # Obtém o índice da linha selecionada
        row = self.bugs_table.row(selected_items[0])
        
        # Obtém os detalhes do bug
        bug = self.bugs[row]
        _, linha, coluna, _, _, _ = bug
        
        # Emite o sinal para navegar para o erro
        self.navigate_to_error.emit(linha, coluna)
    
    def _fix_selected_bug(self):
        """Corrige automaticamente o bug selecionado."""
        selected_items = self.bugs_table.selectedItems()
        if not selected_items:
            return
        
        # Obtém o índice da linha selecionada
        row = self.bugs_table.row(selected_items[0])
        
        # Obtém os detalhes do bug
        bug = self.bugs[row]
        _, linha, coluna, _, _, sugestao = bug
        
        # Emite o sinal para corrigir o erro
        self.fix_error.emit(linha, coluna, sugestao)
    
    def _refresh_bugs(self):
        """Atualiza a lista de bugs."""
        # Este método deve ser implementado pela classe que utiliza o BugsPanel
        pass
    
    def _show_filter_dialog(self):
        """Exibe o diálogo de filtro de bugs."""
        dialog = BugsFilterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Aplica os filtros
            pass


class BugsFilterDialog(QDialog):
    """
    Diálogo para filtrar bugs por tipo e gravidade.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa o diálogo de filtro.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações básicas
        self.setWindowTitle("Filtrar Bugs")
        self.setMinimumWidth(300)
        
        # Configurações de estilo
        self.setStyleSheet("""
            QDialog {
                background-color: #0f0f2d;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
            }
            
            QGroupBox {
                color: #ffffff;
                border: 1px solid #1e1e3f;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            
            QCheckBox, QRadioButton {
                color: #ffffff;
            }
            
            QPushButton {
                background-color: #1e1e3f;
                color: #ffffff;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2d2d5a;
            }
            
            QPushButton#okButton {
                background-color: #00aa00;
            }
            
            QPushButton#okButton:hover {
                background-color: #00cc00;
            }
        """)
        
        # Configura a interface
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do diálogo de filtro."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Grupo de tipos de bug
        self.type_group = QGroupBox("Tipos de Bug")
        type_layout = QVBoxLayout(self.type_group)
        
        self.error_check = QCheckBox("Erros")
        self.error_check.setChecked(True)
        type_layout.addWidget(self.error_check)
        
        self.warning_check = QCheckBox("Avisos")
        self.warning_check.setChecked(True)
        type_layout.addWidget(self.warning_check)
        
        self.info_check = QCheckBox("Informações")
        self.info_check.setChecked(True)
        type_layout.addWidget(self.info_check)
        
        main_layout.addWidget(self.type_group)
        
        # Grupo de gravidade
        self.severity_group = QGroupBox("Gravidade")
        severity_layout = QVBoxLayout(self.severity_group)
        
        self.severity_buttons = QButtonGroup(self)
        
        self.all_radio = QRadioButton("Todos")
        self.all_radio.setChecked(True)
        self.severity_buttons.addButton(self.all_radio)
        severity_layout.addWidget(self.all_radio)
        
        self.high_radio = QRadioButton("Alta")
        self.severity_buttons.addButton(self.high_radio)
        severity_layout.addWidget(self.high_radio)
        
        self.medium_radio = QRadioButton("Média")
        self.severity_buttons.addButton(self.medium_radio)
        severity_layout.addWidget(self.medium_radio)
        
        self.low_radio = QRadioButton("Baixa")
        self.severity_buttons.addButton(self.low_radio)
        severity_layout.addWidget(self.low_radio)
        
        main_layout.addWidget(self.severity_group)
        
        # Botões de ação
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(10)
        
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)
        
        self.ok_button = QPushButton("Aplicar")
        self.ok_button.setObjectName("okButton")
        self.ok_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.ok_button)
        
        main_layout.addLayout(buttons_layout)
    
    def get_filters(self):
        """
        Obtém os filtros selecionados.
        
        Returns:
            Dicionário com os filtros
        """
        return {
            "types": {
                "error": self.error_check.isChecked(),
                "warning": self.warning_check.isChecked(),
                "info": self.info_check.isChecked()
            },
            "severity": {
                "all": self.all_radio.isChecked(),
                "high": self.high_radio.isChecked(),
                "medium": self.medium_radio.isChecked(),
                "low": self.low_radio.isChecked()
            }
        }
