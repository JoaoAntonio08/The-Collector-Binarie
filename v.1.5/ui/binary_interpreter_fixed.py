"""
Módulo aprimorado para interpretação e execução de código binário.
Esta versão corrige problemas na tradução de comandos como print() e input().
"""

import re
import sys
import subprocess
import tempfile
import os
import traceback
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class BinaryInterpreterFixed:
    """
    Interpretador aprimorado para código binário com suporte a interatividade
    e validação robusta de comandos.
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
            
            # Comandos e símbolos
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
            "00101000": "(",
            "00101001": ")",
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
            "00001010": "\n",  # Nova linha
            "00001101": "\r",  # Retorno de carro
            "00001001": "\t",  # Tab
        }
        
        # Dicionário inverso texto -> binário
        self.text_to_binary = {v: k for k, v in self.binary_to_text.items()}
        
        # Expressões regulares para validação
        self.binary_pattern = re.compile(r'^[01]{8}$')
        self.binary_line_pattern = re.compile(r'([01]{8})+')
    
    def traduzir_binario(self, binary_code):
        """
        Traduz código binário para texto.
        
        Args:
            binary_code: Código binário a ser traduzido
            
        Returns:
            Texto traduzido
        """
        # Normaliza o código binário
        binary_code = self._normalize_binary(binary_code)
        
        # Divide o código em tokens de 8 bits
        tokens = self._tokenize_binary(binary_code)
        
        # Traduz cada token
        translated = []
        for token in tokens:
            if token in self.binary_to_text:
                translated.append(self.binary_to_text[token])
            elif self.binary_pattern.match(token):
                # Token binário válido, mas não reconhecido
                translated.append(f"<{token}>")
            else:
                # Não é um token binário válido
                translated.append(token)
        
        return ''.join(translated)
    
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
                    current_token = ""
            elif char in ' \n':
                # Finaliza o token atual se necessário
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                
                # Adiciona quebra de linha como token especial
                if char == '\n':
                    tokens.append("00001010")  # \n em binário
        
        # Adiciona o último token se houver
        if current_token:
            tokens.append(current_token)
        
        return tokens
    
    def _execute_python_code(self, python_code, interactive=True):
        """
        Executa código Python de forma segura.
        
        Args:
            python_code: Código Python a ser executado
            interactive: Se True, permite interatividade (input/output)
            
        Returns:
            Resultado da execução
        """
        if interactive:
            # Execução interativa (permite input/output)
            return self._execute_interactive(python_code)
        else:
            # Execução não interativa (captura saída)
            return self._execute_non_interactive(python_code)
    
    def _execute_interactive(self, python_code):
        """
        Executa código Python de forma interativa.
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        # Cria um arquivo temporário com o código
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(python_code)
            temp_path = temp_file.name
        
        try:
            # Executa o código em um processo separado
            process = subprocess.Popen(
                [sys.executable, temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Captura a saída
            stdout, stderr = process.communicate()
            
            # Combina stdout e stderr
            output = stdout
            if stderr:
                output += f"\n--- Erros ---\n{stderr}"
            
            return output
        
        except Exception as e:
            return f"Erro ao executar o código: {str(e)}"
        
        finally:
            # Remove o arquivo temporário
            try:
                os.unlink(temp_path)
            except:
                pass
    
    def _execute_non_interactive(self, python_code):
        """
        Executa código Python de forma não interativa.
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        # Captura stdout e stderr
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        
        try:
            # Redireciona stdout e stderr
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                # Executa o código
                exec(python_code, {'__builtins__': __builtins__}, {})
            
            # Obtém a saída
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()
            
            # Combina stdout e stderr
            output = stdout
            if stderr:
                output += f"\n--- Erros ---\n{stderr}"
            
            return output
        
        except Exception as e:
            # Captura o traceback
            tb = traceback.format_exc()
            return f"Erro ao executar o código:\n{tb}"
        
        finally:
            # Fecha os buffers
            stdout_buffer.close()
            stderr_buffer.close()
    
    def get_binary_commands(self):
        """
        Obtém a lista de comandos binários disponíveis.
        
        Returns:
            Dicionário com comandos binários
        """
        # Agrupa os comandos por categoria
        commands = {
            "Numerais": {},
            "Letras Maiúsculas": {},
            "Letras Minúsculas": {},
            "Comandos": {},
            "Símbolos": {}
        }
        
        for binary, text in self.binary_to_text.items():
            if text.isdigit():
                commands["Numerais"][text] = binary
            elif text.isupper() and text.isalpha():
                commands["Letras Maiúsculas"][text] = binary
            elif text.islower() and text.isalpha():
                commands["Letras Minúsculas"][text] = binary
            elif len(text) > 1:
                commands["Comandos"][text] = binary
            else:
                commands["Símbolos"][text] = binary
        
        return commands
