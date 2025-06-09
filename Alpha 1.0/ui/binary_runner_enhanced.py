"""
Módulo aprimorado para execução de comandos binários com terminal integrado.
Este módulo estende o interpretador binário para permitir a execução de comandos
em formato binário e integração com o terminal interativo.
"""

import subprocess
import tempfile
import ast
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, List, Tuple, Optional

from binary_syntax_parser import BinarySyntaxParser

class BinaryRunner:
    def __init__(self):
        """Inicializa o executor de código binário."""
        self.parser = BinarySyntaxParser()
        self.last_execution_result = ""
        self.execution_history = []
        self.max_history_size = 50
        
    def interpretar(self, binario_texto: str) -> str:
        """
        Interpreta código binário e converte para Python.
        
        Args:
            binario_texto: String contendo código em formato binário
            
        Returns:
            String contendo código Python equivalente
        """
        try:
            # Usa o parser avançado para traduzir binário para Python
            return self.parser.parse_binary_to_python(binario_texto)
        except Exception as e:
            return f"Erro na conversão: {str(e)}"
    
    def validar_codigo(self, codigo_python: str) -> Tuple[bool, str]:
        """
        Valida a sintaxe do código Python.
        
        Args:
            codigo_python: String contendo código Python
            
        Returns:
            Tupla (é_válido, mensagem_de_erro)
        """
        try:
            ast.parse(codigo_python)
            return True, ""
        except SyntaxError as e:
            return False, f"Erro de sintaxe: {str(e)}"
        except Exception as e:
            return False, f"Erro ao validar código: {str(e)}"
    
    def executar_codigo(self, codigo_python: str, use_subprocess: bool = True) -> str:
        """
        Executa código Python e retorna o resultado.
        
        Args:
            codigo_python: String contendo código Python
            use_subprocess: Se True, executa em um processo separado para maior segurança
            
        Returns:
            String contendo a saída da execução
        """
        # Valida o código antes de executar
        is_valid, error_msg = self.validar_codigo(codigo_python)
        if not is_valid:
            self.last_execution_result = error_msg
            self.add_to_history(codigo_python, error_msg)
            return error_msg
        
        try:
            if use_subprocess:
                # Execução em processo separado (mais seguro)
                with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp_file:
                    tmp_file.write(codigo_python)
                    tmp_file.flush()
                    resultado = subprocess.check_output(
                        ['python3', tmp_file.name], 
                        stderr=subprocess.STDOUT, 
                        text=True,
                        timeout=5  # Timeout de 5 segundos para evitar execuções infinitas
                    )
            else:
                # Execução no mesmo processo (menos seguro, mas permite interatividade)
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                redirected_output = io.StringIO()
                
                try:
                    sys.stdout = redirected_output
                    sys.stderr = redirected_output
                    
                    # Executa o código em um namespace isolado
                    exec_globals = {}
                    exec(codigo_python, exec_globals)
                    
                    resultado = redirected_output.getvalue()
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
            
            self.last_execution_result = resultado
            self.add_to_history(codigo_python, resultado)
            return resultado
        
        except subprocess.TimeoutExpired:
            error_msg = "Erro: Tempo limite de execução excedido (5 segundos)"
            self.last_execution_result = error_msg
            self.add_to_history(codigo_python, error_msg)
            return error_msg
        except subprocess.CalledProcessError as e:
            error_msg = f"Erro ao executar código: {e.output}"
            self.last_execution_result = error_msg
            self.add_to_history(codigo_python, error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Erro ao executar código: {str(e)}"
            self.last_execution_result = error_msg
            self.add_to_history(codigo_python, error_msg)
            return error_msg
    
    def executar_binario(self, codigo_binario: str) -> str:
        """
        Interpreta e executa código binário diretamente.
        
        Args:
            codigo_binario: String contendo código em formato binário
            
        Returns:
            String contendo a saída da execução
        """
        # Primeiro traduz o binário para Python
        codigo_python = self.interpretar(codigo_binario)
        
        # Verifica se houve erro na tradução
        if codigo_python.startswith("Erro"):
            return codigo_python
        
        # Executa o código Python traduzido
        return self.executar_codigo(codigo_python)
    
    def executar_comando(self, comando: str, is_binary: bool = False) -> str:
        """
        Executa um comando, que pode ser em formato binário ou Python.
        
        Args:
            comando: String contendo o comando a ser executado
            is_binary: Se True, trata o comando como binário; caso contrário, como Python
            
        Returns:
            String contendo a saída da execução
        """
        if is_binary:
            return self.executar_binario(comando)
        else:
            return self.executar_codigo(comando)
    
    def add_to_history(self, comando: str, resultado: str):
        """
        Adiciona um comando e seu resultado ao histórico de execução.
        
        Args:
            comando: String contendo o comando executado
            resultado: String contendo o resultado da execução
        """
        self.execution_history.append((comando, resultado))
        
        # Limita o tamanho do histórico
        if len(self.execution_history) > self.max_history_size:
            self.execution_history.pop(0)
    
    def get_history(self) -> List[Tuple[str, str]]:
        """
        Retorna o histórico de execução.
        
        Returns:
            Lista de tuplas (comando, resultado)
        """
        return self.execution_history
    
    def clear_history(self):
        """Limpa o histórico de execução."""
        self.execution_history = []
        self.last_execution_result = ""
