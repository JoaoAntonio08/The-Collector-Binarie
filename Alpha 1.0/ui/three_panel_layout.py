"""
Módulo para implementação do layout de três painéis (navegador, editor, guia).
Este módulo fornece a estrutura base para o layout moderno do The Collector Binarie.
"""

from PyQt5.QtWidgets import (
    QWidget, QSplitter, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette

class ThreePanelLayout(QWidget):
    """
    Widget que implementa o layout de três painéis para a interface principal.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa o layout de três painéis.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Configurações de estilo
        self.setObjectName("threePanelLayout")
        self.setStyleSheet("""
            #threePanelLayout {
                background-color: #0a0a23;
                border-radius: 10px;
            }
            
            QSplitter::handle {
                background-color: #1e1e3f;
                width: 2px;
                height: 2px;
            }
            
            QSplitter::handle:hover {
                background-color: #3e3e5e;
            }
            
            QFrame {
                background-color: #0f0f2d;
                border-radius: 10px;
                border: 1px solid #1e1e3f;
            }
            
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
        """)
        
        # Configura o layout
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do layout de três painéis."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(0)
        
        # Splitter principal para dividir os três painéis
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(2)
        self.main_splitter.setChildrenCollapsible(False)
        
        # Painel esquerdo (navegador de arquivos)
        self.left_panel = self._create_panel("Navegador de Arquivos")
        self.main_splitter.addWidget(self.left_panel)
        
        # Painel central (editor de código)
        self.center_panel = self._create_panel("Editor de Código")
        self.main_splitter.addWidget(self.center_panel)
        
        # Painel direito (guia de referência)
        self.right_panel = self._create_panel("Guia de Referência")
        self.main_splitter.addWidget(self.right_panel)
        
        # Define as proporções iniciais (20% - 60% - 20%)
        self.main_splitter.setSizes([200, 600, 200])
        
        # Adiciona o splitter ao layout principal
        main_layout.addWidget(self.main_splitter)
    
    def _create_panel(self, title):
        """
        Cria um painel com título.
        
        Args:
            title: Título do painel
            
        Returns:
            QFrame contendo o painel
        """
        # Cria um frame para o painel
        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)
        panel.setFrameShadow(QFrame.Raised)
        panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Layout do painel
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(5, 5, 5, 5)
        panel_layout.setSpacing(5)
        
        # Título do painel (comentado para seguir o design da referência)
        # title_label = QLabel(title)
        # title_label.setAlignment(Qt.AlignCenter)
        # title_label.setFont(QFont("Arial", 10, QFont.Bold))
        # panel_layout.addWidget(title_label)
        
        # Área de conteúdo
        content_area = QWidget()
        content_area.setObjectName(f"{title.lower().replace(' ', '_')}_content")
        
        # Layout da área de conteúdo
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Adiciona a área de conteúdo ao painel
        panel_layout.addWidget(content_area)
        
        # Armazena o layout da área de conteúdo como atributo do painel
        panel.content_layout = content_layout
        
        return panel
    
    def set_left_panel_widget(self, widget):
        """
        Define o widget do painel esquerdo.
        
        Args:
            widget: Widget a ser adicionado ao painel esquerdo
        """
        self._set_panel_widget(self.left_panel, widget)
    
    def set_center_panel_widget(self, widget):
        """
        Define o widget do painel central.
        
        Args:
            widget: Widget a ser adicionado ao painel central
        """
        self._set_panel_widget(self.center_panel, widget)
    
    def set_right_panel_widget(self, widget):
        """
        Define o widget do painel direito.
        
        Args:
            widget: Widget a ser adicionado ao painel direito
        """
        self._set_panel_widget(self.right_panel, widget)
    
    def _set_panel_widget(self, panel, widget):
        """
        Define o widget de um painel.
        
        Args:
            panel: Painel a receber o widget
            widget: Widget a ser adicionado
        """
        # Limpa o layout atual
        while panel.content_layout.count():
            item = panel.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Adiciona o novo widget
        panel.content_layout.addWidget(widget)
    
    def get_panel_sizes(self):
        """
        Obtém os tamanhos atuais dos painéis.
        
        Returns:
            Lista com os tamanhos dos painéis
        """
        return self.main_splitter.sizes()
    
    def set_panel_sizes(self, sizes):
        """
        Define os tamanhos dos painéis.
        
        Args:
            sizes: Lista com os tamanhos dos painéis [esquerdo, central, direito]
        """
        self.main_splitter.setSizes(sizes)
