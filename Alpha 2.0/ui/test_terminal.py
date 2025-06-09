"""
Script para testar o terminal interativo aprimorado com execução de comandos binários.
"""

import sys
from PyQt5.QtWidgets import QApplication
from terminal_enhanced import TerminalEnhanced

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Cria o terminal com uma mensagem inicial
    terminal = TerminalEnhanced("=== Terminal Interativo Aprimorado ===\n"
                               "Digite comandos em Python ou modo binário.\n"
                               "Use o checkbox 'Modo Binário' para alternar entre os modos.\n\n")
    
    # Exibe o terminal
    terminal.show()
    
    # Executa a aplicação
    sys.exit(app.exec_())
