"""
Script para testar a interface moderna do The Collector Binarie.
Este script executa testes para validar a experiência do usuário e as funcionalidades
em um fluxo real de uso.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Importa a janela principal moderna
from modern_main_window import ModernMainWindow

def main():
    """Função principal para testar a interface moderna."""
    print("Iniciando testes da interface moderna do The Collector Binarie...")
    
    # Cria a aplicação
    app = QApplication(sys.argv)
    
    # Cria a janela principal
    window = ModernMainWindow()
    window.show()
    
    # Executa testes
    test_welcome_screen(window)
    test_new_file(window)
    test_close_tab(window)
    test_binary_reference(window)
    test_terminal(window)
    test_bugs_panel(window)
    
    print("Todos os testes concluídos com sucesso!")
    
    # Executa a aplicação para interação manual
    sys.exit(app.exec_())

def test_welcome_screen(window):
    """
    Testa a tela de boas-vindas.
    
    Args:
        window: Janela principal
    """
    print("\nTestando tela de boas-vindas...")
    
    # Verifica se a tela de boas-vindas está sendo exibida
    assert window.central_stack.currentWidget() == window.welcome_screen, "A tela de boas-vindas não está sendo exibida inicialmente"
    
    print("Teste da tela de boas-vindas concluído com sucesso!")

def test_new_file(window):
    """
    Testa a criação de um novo arquivo.
    
    Args:
        window: Janela principal
    """
    print("\nTestando criação de novo arquivo...")
    
    # Clica no botão de novo arquivo
    window.welcome_screen.get_new_file_button().click()
    
    # Verifica se o editor está sendo exibido
    assert window.central_stack.currentWidget() == window.editor_widget, "O editor não está sendo exibido após criar novo arquivo"
    
    # Verifica se uma aba foi criada
    assert window.tabs.count() == 1, f"Número incorreto de abas: {window.tabs.count()} (esperado: 1)"
    
    # Verifica o título da aba
    assert window.tabs.tabText(0) == "Sem título", f"Título incorreto da aba: {window.tabs.tabText(0)} (esperado: 'Sem título')"
    
    # Escreve algum texto no editor
    editor = window.tabs.widget(0)
    editor.setPlainText("01000001 01000010 01000011")  # ABC em binário
    
    # Verifica se o texto foi inserido
    assert editor.toPlainText() == "01000001 01000010 01000011", "O texto não foi inserido corretamente no editor"
    
    print("Teste de criação de novo arquivo concluído com sucesso!")

def test_close_tab(window):
    """
    Testa o fechamento de abas.
    
    Args:
        window: Janela principal
    """
    print("\nTestando fechamento de abas...")
    
    # Verifica se há uma aba aberta
    assert window.tabs.count() == 1, f"Número incorreto de abas: {window.tabs.count()} (esperado: 1)"
    
    # Fecha a aba
    window.tabs.tabCloseRequested.emit(0)
    
    # Verifica se a aba foi fechada
    assert window.tabs.count() == 0, f"Número incorreto de abas após fechamento: {window.tabs.count()} (esperado: 0)"
    
    # Verifica se a tela de boas-vindas está sendo exibida
    assert window.central_stack.currentWidget() == window.welcome_screen, "A tela de boas-vindas não está sendo exibida após fechar todas as abas"
    
    print("Teste de fechamento de abas concluído com sucesso!")

def test_binary_reference(window):
    """
    Testa a guia de referência binária.
    
    Args:
        window: Janela principal
    """
    print("\nTestando guia de referência binária...")
    
    # Verifica se a guia de referência existe
    assert window.reference_guide is not None, "A guia de referência não foi criada"
    
    # Cria um novo arquivo para testar a inserção de código
    window.welcome_screen.get_new_file_button().click()
    
    # Simula a seleção de um código binário na guia de referência
    window.reference_guide.code_selected.emit("01000001")  # 'A' em binário
    
    # Verifica se o código foi inserido no editor
    editor = window.tabs.widget(0)
    assert editor.toPlainText() == "01000001", f"O código binário não foi inserido corretamente: {editor.toPlainText()} (esperado: '01000001')"
    
    print("Teste da guia de referência binária concluído com sucesso!")

def test_terminal(window):
    """
    Testa o terminal integrado.
    
    Args:
        window: Janela principal
    """
    print("\nTestando terminal integrado...")
    
    # Verifica se o terminal ainda não foi criado
    assert window.terminal is None, "O terminal já foi criado antes de ser solicitado"
    
    # Clica no botão do terminal
    window.terminal_button.click()
    
    # Verifica se o terminal foi criado
    assert window.terminal is not None, "O terminal não foi criado ao clicar no botão"
    
    # Verifica se o terminal está visível
    assert window.terminal.isVisible(), "O terminal não está visível após ser aberto"
    
    # Fecha o terminal
    window.terminal.close()
    
    print("Teste do terminal integrado concluído com sucesso!")

def test_bugs_panel(window):
    """
    Testa o painel de bugs.
    
    Args:
        window: Janela principal
    """
    print("\nTestando painel de bugs...")
    
    # Verifica se o painel de bugs ainda não foi criado
    assert window.bugs_panel is None, "O painel de bugs já foi criado antes de ser solicitado"
    
    # Insere código com erro no editor atual
    editor = window.tabs.widget(0)
    editor.setPlainText("0100 01000010")  # Primeiro token inválido
    
    # Clica no botão de bugs
    window.bugs_button.click()
    
    # Verifica se o painel de bugs foi criado
    assert window.bugs_panel is not None, "O painel de bugs não foi criado ao clicar no botão"
    
    # Verifica se o painel de bugs está visível
    assert window.bugs_panel.isVisible(), "O painel de bugs não está visível após ser aberto"
    
    # Verifica se bugs foram encontrados
    assert len(window.bugs_panel.bugs) > 0, "Nenhum bug foi encontrado no código com erro"
    
    # Fecha o painel de bugs
    window.bugs_panel.close()
    
    print("Teste do painel de bugs concluído com sucesso!")

if __name__ == "__main__":
    main()
