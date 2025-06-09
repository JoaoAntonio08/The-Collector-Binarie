"""
Módulo para execução de código binário de forma robusta.
Este módulo corrige problemas na execução de código e garante funcionamento correto.
"""

import os
import sys
import subprocess
import tempfile
import io
from contextlib import redirect_stdout, redirect_stderr

class BinaryCodeExecutor:
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
        # Método 1: Execução direta com captura de saída
        try:
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
        except Exception as e:
            # Se falhar, tenta o método 2
            return self._execute_via_subprocess(python_code)
    
    def _execute_via_subprocess(self, python_code):
        """
        Executa código Python via subprocess para maior isolamento.
        
        Args:
            python_code: Código Python a ser executado
            
        Returns:
            Resultado da execução
        """
        try:
            # Cria um arquivo temporário com o código
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(python_code)
                temp_path = temp_file.name
            
            # Executa o código em um processo separado
            process = subprocess.Popen(
                [sys.executable, temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )
            
            # Captura a saída
            stdout, stderr = process.communicate(timeout=10)  # Timeout de 10 segundos
            
            # Remove o arquivo temporário
            try:
                os.unlink(temp_path)
            except:
                pass
            
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
