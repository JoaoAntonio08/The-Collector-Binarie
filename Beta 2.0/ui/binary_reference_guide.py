"""
Módulo para implementação da guia de referência de códigos binários.
Este módulo fornece uma interface para consulta rápida de códigos binários disponíveis.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGridLayout, QToolButton, QSizePolicy,
    QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QIcon

class BinaryReferenceGuide(QWidget):
    """
    Painel de guia de referência para códigos binários.
    """
    
    # Sinais
    code_selected = pyqtSignal(str)  # Emitido quando um código é selecionado
    
    def __init__(self, parent=None):
        """
        Inicializa o painel de guia de referência.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações de estilo
        self.setObjectName("binaryReferenceGuide")
        self.setStyleSheet("""
            #binaryReferenceGuide {
                background-color: #0f0f2d;
                border-radius: 10px;
            }
            
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
            
            QTreeWidget {
                background-color: #0f0f2d;
                border: none;
                color: #ffffff;
                font-size: 12px;
            }
            
            QTreeWidget::item {
                padding: 4px;
                border-radius: 4px;
            }
            
            QTreeWidget::item:selected {
                background-color: #2d2d5a;
            }
            
            QTreeWidget::item:hover {
                background-color: #1e1e3f;
            }
            
            QScrollArea {
                border: none;
                background-color: transparent;
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
        """)
        
        # Dados de referência
        self.reference_data = self._get_reference_data()
        
        # Configura o layout
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do painel de guia de referência."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Título do painel
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        self.title_label = QLabel("Guia")
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        main_layout.addLayout(title_layout)
        
        # Árvore de referência
        self.reference_tree = QTreeWidget()
        self.reference_tree.setHeaderHidden(True)
        self.reference_tree.setAnimated(True)
        self.reference_tree.setIndentation(15)
        self.reference_tree.setColumnCount(1)
        self.reference_tree.itemClicked.connect(self._on_item_clicked)
        
        # Preenche a árvore com os dados de referência
        self._populate_reference_tree()
        
        main_layout.addWidget(self.reference_tree)
    
    def _get_reference_data(self):
        """
        Obtém os dados de referência para códigos binários.
        
        Returns:
            Dicionário com categorias e códigos binários
        """
        return {
            "Numerais ↓": {
                "0": "00110000",
                "1": "00110001",
                "2": "00110010",
                "3": "00110011",
                "4": "00110100",
                "5": "00110101",
                "6": "00110110",
                "7": "00110111",
                "8": "00111000",
                "9": "00111001"
            },
            "Letras Maiúsculas ↓": {
                "A": "01000001",
                "B": "01000010",
                "C": "01000011",
                "D": "01000100",
                "E": "01000101",
                "F": "01000110",
                "G": "01000111",
                "H": "01001000",
                "I": "01001001",
                "J": "01001010",
                "K": "01001011",
                "L": "01001100",
                "M": "01001101",
                "N": "01001110",
                "O": "01001111",
                "P": "01010000",
                "Q": "01010001",
                "R": "01010010",
                "S": "01010011",
                "T": "01010100",
                "U": "01010101",
                "V": "01010110",
                "W": "01010111",
                "X": "01011000",
                "Y": "01011001",
                "Z": "01011010"
            },
            "Letras Minúsculas ↓": {
                "a": "01100001",
                "b": "01100010",
                "c": "01100011",
                "d": "01100100",
                "e": "01100101",
                "f": "01100110",
                "g": "01100111",
                "h": "01101000",
                "i": "01101001",
                "j": "01101010",
                "k": "01101011",
                "l": "01101100",
                "m": "01101101",
                "n": "01101110",
                "o": "01101111",
                "p": "01110000",
                "q": "01110001",
                "r": "01110010",
                "s": "01110011",
                "t": "01110100",
                "u": "01110101",
                "v": "01110110",
                "w": "01110111",
                "x": "01111000",
                "y": "01111001",
                "z": "01111010"
            },
            "Comandos ↓": {
                "var": "01111011",
                "print": "01111100",
                "\"": "01111111",
                "input": "01111110",
                "int": "10000000",
                "float": "10000001",
                "str": "10000010",
                "if": "10000011",
                "else": "10000100",
                "while": "10000101",
                "for": "10000110",
                "def": "10000111",
                "return": "10001000",
                "=": "10001001",
                "+": "10001010",
                "-": "10001011",
                "*": "10001100",
                "/": "10001101",
                "==": "10001110",
                "(": "00101000",
                ")": "00101001",
                ":": "10010001",
                "print()": "10010010",
                "espaço": "00100000",
                "_": "10010011",
                "{": "10010100",
                "}": "10010101",
                "[": "10010110",
                "]": "10010111",
                "'": "10011000",
                ",": "10011001",
                ".": "10011010",
                ";": "10011011",
                "\\": "10011100",
                "%": "10011101",
                "!": "10011110",
                "<": "10011111",
                ">": "10100000",
                "&": "10100001",
                "|": "10100010"
            }
        }
    
    def _populate_reference_tree(self):
        """Preenche a árvore de referência com os dados."""
        self.reference_tree.clear()
        
        # Cria os itens de categoria
        for category, items in self.reference_data.items():
            category_item = QTreeWidgetItem([category])
            category_item.setFont(0, QFont("Arial", 10, QFont.Bold))
            self.reference_tree.addTopLevelItem(category_item)
            
            # Adiciona os itens da categoria
            for label, code in items.items():
                item = QTreeWidgetItem([f"{label}: {code}"])
                item.setData(0, Qt.UserRole, code)
                category_item.addChild(item)
            
            # Expande a categoria
            category_item.setExpanded(True)
    
    def _on_item_clicked(self, item, column):
        """
        Manipula o clique em um item da árvore.
        
        Args:
            item: Item clicado
            column: Coluna clicada
        """
        # Verifica se é um item de código (não uma categoria)
        if item.parent() is not None:
            code = item.data(0, Qt.UserRole)
            self.code_selected.emit(code)
    
    def update_reference_data(self, new_data):
        """
        Atualiza os dados de referência.
        
        Args:
            new_data: Novos dados de referência
        """
        self.reference_data = new_data
        self._populate_reference_tree()
