"""
Módulo para análise e tradução de sintaxe binária personalizada para Python.
Este módulo expande as capacidades do interpretador binário original,
adicionando suporte para estruturas de controle e funções em binário.
"""

import re
from typing import Dict, List, Tuple, Optional


class BinarySyntaxParser:
    def __init__(self):
        # Dicionário expandido de palavras-chave binárias
        self.binary_keywords = {
            # Dígitos
            "00110000": "0", "00110001": "1", "00110010": "2", "00110011": "3",
            "00110100": "4", "00110101": "5", "00110110": "6", "00110111": "7",
            "00111000": "8", "00111001": "9",

            # Letras maiúsculas
            "01000001": "A", "01000010": "B", "01000011": "C", "01000100": "D",
            "01000101": "E", "01000110": "F", "01000111": "G", "01001000": "H",
            "01001001": "I", "01001010": "J", "01001011": "K", "01001100": "L",
            "01001101": "M", "01001110": "N", "01001111": "O", "01010000": "P",
            "01010001": "Q", "01010010": "R", "01010011": "S", "01010100": "T",
            "01010101": "U", "01010110": "V", "01010111": "W", "01011000": "X",
            "01011001": "Y", "01011010": "Z",

            # Letras minúsculas
            "01100001": "a", "01100010": "b", "01100011": "c", "01100100": "d",
            "01100101": "e", "01100110": "f", "01100111": "g", "01101000": "h",
            "01101001": "i", "01101010": "j", "01101011": "k", "01101100": "l",
            "01101101": "m", "01101110": "n", "01101111": "o", "01110000": "p",
            "01110001": "q", "01110010": "r", "01110011": "s", "01110100": "t",
            "01110101": "u", "01110110": "v", "01110111": "w", "01111000": "x",
            "01111001": "y", "01111010": "z",

            # Caracteres especiais
            "00100000": " ",     # Espaço
            "00100001": "!",     # Ponto de exclamação
            "00100010": "\"",    # Aspas duplas
            "00100011": "#",     # Hashtag
            "00100100": "$",     # Cifrão
            "00100101": "%",     # Porcentagem
            "00100110": "&",     # E comercial
            "00100111": "'",     # Aspas simples
            "00101000": "(",     # Parêntese aberto
            "00101001": ")",     # Parêntese fechado
            "00101010": "*",     # Asterisco
            "00101011": "+",     # Mais
            "00101100": ",",     # Vírgula
            "00101101": "-",     # Hífen
            "00101110": ".",     # Ponto
            "00101111": "/",     # Barra
            "00111010": ":",     # Dois pontos
            "00111011": ";",     # Ponto e vírgula
            "00111100": "<",     # Menor que
            "00111101": "=",     # Igual
            "00111110": ">",     # Maior que
            "00111111": "?",     # Ponto de interrogação
            "01000000": "@",     # Arroba
            "01011011": "[",     # Colchete aberto
            "01011100": "\\",    # Barra invertida
            "01011101": "]",     # Colchete fechado
            "01011110": "^",     # Circunflexo
            "01011111": "_",     # Sublinhado
            "01100000": "`",     # Crase
            "01111011": "{",     # Chave aberta
            "01111100": "|",     # Barra vertical
            "01111101": "}",     # Chave fechada
            "01111110": "~",     # Til

            # Palavras-chave Python (expandidas)
            "10000000": "and",
            "10000001": "as",
            "10000010": "assert",
            "10000011": "async",
            "10000100": "await",
            "10000101": "break",
            "10000110": "class",
            "10000111": "continue",
            "10001000": "def",
            "10001001": "del",
            "10001010": "elif",
            "10001011": "else",
            "10001100": "except",
            "10001101": "False",
            "10001110": "finally",
            "10001111": "for",
            "10010000": "from",
            "10010001": "global",
            "10010010": "if",
            "10010011": "import",
            "10010100": "in",
            "10010101": "is",
            "10010110": "lambda",
            "10010111": "None",
            "10011000": "nonlocal",
            "10011001": "not",
            "10011010": "or",
            "10011011": "pass",
            "10011100": "raise",
            "10011101": "return",
            "10011110": "True",
            "10011111": "try",
            "10100000": "while",
            "10100001": "with",
            "10100010": "yield",

            # Funções comuns
            "10100011": "print",
            "10100100": "input",
            "10100101": "len",
            "10100110": "range",
            "10100111": "int",
            "10101000": "str",
            "10101001": "float",
            "10101010": "list",
            "10101011": "dict",
            "10101100": "set",
            "10101101": "tuple",
            "10101110": "sum",
            "10101111": "min",
            "10110000": "max",
            "10110001": "sorted",
            "10110010": "open",
            "10110011": "read",
            "10110100": "write",
            "10110101": "append",
            "10110110": "extend",
            "10110111": "pop",
            "10111000": "remove",
            "10111001": "join",
            "10111010": "split",
            "10111011": "strip",
            "10111100": "replace",
            "10111101": "format",
            "10111110": "enumerate",
            "10111111": "zip",
            "11000000": "map",
            "11000001": "filter",
            "11000010": "lambda",
            
            # Operadores compostos
            "11000011": "==",    # Igual a
            "11000100": "!=",    # Diferente de
            "11000101": "<=",    # Menor ou igual a
            "11000110": ">=",    # Maior ou igual a
            "11000111": "+=",    # Incremento
            "11001000": "-=",    # Decremento
            "11001001": "*=",    # Multiplicação e atribuição
            "11001010": "/=",    # Divisão e atribuição
            "11001011": "//",    # Divisão inteira
            "11001100": "**",    # Potência
            "11001101": "%=",    # Módulo e atribuição
            "11001110": "//=",   # Divisão inteira e atribuição
            "11001111": "**=",   # Potência e atribuição
            
            # Comandos especiais da linguagem binária
            "11010000": "BINSTART",  # Início de bloco binário
            "11010001": "BINEND",    # Fim de bloco binário
            "11010010": "BINVAR",    # Declaração de variável
            "11010011": "BINFUNC",   # Declaração de função
            "11010100": "BINIF",     # Estrutura condicional
            "11010101": "BINELSE",   # Estrutura condicional (else)
            "11010110": "BINLOOP",   # Estrutura de repetição
            "11010111": "BINBREAK",  # Interromper loop
            "11011000": "BINCONT",   # Continuar loop
            "11011001": "BINRET",    # Retorno de função
            "11011010": "BINPRINT",  # Impressão formatada
            "11011011": "BININPUT",  # Entrada formatada
            "11011100": "BINCOMMENT" # Comentário
        }
        
        # Dicionário inverso para conversão de texto para binário
        self.text_to_binary = {v: k for k, v in self.binary_keywords.items()}
        
        # Adiciona mapeamento para caracteres individuais que não estão no dicionário
        for i in range(32, 127):
            char = chr(i)
            if char not in self.text_to_binary:
                binary = format(i, '08b')
                if binary not in self.binary_keywords:
                    self.binary_keywords[binary] = char
                    self.text_to_binary[char] = binary
    
    def parse_binary_to_python(self, binary_code: str) -> str:
        """
        Converte código binário para código Python.
        
        Args:
            binary_code: String contendo código em formato binário
            
        Returns:
            String contendo código Python equivalente
        """
        lines = binary_code.strip().splitlines()
        python_lines = []
        
        # Controle de indentação
        indent_level = 0
        
        for line in lines:
            # Ignora linhas vazias
            if not line.strip():
                python_lines.append("")
                continue
                
            tokens = line.strip().split()
            python_tokens = []
            
            # Processa tokens especiais de controle
            i = 0
            while i < len(tokens):
                token = tokens[i]
                
                # Verifica se é um token especial
                if token == "11010000":  # BINSTART - início de bloco
                    indent_level += 1
                    python_tokens.append(":")
                elif token == "11010001":  # BINEND - fim de bloco
                    indent_level -= 1
                    # Não adiciona nada, apenas reduz a indentação
                elif token == "11010010":  # BINVAR - declaração de variável
                    if i + 2 < len(tokens):
                        var_name = self.binary_keywords.get(tokens[i+1], f"[{tokens[i+1]}]")
                        python_tokens.append(var_name)
                        python_tokens.append("=")
                        i += 2  # Pula os próximos dois tokens
                    else:
                        python_tokens.append("[ERRO: BINVAR incompleto]")
                elif token == "11010011":  # BINFUNC - declaração de função
                    if i + 1 < len(tokens):
                        func_name = self.binary_keywords.get(tokens[i+1], f"[{tokens[i+1]}]")
                        python_tokens.append("def")
                        python_tokens.append(func_name)
                        python_tokens.append("()")
                        i += 1  # Pula o próximo token
                    else:
                        python_tokens.append("[ERRO: BINFUNC incompleto]")
                elif token == "11010100":  # BINIF - estrutura condicional
                    python_tokens.append("if")
                elif token == "11010101":  # BINELSE - estrutura condicional (else)
                    python_tokens.append("else")
                elif token == "11010110":  # BINLOOP - estrutura de repetição
                    if i + 1 < len(tokens):
                        count = self.binary_keywords.get(tokens[i+1], f"[{tokens[i+1]}]")
                        python_tokens.append(f"for _ in range({count})")
                        i += 1  # Pula o próximo token
                    else:
                        python_tokens.append("[ERRO: BINLOOP incompleto]")
                elif token == "11010111":  # BINBREAK - interromper loop
                    python_tokens.append("break")
                elif token == "11011000":  # BINCONT - continuar loop
                    python_tokens.append("continue")
                elif token == "11011001":  # BINRET - retorno de função
                    python_tokens.append("return")
                elif token == "11011010":  # BINPRINT - impressão formatada
                    python_tokens.append("print")
                    python_tokens.append("(")
                    
                    # Coleta todos os tokens até o fim da linha para o print
                    j = i + 1
                    print_tokens = []
                    while j < len(tokens):
                        print_token = self.binary_keywords.get(tokens[j], f"[{tokens[j]}]")
                        print_tokens.append(print_token)
                        j += 1
                    
                    python_tokens.append(" ".join(print_tokens))
                    python_tokens.append(")")
                    i = j - 1  # Ajusta o índice para o último token processado
                elif token == "11011011":  # BININPUT - entrada formatada
                    if i + 1 < len(tokens):
                        var_name = self.binary_keywords.get(tokens[i+1], f"[{tokens[i+1]}]")
                        python_tokens.append(f"{var_name} = input()")
                        i += 1  # Pula o próximo token
                    else:
                        python_tokens.append("[ERRO: BININPUT incompleto]")
                elif token == "11011100":  # BINCOMMENT - comentário
                    # Coleta todos os tokens até o fim da linha para o comentário
                    j = i + 1
                    comment_tokens = []
                    while j < len(tokens):
                        comment_token = self.binary_keywords.get(tokens[j], f"[{tokens[j]}]")
                        comment_tokens.append(comment_token)
                        j += 1
                    
                    python_tokens.append("# " + " ".join(comment_tokens))
                    i = j - 1  # Ajusta o índice para o último token processado
                else:
                    # Token normal, traduz diretamente
                    translated = self.binary_keywords.get(token, f"[{token}]")
                    python_tokens.append(translated)
                
                i += 1
            
            # Adiciona a linha com a indentação correta
            indentation = "    " * max(0, indent_level)
            python_line = indentation + " ".join(python_tokens)
            python_lines.append(python_line)
        
        return "\n".join(python_lines)
    
    def parse_python_to_binary(self, python_code: str) -> str:
        """
        Converte código Python para código binário.
        
        Args:
            python_code: String contendo código Python
            
        Returns:
            String contendo código em formato binário equivalente
        """
        lines = python_code.strip().splitlines()
        binary_lines = []
        
        for line in lines:
            # Ignora linhas vazias
            if not line.strip():
                binary_lines.append("")
                continue
            
            # Analisa a indentação
            indent_count = len(line) - len(line.lstrip())
            indent_level = indent_count // 4  # Assume 4 espaços por nível
            line = line.strip()
            
            # Tokens especiais para estruturas Python comuns
            if line.startswith("def "):
                parts = line.split("(")[0].split()
                func_name = parts[1]
                binary_tokens = ["11010011"]  # BINFUNC
                
                # Adiciona o nome da função em binário
                if func_name in self.text_to_binary:
                    binary_tokens.append(self.text_to_binary[func_name])
                else:
                    # Converte caractere por caractere
                    for char in func_name:
                        if char in self.text_to_binary:
                            binary_tokens.append(self.text_to_binary[char])
                        else:
                            binary_tokens.append(format(ord(char), '08b'))
                
                # Adiciona o início do bloco
                if line.endswith(":"):
                    binary_tokens.append("11010000")  # BINSTART
                
                binary_lines.append(" ".join(binary_tokens))
                continue
            
            elif line.startswith("if "):
                parts = line.split(":")
                condition = parts[0][3:].strip()
                
                binary_tokens = ["11010100"]  # BINIF
                
                # Converte a condição
                for word in condition.split():
                    if word in self.text_to_binary:
                        binary_tokens.append(self.text_to_binary[word])
                    else:
                        # Converte caractere por caractere
                        for char in word:
                            if char in self.text_to_binary:
                                binary_tokens.append(self.text_to_binary[char]
(Content truncated due to size limit. Use line ranges to read in chunks)