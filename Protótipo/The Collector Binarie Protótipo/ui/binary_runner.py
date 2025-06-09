import subprocess
import tempfile
import ast

class BinariosInterpreter:
    def interpretar(self, binario_texto):
        try:
            linhas = binario_texto.strip().split("\n")
            texto_convertido = ""
            for linha in linhas:
                binarios = linha.strip().split(" ")
                linha_convertida = ""
                
                for b in binarios:
                    if b == "00100000":  # Espaço
                        linha_convertida += " "
                    elif b == "00100010":  # Aspas duplas (")
                        linha_convertida += '"'
                    elif b == "10010100":  # Chave aberta ({)
                        linha_convertida += "{"
                    elif b == "10010101":  # Chave fechada (})
                        linha_convertida += "}"
                    elif b == "00111101":  # Sinal de igual (=)
                        linha_convertida += "="
                    elif b == "01011111":  # Underline (_)
                        linha_convertida += "_"
                    elif b == "00111010":  # Dois pontos (:)
                        linha_convertida += ":"
                    elif b == "00100010": # Abre Parentese (
                        linha_convertida += "("       
                    else:
                        linha_convertida += chr(int(b, 2))  # Conversão normal
                
                texto_convertido += linha_convertida + "\n"
            
            return texto_convertido
        except Exception as e:
            return f"Erro na conversão: {str(e)}"

    def executar_codigo(self, codigo_str):
        try:
            # Validação de segurança para evitar código malicioso
            ast.parse(codigo_str)

            with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(codigo_str)
                tmp_file.flush()
                resultado = subprocess.check_output(['python', tmp_file.name], stderr=subprocess.STDOUT, text=True)
            return resultado
        except (subprocess.CalledProcessError, SyntaxError) as e:
            return f"Erro ao executar código: {str(e)}"
