"""
Módulo para gerenciamento de temas da aplicação.
Implementa os temas Dark, White e Dark Blue.
"""

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt

class ThemeManager:
    """
    Gerenciador de temas para a aplicação The Collector Binarie.
    """
    
    # Constantes para os temas
    DARK_BLUE = "dark_blue"  # Tema atual/padrão
    DARK = "dark"            # Tema escuro com texto verde
    WHITE = "white"          # Tema claro
    
    def __init__(self):
        """Inicializa o gerenciador de temas."""
        self.current_theme = self.DARK_BLUE
        
        # Define os estilos para cada tema
        self._setup_themes()
    
    def _setup_themes(self):
        """Configura os estilos para cada tema."""
        # Tema Dark Blue (atual/padrão)
        self.dark_blue_style = """
            QMainWindow { background-color: #181a20; color: #e6e6e6; }
            QWidget { background-color: #181a20; color: #e6e6e6; }
            QSplitter::handle { background-color: #2d2d5a; width: 3px; height: 3px; }
            QSplitter::handle:hover { background-color: #3e3e5e; }
            QScrollBar:vertical { background-color: #181a20; width: 16px; margin: 0px; }
            QScrollBar::handle:vertical { background-color: #2d2d5a; min-height: 24px; border-radius: 8px; }
            QScrollBar::handle:vertical:hover { background-color: #3e3e5e; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background-color: #181a20; }
            QScrollBar:horizontal { background-color: #181a20; height: 16px; margin: 0px; }
            QScrollBar::handle:horizontal { background-color: #2d2d5a; min-width: 24px; border-radius: 8px; }
            QScrollBar::handle:horizontal:hover { background-color: #3e3e5e; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background-color: #181a20; }
            #customMenuBar { background-color: #23272e; border-bottom: 1px solid #282a36; min-height: 54px; max-height: 54px; }
            QPushButton { background-color: transparent; color: #e6e6e6; border: none; padding: 12px 22px; font-weight: bold; font-size: 15px; border-radius: 10px; }
            QPushButton:hover { background-color: #2d2d5a; }
            QPushButton#runButton { background-color: #00aa00; border-radius: 10px; font-size: 16px; }
            QPushButton#runButton:hover { background-color: #00cc00; }
            QPushButton#terminalButton { background-color: #23272e; border-radius: 10px; font-size: 16px; }
            QPushButton#terminalButton:hover { background-color: #2d2d5a; }
            QTabWidget::pane { border: none; background-color: #181a20; border-radius: 14px; }
            QTabBar::tab { background-color: #23272e; color: #e6e6e6; border-top-left-radius: 10px; border-top-right-radius: 10px; padding: 10px 18px; margin-right: 4px; font-size: 15px; }
            QTabBar::tab:selected { background-color: #2d2d5a; border-bottom: 3px solid #bd93f9; }
            QTabBar::tab:hover { background-color: #3e3e5e; }
            QTabBar::close-button { subcontrol-position: right; border-radius: 6px; padding: 2px; }
            QTabBar::close-button:hover { background-color: #ff5555; }
            QMenu { background-color: #23272e; color: #e6e6e6; border: 1px solid #282a36; border-radius: 10px; }
            QMenu::item { padding: 12px 28px; font-size: 15px; }
            QMenu::item:selected { background-color: #2d2d5a; }
            QStatusBar { background-color: #181a20; color: #bd93f9; border-top: 1px solid #282a36; font-size: 15px; }
            QPlainTextEdit { background-color: #181a20; color: #e6e6e6; border: none; font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace; font-size: 16px; selection-background-color: #2d2d5a; border-radius: 10px; padding: 10px; }
            QPlainTextEdit:focus { border: none; }
            QLineEdit { background-color: #23272e; color: #e6e6e6; border-radius: 10px; padding: 8px; border: 1px solid #bd93f9; font-size: 15px; }
            QTreeView { background-color: #181a20; border: none; color: #e6e6e6; font-size: 14px; }
            QTreeView::item { padding: 6px; border-radius: 6px; }
            QTreeView::item:selected { background-color: #2d2d5a; }
            QTreeView::item:hover { background-color: #23272e; }
            QLabel { color: #bd93f9; font-weight: bold; font-size: 16px; }
        """
        
        # Tema Dark (preto com texto verde)
        self.dark_style = """
            QMainWindow { background-color: #000000; color: #00ff00; }
            QWidget { background-color: #000000; color: #00ff00; }
            QSplitter::handle { background-color: #1a1a1a; width: 2px; height: 2px; }
            QSplitter::handle:hover { background-color: #2a2a2a; }
            QScrollBar:vertical { background-color: #000000; width: 14px; margin: 0px; }
            QScrollBar::handle:vertical { background-color: #1a1a1a; min-height: 20px; border-radius: 7px; }
            QScrollBar::handle:vertical:hover { background-color: #2a2a2a; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background-color: #000000; }
            QScrollBar:horizontal { background-color: #000000; height: 14px; margin: 0px; }
            QScrollBar::handle:horizontal { background-color: #1a1a1a; min-width: 20px; border-radius: 7px; }
            QScrollBar::handle:horizontal:hover { background-color: #2a2a2a; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background-color: #000000; }
            
            #customMenuBar { background-color: #000000; border-bottom: 1px solid #1a1a1a; min-height: 40px; max-height: 40px; }
            QPushButton { background-color: transparent; color: #00ff00; border: none; padding: 8px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #1a1a1a; border-radius: 5px; }
            QPushButton#runButton { background-color: #006600; border-radius: 5px; padding: 8px 12px; }
            QPushButton#runButton:hover { background-color: #008800; }
            QPushButton#terminalButton { background-color: #1a1a1a; border-radius: 5px; padding: 8px 12px; }
            QPushButton#terminalButton:hover { background-color: #2a2a2a; }
            
            QTabWidget::pane { border: none; background-color: #0a0a0a; border-radius: 10px; }
            QTabBar::tab { background-color: #1a1a1a; color: #00ff00; border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 8px 12px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #2a2a2a; border-bottom: 2px solid #00aa00; }
            QTabBar::tab:hover { background-color: #2a2a2a; }
            QTabBar::close-button { subcontrol-position: right; }
            QTabBar::close-button:hover { background-color: #aa0000; border-radius: 4px; }
            
            QMenu { background-color: #000000; color: #00ff00; border: 1px solid #1a1a1a; border-radius: 5px; }
            QMenu::item { padding: 8px 20px; }
            QMenu::item:selected { background-color: #1a1a1a; }
            
            QStatusBar { background-color: #000000; color: #00ff00; border-top: 1px solid #1a1a1a; }
            
            QPlainTextEdit { background-color: #0a0a0a; color: #00ff00; border: none; font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace; font-size: 16px; selection-background-color: #2a2a2a; }
            QPlainTextEdit:focus { border: none; }
            
            QLineEdit { background-color: #1a1a1a; color: #00ff00; border-radius: 8px; padding: 4px; border: 1px solid #2a2a2a; font-size: 15px; }
            
            QTreeView { background-color: #0a0a0a; border: none; color: #00ff00; font-size: 14px; }
            QTreeView::item { padding: 4px; border-radius: 4px; }
            QTreeView::item:selected { background-color: #2a2a2a; }
            QTreeView::item:hover { background-color: #1a1a1a; }
        """
        
        # Tema White (claro)
        self.white_style = """
            QMainWindow { background-color: #f0f0f0; color: #000000; }
            QWidget { background-color: #f0f0f0; color: #000000; }
            QSplitter::handle { background-color: #d0d0d0; width: 2px; height: 2px; }
            QSplitter::handle:hover { background-color: #b0b0b0; }
            QScrollBar:vertical { background-color: #f0f0f0; width: 14px; margin: 0px; }
            QScrollBar::handle:vertical { background-color: #d0d0d0; min-height: 20px; border-radius: 7px; }
            QScrollBar::handle:vertical:hover { background-color: #b0b0b0; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background-color: #f0f0f0; }
            QScrollBar:horizontal { background-color: #f0f0f0; height: 14px; margin: 0px; }
            QScrollBar::handle:horizontal { background-color: #d0d0d0; min-width: 20px; border-radius: 7px; }
            QScrollBar::handle:horizontal:hover { background-color: #b0b0b0; }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0px; }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background-color: #f0f0f0; }
            
            #customMenuBar { background-color: #e0e0e0; border-bottom: 1px solid #d0d0d0; min-height: 40px; max-height: 40px; }
            QPushButton { background-color: transparent; color: #000000; border: none; padding: 8px 12px; font-weight: bold; }
            QPushButton:hover { background-color: #d0d0d0; border-radius: 5px; }
            QPushButton#runButton { background-color: #4CAF50; border-radius: 5px; padding: 8px 12px; color: white; }
            QPushButton#runButton:hover { background-color: #45a049; }
            QPushButton#terminalButton { background-color: #d0d0d0; border-radius: 5px; padding: 8px 12px; }
            QPushButton#terminalButton:hover { background-color: #b0b0b0; }
            
            QTabWidget::pane { border: none; background-color: #ffffff; border-radius: 10px; }
            QTabBar::tab { background-color: #e0e0e0; color: #000000; border-top-left-radius: 8px; border-top-right-radius: 8px; padding: 8px 12px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: #ffffff; border-bottom: 2px solid #4CAF50; }
            QTabBar::tab:hover { background-color: #d0d0d0; }
            QTabBar::close-button { subcontrol-position: right; }
            QTabBar::close-button:hover { background-color: #ff5555; border-radius: 4px; }
            
            QMenu { background-color: #ffffff; color: #000000; border: 1px solid #d0d0d0; border-radius: 5px; }
            QMenu::item { padding: 8px 20px; }
            QMenu::item:selected { background-color: #e0e0e0; }
            
            QStatusBar { background-color: #e0e0e0; color: #000000; border-top: 1px solid #d0d0d0; }
            
            QPlainTextEdit { background-color: #ffffff; color: #000000; border: none; font-family: 'JetBrains Mono', 'Fira Mono', 'Consolas', 'Courier New', monospace; font-size: 16px; selection-background-color: #d0d0d0; }
            QPlainTextEdit:focus { border: none; }
            
            QLineEdit { background-color: #ffffff; color: #000000; border-radius: 8px; padding: 4px; border: 1px solid #d0d0d0; font-size: 15px; }
            
            QTreeView { background-color: #ffffff; border: none; color: #000000; font-size: 14px; }
            QTreeView::item { padding: 4px; border-radius: 4px; }
            QTreeView::item:selected { background-color: #d0d0d0; }
            QTreeView::item:hover { background-color: #e0e0e0; }
        """
        
        # Estilos específicos para o terminal em cada tema
        self.terminal_styles = {
            self.DARK_BLUE: """
                QDialog { background-color: #0C0C0C; color: #CCCCCC; }
                QPlainTextEdit { background-color: #0C0C0C; color: #CCCCCC; border: 1px solid #333333; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLabel { color: #CCCCCC; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLineEdit { background-color: #0C0C0C; color: #CCCCCC; border: none; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
            """,
            self.DARK: """
                QDialog { background-color: #000000; color: #00ff00; }
                QPlainTextEdit { background-color: #000000; color: #00ff00; border: 1px solid #1a1a1a; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLabel { color: #00ff00; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLineEdit { background-color: #000000; color: #00ff00; border: none; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
            """,
            self.WHITE: """
                QDialog { background-color: #ffffff; color: #000000; }
                QPlainTextEdit { background-color: #ffffff; color: #000000; border: 1px solid #d0d0d0; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLabel { color: #000000; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
                QLineEdit { background-color: #ffffff; color: #000000; border: none; font-family: 'Consolas', 'Courier New', monospace; font-size: 14px; }
            """
        }
    
    def get_theme_style(self, theme_name=None):
        """
        Retorna o estilo CSS para o tema especificado.
        
        Args:
            theme_name: Nome do tema (opcional, usa o tema atual se não especificado)
            
        Returns:
            str: Estilo CSS para o tema
        """
        if theme_name is None:
            theme_name = self.current_theme
            
        if theme_name == self.DARK_BLUE:
            return self.dark_blue_style
        elif theme_name == self.DARK:
            return self.dark_style
        elif theme_name == self.WHITE:
            return self.white_style
        else:
            # Tema padrão
            return self.dark_blue_style
    
    def get_terminal_style(self, theme_name=None):
        """
        Retorna o estilo CSS para o terminal no tema especificado.
        
        Args:
            theme_name: Nome do tema (opcional, usa o tema atual se não especificado)
            
        Returns:
            str: Estilo CSS para o terminal
        """
        if theme_name is None:
            theme_name = self.current_theme
            
        return self.terminal_styles.get(theme_name, self.terminal_styles[self.DARK_BLUE])
    
    def set_theme(self, theme_name):
        """
        Define o tema atual.
        
        Args:
            theme_name: Nome do tema
            
        Returns:
            bool: True se o tema foi alterado, False caso contrário
        """
        if theme_name in [self.DARK_BLUE, self.DARK, self.WHITE]:
            self.current_theme = theme_name
            return True
        return False
    
    def get_current_theme(self):
        """
        Retorna o nome do tema atual.
        
        Returns:
            str: Nome do tema atual
        """
        return self.current_theme
