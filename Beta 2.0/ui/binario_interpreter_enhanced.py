"""
Módulo interpretador binário aprimorado com suporte à linguagem binária personalizada.
Este módulo estende o interpretador binário original, adicionando suporte para
tradução bidirecional entre código binário e Python, com sintaxe personalizada.
"""

from binary_syntax_parser import BinarySyntaxParser

class BinarioInterpreterEnhanced:
    def __init__(self):
        # Inicializa o parser de sintaxe binária
        self.parser = BinarySyntaxParser()
        
    def traduzir_binario(self, codigo_binario: str) -> str:
        """
        Traduz código binário para texto legível, usando o parser avançado.
        
        Args:
            codigo_binario: String contendo código em formato binário
            
        Returns:
            String contendo texto traduzido
        """
        return self.parser.parse_binary_to_python(codigo_binario)
    
    def converter_para_binario(self, texto: str) -> str:
        """
        Converte texto para código binário, usando o parser avançado.
        
        Args:
            texto: String contendo texto ou código Python
            
        Returns:
            String contendo código em formato binário
        """
        return self.parser.parse_python_to_binary(texto)
    
    def validar_sintaxe_binaria(self, codigo_binario: str) -> list:
        """
        Valida a sintaxe do código binário e retorna uma lista de erros.
        
        Args:
            codigo_binario: String contendo código em formato binário
            
        Returns:
            Lista de tuplas (linha, mensagem de erro)
        """
        return self.parser.validate_binary_syntax(codigo_binario)
    
    def obter_significado_token(self, token: str) -> str:
        """
        Retorna o significado de um token binário.
        
        Args:
            token: String contendo um token binário de 8 dígitos
            
        Returns:
            String contendo o significado do token ou None se não existir
        """
        return self.parser.get_text_keyword(token)
    
    def traduzir_simples(self, codigo_binario: str) -> str:
        """
        Traduz código binário para texto de forma simples (compatibilidade com versão anterior).
        
        Args:
            codigo_binario: String contendo código em formato binário
            
        Returns:
            String contendo texto traduzido
        """
        linhas = codigo_binario.strip().splitlines()
        resultado = []
        for linha in linhas:
            palavras_binarias = linha.strip().split()
            traduzidas = [self.parser.get_text_keyword(b) or f"[{b}]" for b in palavras_binarias]
            resultado.append(" ".join(traduzidas))
        return "\n".join(resultado)
