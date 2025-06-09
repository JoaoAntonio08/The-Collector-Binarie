"""
Script para testar o parser de sintaxe binária e o interpretador aprimorado.
"""

from binary_syntax_parser import BinarySyntaxParser
from binario_interpreter_enhanced import BinarioInterpreterEnhanced

def test_binary_parser():
    print("=== Testando o Parser de Sintaxe Binária ===")
    
    parser = BinarySyntaxParser()
    
    # Teste de tradução de binário para Python
    print("\n1. Teste de tradução de binário para Python:")
    binary_code = """11010011 01100110 01110101 01101110 01100011 01100001 01101111 11010000
11011010 01001111 01101100 01100001 00100000 01001101 01110101 01101110 01100100 01101111
11010001
"""
    python_code = parser.parse_binary_to_python(binary_code)
    print(f"Código binário:\n{binary_code}")
    print(f"Código Python traduzido:\n{python_code}")
    
    # Teste de tradução de Python para binário
    print("\n2. Teste de tradução de Python para binário:")
    python_code = """def hello():
    print("Hello World")
"""
    binary_code = parser.parse_python_to_binary(python_code)
    print(f"Código Python:\n{python_code}")
    print(f"Código binário traduzido:\n{binary_code}")
    
    # Teste de validação de sintaxe
    print("\n3. Teste de validação de sintaxe:")
    invalid_binary = """11010011 01100110 01110101 01101110 01100011 01100001 01101111 11010000
11011010 01001111 01101100 01100001 00100000 01001101 01110101 01101110 01100100 01101111
"""  # Falta BINEND
    errors = parser.validate_binary_syntax(invalid_binary)
    print(f"Erros encontrados: {len(errors)}")
    for line_num, error_msg in errors:
        print(f"Linha {line_num}: {error_msg}")

def test_enhanced_interpreter():
    print("\n=== Testando o Interpretador Binário Aprimorado ===")
    
    interpreter = BinarioInterpreterEnhanced()
    
    # Teste de tradução
    print("\n1. Teste de tradução:")
    binary_code = """11010011 01100110 01110101 01101110 01100011 01100001 01101111 11010000
11011010 01001111 01101100 01100001 00100000 01001101 01110101 01101110 01100100 01101111
11010001
"""
    result = interpreter.traduzir_binario(binary_code)
    print(f"Código binário:\n{binary_code}")
    print(f"Resultado da tradução:\n{result}")
    
    # Teste de conversão
    print("\n2. Teste de conversão para binário:")
    text = "print('Teste')"
    binary = interpreter.converter_para_binario(text)
    print(f"Texto original: {text}")
    print(f"Binário convertido:\n{binary}")
    
    # Teste de validação
    print("\n3. Teste de validação:")
    errors = interpreter.validar_sintaxe_binaria(binary_code)
    print(f"Erros encontrados: {len(errors)}")
    for line_num, error_msg in errors:
        print(f"Linha {line_num}: {error_msg}")

if __name__ == "__main__":
    test_binary_parser()
    test_enhanced_interpreter()
    print("\nTestes concluídos!")
