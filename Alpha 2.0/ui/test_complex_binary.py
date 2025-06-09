"""
Script para testar a execução de códigos binários complexos.
"""

import sys
import os
from main import BinaryInterpreter, BinaryCodeExecutor

def test_binary_code(binary_code, description):
    """
    Testa a execução de um código binário.
    
    Args:
        binary_code: Código binário a ser testado
        description: Descrição do teste
    """
    print(f"\n=== Teste: {description} ===")
    
    # Cria instâncias do interpretador e executor
    interpreter = BinaryInterpreter()
    executor = BinaryCodeExecutor(interpreter)
    
    # Traduz o código binário para Python
    python_code = interpreter.traduzir_binario(binary_code)
    print(f"Código Python traduzido:\n{python_code}\n")
    
    # Executa o código
    try:
        result = executor.execute_binary_code(binary_code)
        print(f"Resultado da execução:\n{result}")
    except Exception as e:
        print(f"Erro ao executar o código: {str(e)}")

def main():
    """Função principal."""
    # Teste 1: Variáveis e operações aritméticas
    test_binary_code(
        "01100001 10001001 00110101 01100010 10001001 00110011 01110011 01101111 01101101 01100001 10001001 01100001 10001010 01100010 10000011 01110011 01101111 01101101 01100001 10001001 10001001 00111000 10010001 01111100 00101000 01111111 01100001 01110011 01101111 01101101 01100001 01100101 00111000 01111111 00101001 10000100 10010001 01111100 00101000 01111111 01100001 01110011 01101111 01101101 01100001 01101110 01100001 01101111 01100101 00111000 01111111 00101001",
        "Variáveis e operações aritméticas"
    )
    
    # Teste 2: Print simples
    test_binary_code(
        "01111100 00101000 01111111 01001111 01101100 01100001 00100000 01001101 01110101 01101110 01100100 01101111 01111111 00101001",
        "Print simples"
    )
    
    # Teste 3: Loop while
    test_binary_code(
        "01101001 10001001 00110000 10000101 01101001 10001100 00110101 10010001 01111100 00101000 01101001 00101001 01101001 10001001 01101001 10001010 00110001",
        "Loop while"
    )
    
    # Teste 4: Função simples
    test_binary_code(
        "10000111 01110011 01101111 01101101 01100001 00101000 01100001 00101100 01100010 00101001 10010001 01110010 01100101 01110100 01110101 01110010 01101110 01100001 10001010 01100010 10001001 01110011 01101111 01101101 01100001 00101000 00110010 00101100 00110011 00101001",
        "Função simples"
    )

if __name__ == "__main__":
    main()
