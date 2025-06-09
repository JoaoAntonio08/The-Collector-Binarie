"""
Módulo para execução de código binário de forma robusta com suporte a entrada de dados.
Esta versão corrige problemas na execução de comandos input() e print().
"""

import os
import sys
import subprocess
import tempfile
import io
import time
import threading
import queue
from contextlib import redirect_stdout, redirect_stderr

class BinaryCodeExecutorFixed:
    """
    Executor de código binário com suporte a execução real e interativa.
    """
    
    def __init__(self, interpreter):
        """
        Inicializa o executor de código.
        
        Args:
            interpreter: Instância do interpretador binário
        """
        self.interpreter = interpreter
    
    def execute_binary_code(self, binary_code):
        """
        Executa código binário traduzindo para Python e executando.
        
        Args:
            binary_code: Código binário a ser executado
            
        Returns:
            Resultado da execução
        """
        try:
            # Traduz o código binário para Python
            python_code = self.interpreter.traduzir_binario(binary_code)
            
            # Executa o código Python
            return self._execute_python_code(python_code)
        except Exception as e:
            return f"Erro ao executar código binário: {str(e)}"
    
    def _execute_python_code(self, python_code):
        """
        Executa código Python de forma segura.
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        # Método 1: Execução via subprocess (mais seguro e suporta input)
        try:
            return self._execute_via_subprocess(python_code)
        except Exception as e:
            # Se falhar, tenta o método 2
            try:
                return self._execute_direct(python_code)
            except Exception as e2:
                return f"Erro ao executar o código: {str(e2)}"
    
    def _execute_direct(self, python_code):
        """
        Executa código Python diretamente (sem suporte a input).
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        # Cria buffers para capturar stdout e stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Redireciona stdout e stderr
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            # Executa o código
            exec(python_code)
        
        # Obtém a saída
        stdout = stdout_buffer.getvalue()
        stderr = stderr_buffer.getvalue()
        
        # Combina stdout e stderr
        output = stdout
        if stderr:
            output += f"\n--- Erros ---\n{stderr}"
        
        return output
    
    def _execute_via_subprocess(self, python_code):
        """
        Executa código Python via subprocess para maior isolamento e suporte a input.
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        # Verifica se o código contém input()
        has_input = "input(" in python_code
        
        # Se contém input(), adiciona um tratamento especial
        if has_input:
            # Modifica o código para usar um valor padrão para input
            # Isso evita que o processo fique travado esperando entrada
            modified_code = python_code.replace("input(", "input('Entrada simulada: ')")
            
            # Cria um arquivo temporário com o código modificado
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(modified_code)
                temp_path = temp_file.name
            
            try:
                # Executa o código em um processo separado
                process = subprocess.Popen(
                    [sys.executable, temp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    text=True,
                    universal_newlines=True
                )
                
                # Captura a saída com timeout
                stdout, stderr = process.communicate(timeout=10)
                
                # Combina stdout e stderr
                output = stdout
                if stderr:
                    output += f"\n--- Erros ---\n{stderr}"
                
                # Adiciona uma nota sobre a entrada simulada
                if "Entrada simulada:" in output:
                    output += "\n\nNota: Para entrada de dados real, use o terminal interativo."
                
                return output
            
            except subprocess.TimeoutExpired:
                process.kill()
                return "Erro: A execução do código excedeu o tempo limite."
            
            except Exception as e:
                return f"Erro ao executar o código: {str(e)}"
            
            finally:
                # Remove o arquivo temporário
                try:
                    os.unlink(temp_path)
                except:
                    pass
        
        else:
            # Código sem input, execução normal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(python_code)
                temp_path = temp_file.name
            
            try:
                # Executa o código em um processo separado
                process = subprocess.Popen(
                    [sys.executable, temp_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    universal_newlines=True
                )
                
                # Captura a saída
                stdout, stderr = process.communicate(timeout=10)
                
                # Combina stdout e stderr
                output = stdout
                if stderr:
                    output += f"\n--- Erros ---\n{stderr}"
                
                return output
            
            except subprocess.TimeoutExpired:
                process.kill()
                return "Erro: A execução do código excedeu o tempo limite."
            
            except Exception as e:
                return f"Erro ao executar o código: {str(e)}"
            
            finally:
                # Remove o arquivo temporário
                try:
                    os.unlink(temp_path)
                except:
                    pass
