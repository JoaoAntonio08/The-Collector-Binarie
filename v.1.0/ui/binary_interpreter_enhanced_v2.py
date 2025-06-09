"""
Módulo aprimorado para interpretação e execução de código binário.
Esta versão amplia a biblioteca de códigos binários e corrige a tradução para gerar código Python válido.
"""

import re
import sys
import subprocess
import tempfile
import os
import traceback
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class BinaryInterpreterEnhancedV2:
    """
    Interpretador aprimorado para código binário com suporte a interatividade,
    validação robusta de comandos e tradução correta para código Python válido.
    """
    
    def __init__(self):
        """Inicializa o interpretador binário."""
        # Dicionário de tradução binário -> texto
        self.binary_to_text = {
            # Numerais
            "00110000": "0",
            "00110001": "1",
            "00110010": "2",
            "00110011": "3",
            "00110100": "4",
            "00110101": "5",
            "00110110": "6",
            "00110111": "7",
            "00111000": "8",
            "00111001": "9",
            
            # Letras maiúsculas
            "01000001": "A",
            "01000010": "B",
            "01000011": "C",
            "01000100": "D",
            "01000101": "E",
            "01000110": "F",
            "01000111": "G",
            "01001000": "H",
            "01001001": "I",
            "01001010": "J",
            "01001011": "K",
            "01001100": "L",
            "01001101": "M",
            "01001110": "N",
            "01001111": "O",
            "01010000": "P",
            "01010001": "Q",
            "01010010": "R",
            "01010011": "S",
            "01010100": "T",
            "01010101": "U",
            "01010110": "V",
            "01010111": "W",
            "01011000": "X",
            "01011001": "Y",
            "01011010": "Z",
            
            # Letras minúsculas
            "01100001": "a",
            "01100010": "b",
            "01100011": "c",
            "01100100": "d",
            "01100101": "e",
            "01100110": "f",
            "01100111": "g",
            "01101000": "h",
            "01101001": "i",
            "01101010": "j",
            "01101011": "k",
            "01101100": "l",
            "01101101": "m",
            "01101110": "n",
            "01101111": "o",
            "01110000": "p",
            "01110001": "q",
            "01110010": "r",
            "01110011": "s",
            "01110100": "t",
            "01110101": "u",
            "01110110": "v",
            "01110111": "w",
            "01111000": "x",
            "01111001": "y",
            "01111010": "z",
            
            # Comandos e palavras-chave Python
            "01111011": "var",
            "01111100": "print",
            "01111111": "\"",
            "01111110": "input",
            "10000000": "int",
            "10000001": "float",
            "10000010": "str",
            "10000011": "if",
            "10000100": "else",
            "10000101": "while",
            "10000110": "for",
            "10000111": "def",
            "10001000": "return",
            "10001001": "=",
            "10001010": "+",
            "10001011": "-",
            "10001100": "*",
            "10001101": "/",
            "10001110": "==",
            "10001111": "!=",
            "10010000": "<=",
            "10010001": ":",
            "10010010": "print()",  # print() completo
            "00100000": " ",
            "10010011": "_",
            "10010100": "{",
            "10010101": "}",
            "10010110": "[",
            "10010111": "]",
            "10011000": "'",
            "10011001": ",",
            "10011010": ".",
            "10011011": ";",
            "10011100": "\\",
            "10011101": "%",
            "10011110": "!",
            "10011111": "<",
            "10100000": ">",
            "10100001": "&",
            "10100010": "|",
            "10100011": ">=",
            "10100100": "and",
            "10100101": "or",
            "10100110": "not",
            "10100111": "True",
            "10101000": "False",
            "10101001": "None",
            "10101010": "in",
            "10101011": "is",
            "10101100": "class",
            "10101101": "import",
            "10101110": "from",
            "10101111": "as",
            "10110000": "try",
            "10110001": "except",
            "10110010": "finally",
            "10110011": "raise",
            "10110100": "with",
            "10110101": "pass",
            "10110110": "continue",
            "10110111": "break",
            "10111000": "global",
            "10111001": "nonlocal",
            "10111010": "lambda",
            "10111011": "yield",
            "10111100": "assert",
            "10111101": "del",
            "10111110": "elif",
            "10111111": "async",
            "11000000": "await",
            "11000001": "**",  # Exponenciação
            "11000010": "//",  # Divisão inteira
            "11000011": "+=",
            "11000100": "-=",
            "11000101": "*=",
            "11000110": "/=",
            "11000111": "%=",
            "11001000": "**=",
            "11001001": "//=",
            "11001010": "&=",
            "11001011": "|=",
            "11001100": "^=",
            "11001101": ">>=",
            "11001110": "<<=",
            "11001111": "^",  # XOR
            "11010000": "~",  # NOT bit a bit
            "11010001": "<<",  # Shift left
            "11010010": ">>",  # Shift right
            "00001010": "\n",  # Nova linha
            "00001101": "\r",  # Retorno de carro
            "00001001": "\t",  # Tab
        }
        
        # Dicionário inverso texto -> binário
        self.text_to_binary = {v: k for k, v in self.binary_to_text.items()}
        
        # Tokens que precisam de espaço antes e depois na tradução
        self.tokens_requiring_space = {
            "=", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", 
            ":", ",", "and", "or", "not", "in", "is", "**", "//", "+=", 
            "-=", "*=", "/=", "%=", "**=", "//=", "&=", "|=", "^=", ">>=", 
            "<<=", "^", "~", "<<", ">>", "&", "|"
        }
        
        # Tokens que precisam de quebra de linha após
        self.tokens_requiring_newline = {
            ":", # Para if, else, for, while, def, class, etc.
        }
        
        # Tokens que não devem ter espaço após
        self.tokens_no_space_after = {
            "("
        }
        
        # Tokens que não devem ter espaço antes
        self.tokens_no_space_before = {
            ")", ",", ":", ".", ";"
        }
        
        # Expressões regulares para validação
        self.binary_pattern = re.compile(r'^[01]{8}$')
        self.binary_line_pattern = re.compile(r'([01]{8})+')
    
    def traduzir_binario(self, binary_code):
        """
        Traduz código binário para texto Python válido.
        
        Args:
            binary_code: Código binário a ser traduzido
            
        Returns:
            Texto Python válido
        """
        # Normaliza o código binário
        binary_code = self._normalize_binary(binary_code)
        
        # Divide o código em tokens de 8 bits
        tokens = self._tokenize_binary(binary_code)
        
        # Traduz cada token
        translated_tokens = []
        for token in tokens:
            if token in self.binary_to_text:
                translated_tokens.append(self.binary_to_text[token])
            elif self.binary_pattern.match(token):
                # Token binário válido, mas não reconhecido
                translated_tokens.append(f"<{token}>")
            else:
                # Não é um token binário válido
                translated_tokens.append(token)
        
        # Formata o código Python para garantir espaçamento correto
        return self._format_python_code(translated_tokens)
    
    def _format_python_code(self, tokens):
        """
        Formata tokens traduzidos para código Python válido.
        
        Args:
            tokens: Lista de tokens traduzidos
            
        Returns:
            Código Python formatado
        """
        formatted_code = []
        indent_level = 0
        indent_str = "    "  # 4 espaços por nível de indentação
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Adiciona indentação no início da linha
            if i == 0 or formatted_code[-1].endswith('\n'):
                formatted_code.append(indent_str * indent_level)
            
            # Verifica se é uma palavra-chave que inicia um bloco
            if token in ["if", "else", "elif", "for", "while", "def", "class", "try", "except", "finally", "with"]:
                # Adiciona espaço após a palavra-chave
                formatted_code.append(token + " ")
            
            # Verifica se é um token que requer espaço antes e depois
            elif token in self.tokens_requiring_space:
                # Verifica se já tem espaço antes
                if not formatted_code[-1].endswith(' '):
                    formatted_code[-1] += " "
                formatted_code.append(token + " ")
            
            # Verifica se é um token que não deve ter espaço após
            elif token in self.tokens_no_space_after:
                formatted_code.append(token)
            
            # Verifica se é um token que não deve ter espaço antes
            elif token in self.tokens_no_space_before:
                # Remove espaço antes se existir
                if formatted_code[-1].endswith(' '):
                    formatted_code[-1] = formatted_code[-1][:-1]
                formatted_code.append(token)
                
                # Adiciona espaço após vírgula
                if token == ",":
                    formatted_code[-1] += " "
            
            # Verifica se é uma quebra de linha
            elif token == "\n":
                formatted_code.append(token)
            
            # Caso padrão
            else:
                formatted_code.append(token)
            
            # Ajusta o nível de indentação
            if token == ":" and i < len(tokens) - 1:
                # Aumenta a indentação após ':'
                indent_level += 1
                formatted_code[-1] += "\n"
            elif token == "\n" and i < len(tokens) - 1:
                # Verifica se o próximo token é uma palavra-chave que reduz a indentação
                next_token = tokens[i+1]
                if next_token in ["else", "elif", "except", "finally"]:
                    indent_level = max(0, indent_level - 1)
            
            i += 1
        
        # Junta todos os tokens formatados
        return ''.join(formatted_code)
    
    def converter_para_binario(self, text):
        """
        Converte texto para código binário.
        
        Args:
            text: Texto a ser convertido
            
        Returns:
            Código binário
        """
        # Tratamento especial para print() e input()
        # Substitui print() pelo token específico
        text = text.replace("print()", " print() ")
        
        # Trata print com argumentos: print("texto") -> print ( "texto" )
        # Isso garante que cada parte seja tokenizada separadamente
        text = re.sub(r'print\(', 'print ( ', text)
        
        # Trata input com argumentos: input("texto") -> input ( "texto" )
        text = re.sub(r'input\(', 'input ( ', text)
        
        # Garante espaços ao redor de parênteses e outros símbolos
        for symbol in ['(', ')', ',', '+', '-', '*', '/', '=', '<', '>', ':', ';']:
            text = text.replace(symbol, f' {symbol} ')
        
        # Normaliza espaços
        text = ' '.join(text.split())
        
        # Converte cada token para binário
        tokens = text.split()
        binary_tokens = []
        
        for token in tokens:
            # Verifica se é um token especial
            if token == "print()":
                binary_tokens.append(self.text_to_binary["print()"])
            elif token in self.text_to_binary:
                binary_tokens.append(self.text_to_binary[token])
            else:
                # Para tokens não reconhecidos, converte caractere por caractere
                for char in token:
                    if char in self.text_to_binary:
                        binary_tokens.append(self.text_to_binary[char])
                    else:
                        # Caractere não reconhecido
                        binary_tokens.append(f"<{char}>")
        
        return ' '.join(binary_tokens)
    
    def validar_codigo_binario(self, binary_code):
        """
        Valida se o código binário está correto.
        
        Args:
            binary_code: Código binário a ser validado
            
        Returns:
            Tupla (válido, mensagem de erro)
        """
        # Normaliza o código binário
        binary_code = self._normalize_binary(binary_code)
        
        # Verifica se está vazio
        if not binary_code:
            return False, "Código binário vazio"
        
        # Divide o código em tokens de 8 bits
        tokens = self._tokenize_binary(binary_code)
        
        # Verifica cada token
        invalid_tokens = []
        for i, token in enumerate(tokens):
            if not self.binary_pattern.match(token):
                invalid_tokens.append((i + 1, token))
        
        if invalid_tokens:
            error_msg = "Tokens binários inválidos:\n"
            for pos, token in invalid_tokens:
                error_msg += f"  Posição {pos}: '{token}' (deve ter 8 dígitos binários)\n"
            return False, error_msg
        
        return True, "Código binário válido"
    
    def executar_codigo(self, binary_code, interactive=True):
        """
        Executa código binário traduzindo-o para Python.
        
        Args:
            binary_code: Código binário a ser executado
            interactive: Se True, permite interatividade (input/output)
            
        Returns:
            Resultado da execução
        """
        # Traduz o código binário para Python
        python_code = self.traduzir_binario(binary_code)
        
        # Executa o código Python
        return self._execute_python_code(python_code, interactive)
    
    def _normalize_binary(self, binary_code):
        """
        Normaliza o código binário removendo espaços, comentários e caracteres inválidos.
        
        Args:
            binary_code: Código binário a ser normalizado
            
        Returns:
            Código binário normalizado
        """
        # Remove comentários (tudo após //)
        lines = binary_code.split('\n')
        cleaned_lines = []
        for line in lines:
            comment_pos = line.find('//')
            if comment_pos >= 0:
                line = line[:comment_pos]
            cleaned_lines.append(line)
        
        binary_code = '\n'.join(cleaned_lines)
        
        # Remove espaços e outros caracteres não binários
        normalized = []
        for char in binary_code:
            if char in '01\n':
                normalized.append(char)
            elif char.isspace():
                # Preserva quebras de linha, converte outros espaços para espaço único
                if char != '\n':
                    normalized.append(' ')
        
        return ''.join(normalized)
    
    def _tokenize_binary(self, binary_code):
        """
        Divide o código binário em tokens de 8 bits.
        
        Args:
            binary_code: Código binário normalizado
            
        Returns:
            Lista de tokens
        """
        tokens = []
        current_token = ""
        
        for char in binary_code:
            if char in '01':
                current_token += char
                if len(current_token) == 8:
                    tokens.append(current_token)
                
(Content truncated due to size limit. Use line ranges to read in chunks)