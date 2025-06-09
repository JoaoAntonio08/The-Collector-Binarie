"""
Módulo para destacar erros de sintaxe no código binário em tempo real.
Este módulo implementa um sistema de validação e destaque de erros
que se integra ao editor de código para fornecer feedback visual imediato.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QListWidgetItem, QSplitter, QTextEdit
)
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat, QBrush, QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

from binary_syntax_parser import BinarySyntaxParser

class ErrorHighlighter:
    """
    Classe para destacar erros de sintaxe no editor de código.
    """
    
    def __init__(self, editor):
        """
        Inicializa o destacador de erros.
        
        Args:
            editor: Editor de código (QPlainTextEdit ou similar)
        """
        self.editor = editor
        self.parser = BinarySyntaxParser()
        
        # Lista de erros atuais
        self.current_errors = []
        
        # Formato para destacar erros
        self.error_format = QTextCharFormat()
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        self.error_format.setUnderlineColor(QColor("#ff5555"))
        self.error_format.setBackground(QBrush(QColor(255, 85, 85, 30)))
        
        # Timer para validação com delay
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate_code)
        
        # Conecta ao sinal de mudança de texto
        self.editor.textChanged.connect(self.schedule_validation)
    
    def schedule_validation(self):
        """Agenda a validação do código com um pequeno delay."""
        self.validation_timer.start(500)  # 500ms de delay
    
    def validate_code(self):
        """Valida o código e destaca os erros."""
        # Limpa os destaques anteriores
        self.clear_highlights()
        
        # Obtém o código atual
        code = self.editor.toPlainText()
        
        # Valida a sintaxe
        self.current_errors = self.parser.validate_binary_syntax(code)
        
        # Destaca os erros
        self.highlight_errors()
    
    def clear_highlights(self):
        """Limpa todos os destaques de erro."""
        # Remove as seleções extras
        self.editor.setExtraSelections([])
    
    def highlight_errors(self):
        """Destaca os erros no editor."""
        if not self.current_errors:
            return
        
        # Lista de seleções extras
        extra_selections = []
        
        # Para cada erro, cria uma seleção
        for line_num, error_msg in self.current_errors:
            # Ajusta para índice baseado em 0
            line_index = line_num - 1
            
            # Obtém o bloco de texto da linha com erro
            block = self.editor.document().findBlockByLineNumber(line_index)
            if not block.isValid():
                continue
            
            # Cria uma seleção para a linha inteira
            selection = QTextEdit.ExtraSelection()
            selection.format = self.error_format
            selection.format.setToolTip(error_msg)
            
            # Posiciona o cursor no início da linha
            cursor = QTextCursor(block)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            
            selection.cursor = cursor
            extra_selections.append(selection)
        
        # Aplica as seleções
        self.editor.setExtraSelections(extra_selections)
    
    def get_errors(self):
        """
        Retorna a lista de erros atuais.
        
        Returns:
            Lista de tuplas (linha, mensagem de erro)
        """
        return self.current_errors


class ErrorPanel(QWidget):
    """
    Painel para exibir erros de sintaxe encontrados no código.
    """
    
    # Sinal emitido quando um erro é clicado
    error_selected = pyqtSignal(int)  # linha do erro
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configura a interface
        self._setup_ui()
        
        # Lista de erros atuais
        self.errors = []
    
    def _setup_ui(self):
        """Configura a interface do painel de erros."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título do painel
        title_layout = QHBoxLayout()
        title_label = QLabel("Erros de Sintaxe")
        title_label.setStyleSheet("""
            QLabel {
                color: #ff5555;
                font-weight: bold;
                padding: 5px;
            }
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Lista de erros
        self.error_list = QListWidget()
        self.error_list.setStyleSheet("""
            QListWidget {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #44475a;
            }
        """)
        self.error_list.itemClicked.connect(self._on_error_clicked)
        
        # Adiciona widgets ao layout
        layout.addLayout(title_layout)
        layout.addWidget(self.error_list)
    
    def update_errors(self, errors):
        """
        Atualiza a lista de erros exibidos.
        
        Args:
            errors: Lista de tuplas (linha, mensagem de erro)
        """
        self.errors = errors
        self.error_list.clear()
        
        if not errors:
            self.error_list.addItem("Nenhum erro encontrado")
            return
        
        # Adiciona cada erro à lista
        for line_num, error_msg in errors:
            item = QListWidgetItem(f"Linha {line_num}: {error_msg}")
            item.setForeground(QBrush(QColor("#ff5555")))
            self.error_list.addItem(item)
    
    def _on_error_clicked(self, item):
        """
        Manipula o clique em um item da lista de erros.
        
        Args:
            item: Item clicado
        """
        # Obtém o índice do item
        index = self.error_list.row(item)
        
        # Se não houver erros, retorna
        if not self.errors:
            return
        
        # Obtém a linha do erro
        line_num = self.errors[index][0]
        
        # Emite o sinal com a linha do erro
        self.error_selected.emit(line_num)


class CodeValidationWidget(QWidget):
    """
    Widget que combina o editor de código com o painel de erros.
    """
    
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        
        # Editor de código
        self.editor = editor
        
        # Destacador de erros
        self.error_highlighter = ErrorHighlighter(editor)
        
        # Configura a interface
        self._setup_ui()
        
        # Conecta sinais
        self.error_highlighter.validation_timer.timeout.connect(self._update_error_panel)
        self.error_panel.error_selected.connect(self._go_to_error_line)
    
    def _setup_ui(self):
        """Configura a interface do widget de validação."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Splitter para dividir o editor e o painel de erros
        splitter = QSplitter(Qt.Vertical)
        
        # Adiciona o editor ao splitter
        splitter.addWidget(self.editor)
        
        # Painel de erros
        self.error_panel = ErrorPanel()
        splitter.addWidget(self.error_panel)
        
        # Define proporções iniciais (70% editor, 30% painel de erros)
        splitter.setSizes([700, 300])
        
        # Adiciona o splitter ao layout
        layout.addWidget(splitter)
    
    def _update_error_panel(self):
        """Atualiza o painel de erros com os erros atuais."""
        errors = self.error_highlighter.get_errors()
        self.error_panel.update_errors(errors)
    
    def _go_to_error_line(self, line_num):
        """
        Move o cursor para a linha com erro.
        
        Args:
            line_num: Número da linha (baseado em 1)
        """
        # Ajusta para índice baseado em 0
        line_index = line_num - 1
        
        # Obtém o bloco de texto da linha
        block = self.editor.document().findBlockByLineNumber(line_index)
        if not block.isValid():
            return
        
        # Cria um cursor na posição do bloco
        cursor = QTextCursor(block)
        
        # Define o cursor no editor
        self.editor.setTextCursor(cursor)
        
        # Garante que a linha seja visível
        self.editor.centerCursor()
        
        # Foca no editor
        self.editor.setFocus()
    
    def validate_code(self):
        """Força a validação do código."""
        self.error_highlighter.validate_code()
        self._update_error_panel()
