"""
Script para testar a integração e funcionamento do The Collector Binarie.
Este script executa testes básicos para garantir que o aplicativo está funcionando corretamente.
"""

import os
import sys
import unittest
import tempfile
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Importa o módulo principal
try:
    from main_app import MainAppWindow
except ImportError as e:
    print(f"Erro ao importar o módulo principal: {e}")
    print("Certifique-se de que o arquivo main_app.py está no mesmo diretório que este script.")
    sys.exit(1)

class TestMainApp(unittest.TestCase):
    """Testes para o aplicativo The Collector Binarie."""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para os testes."""
        # Cria a aplicação Qt
        cls.app = QApplication.instance() or QApplication(sys.argv)
        
        # Cria a janela principal
        cls.window = MainAppWindow()
    
    def test_01_window_initialization(self):
        """Testa se a janela principal é inicializada corretamente."""
        self.assertIsNotNone(self.window)
        self.assertEqual(self.window.windowTitle(), "The Collector Binarie")
    
    def test_02_create_new_file(self):
        """Testa a criação de um novo arquivo."""
        # Verifica se a tela de boas-vindas está visível inicialmente
        self.assertEqual(self.window.central_stack.currentWidget(), self.window.welcome_screen)
        
        # Cria um novo arquivo
        self.window._new_file()
        
        # Verifica se o editor está visível
        self.assertEqual(self.window.central_stack.currentWidget(), self.window.editor_widget)
        
        # Verifica se uma nova aba foi criada
        self.assertEqual(self.window.tabs.count(), 1)
        self.assertEqual(self.window.tabs.tabText(0), "Sem título")
    
    def test_03_binary_translation(self):
        """Testa a tradução entre texto e binário."""
        # Cria um novo arquivo
        self.window._new_file()
        
        # Obtém o editor atual
        editor = self.window.tabs.currentWidget()
        self.assertIsNotNone(editor)
        
        # Define um texto de teste
        test_text = "Hello"
        editor.setPlainText(test_text)
        
        # Traduz para binário
        self.window._text_to_binary()
        
        # Verifica se uma nova aba foi criada com o texto traduzido
        self.assertEqual(self.window.tabs.count(), 2)
        binary_editor = self.window.tabs.currentWidget()
        self.assertIsNotNone(binary_editor)
        
        # Traduz de volta para texto
        self.window._binary_to_text()
        
        # Verifica se uma nova aba foi criada com o texto original
        self.assertEqual(self.window.tabs.count(), 3)
        text_editor = self.window.tabs.currentWidget()
        self.assertIsNotNone(text_editor)
        
        # Verifica se o texto foi traduzido corretamente (pode conter espaços)
        translated_text = text_editor.toPlainText().replace(" ", "")
        self.assertEqual(translated_text, test_text)
    
    def test_04_close_all_tabs(self):
        """Testa o fechamento de todas as abas."""
        # Fecha todas as abas
        while self.window.tabs.count() > 0:
            self.window._close_tab(0)
        
        # Verifica se a tela de boas-vindas está visível
        self.assertEqual(self.window.central_stack.currentWidget(), self.window.welcome_screen)
    
    def test_05_reference_guide(self):
        """Testa o guia de referência."""
        # Verifica se o guia de referência existe
        self.assertIsNotNone(self.window.reference_guide)
        
        # Cria um novo arquivo para testar a inserção de código
        self.window._new_file()
        
        # Simula a seleção de um código binário
        # Nota: Não podemos testar diretamente o clique na árvore,
        # mas podemos simular o sinal emitido
        binary_code = "01000001 "  # 'A' com espaço
        self.window.reference_guide.code_selected.emit(binary_code)
        
        # Verifica se o código foi inserido no editor
        editor = self.window.tabs.currentWidget()
        self.assertEqual(editor.toPlainText(), binary_code)
    
    @classmethod
    def tearDownClass(cls):
        """Limpeza após os testes."""
        # Fecha a janela principal
        cls.window.close()
        
        # Limpa a aplicação Qt
        cls.app.quit()

if __name__ == "__main__":
    # Executa os testes
    unittest.main()
