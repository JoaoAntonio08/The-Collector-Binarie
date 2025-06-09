"""
Módulo para gerenciamento de arquivos temporários e recuperação de sessão.
Este módulo implementa funcionalidades para salvar automaticamente o conteúdo
do editor e permitir a recuperação em caso de falhas.
"""

import os
import json
import time
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class TempFileManager:
    def __init__(self, temp_dir: str = None):
        """
        Inicializa o gerenciador de arquivos temporários.
        
        Args:
            temp_dir: Diretório para armazenar arquivos temporários.
                     Se None, usa o diretório padrão ~/.the_collector_binarie/temp
        """
        if temp_dir is None:
            home_dir = os.path.expanduser("~")
            self.temp_dir = os.path.join(home_dir, ".the_collector_binarie", "temp")
        else:
            self.temp_dir = temp_dir
            
        # Garante que o diretório existe
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Arquivo de metadados para rastrear sessões
        self.metadata_file = os.path.join(self.temp_dir, "sessions.json")
        self.sessions = self._load_metadata()
        
        # Intervalo de salvamento automático (em segundos)
        self.autosave_interval = 60
        self.last_autosave_time = time.time()
        
    def _load_metadata(self) -> Dict:
        """
        Carrega os metadados das sessões salvas.
        
        Returns:
            Dicionário com informações das sessões
        """
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Se o arquivo estiver corrompido, cria um novo
                return {"sessions": []}
        else:
            return {"sessions": []}
    
    def _save_metadata(self):
        """Salva os metadados das sessões no arquivo."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, indent=2)
    
    def create_session(self) -> str:
        """
        Cria uma nova sessão para rastreamento de arquivos temporários.
        
        Returns:
            ID da sessão criada
        """
        session_id = f"session_{int(time.time())}_{os.getpid()}"
        session_dir = os.path.join(self.temp_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Registra a sessão nos metadados
        session_info = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "tabs": []
        }
        
        self.sessions["sessions"].append(session_info)
        self._save_metadata()
        
        return session_id
    
    def save_tab_content(self, session_id: str, tab_index: int, content: str, 
                         file_path: Optional[str] = None, tab_title: str = "Sem título") -> bool:
        """
        Salva o conteúdo de uma aba em um arquivo temporário.
        
        Args:
            session_id: ID da sessão
            tab_index: Índice da aba
            content: Conteúdo a ser salvo
            file_path: Caminho do arquivo original (se existir)
            tab_title: Título da aba
            
        Returns:
            True se o salvamento foi bem-sucedido, False caso contrário
        """
        try:
            session_dir = os.path.join(self.temp_dir, session_id)
            if not os.path.exists(session_dir):
                os.makedirs(session_dir, exist_ok=True)
            
            # Nome do arquivo temporário
            temp_file = os.path.join(session_dir, f"tab_{tab_index}.tmp")
            
            # Salva o conteúdo
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Atualiza os metadados
            for session in self.sessions["sessions"]:
                if session["id"] == session_id:
                    # Verifica se a aba já existe
                    tab_exists = False
                    for tab in session["tabs"]:
                        if tab["index"] == tab_index:
                            tab["temp_file"] = temp_file
                            tab["original_file"] = file_path
                            tab["title"] = tab_title
                            tab["last_modified"] = datetime.now().isoformat()
                            tab_exists = True
                            break
                    
                    # Se a aba não existe, adiciona
                    if not tab_exists:
                        session["tabs"].append({
                            "index": tab_index,
                            "temp_file": temp_file,
                            "original_file": file_path,
                            "title": tab_title,
                            "last_modified": datetime.now().isoformat()
                        })
                    
                    session["last_modified"] = datetime.now().isoformat()
                    break
            
            self._save_metadata()
            return True
        
        except Exception as e:
            print(f"Erro ao salvar conteúdo da aba: {e}")
            return False
    
    def check_autosave(self, force: bool = False) -> bool:
        """
        Verifica se é hora de fazer um salvamento automático.
        
        Args:
            force: Se True, força o salvamento independente do intervalo
            
        Returns:
            True se for hora de salvar, False caso contrário
        """
        current_time = time.time()
        if force or (current_time - self.last_autosave_time >= self.autosave_interval):
            self.last_autosave_time = current_time
            return True
        return False
    
    def get_recoverable_sessions(self) -> List[Dict]:
        """
        Retorna a lista de sessões que podem ser recuperadas.
        
        Returns:
            Lista de dicionários com informações das sessões
        """
        recoverable = []
        for session in self.sessions["sessions"]:
            # Verifica se a sessão tem abas
            if session["tabs"]:
                # Verifica se os arquivos temporários existem
                valid_tabs = []
                for tab in session["tabs"]:
                    if os.path.exists(tab["temp_file"]):
                        valid_tabs.append(tab)
                
                if valid_tabs:
                    session_copy = session.copy()
                    session_copy["tabs"] = valid_tabs
                    recoverable.append(session_copy)
        
        return recoverable
    
    def recover_session(self, session_id: str) -> List[Tuple[str, str, str]]:
        """
        Recupera os conteúdos de uma sessão.
        
        Args:
            session_id: ID da sessão a ser recuperada
            
        Returns:
            Lista de tuplas (conteúdo, caminho_original, título)
        """
        recovered_tabs = []
        
        for session in self.sessions["sessions"]:
            if session["id"] == session_id:
                for tab in session["tabs"]:
                    temp_file = tab["temp_file"]
                    if os.path.exists(temp_file):
                        try:
                            with open(temp_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            recovered_tabs.append((
                                content,
                                tab["original_file"],
                                tab["title"]
                            ))
                        except Exception as e:
                            print(f"Erro ao recuperar aba {tab['index']}: {e}")
                
                break
        
        return recovered_tabs
    
    def clean_old_sessions(self, days: int = 7):
        """
        Remove sessões antigas.
        
        Args:
            days: Número de dias para considerar uma sessão como antiga
        """
        current_time = time.time()
        seconds_in_day = 86400  # 24 * 60 * 60
        cutoff_time = current_time - (days * seconds_in_day)
        
        sessions_to_keep = []
        
        for session in self.sessions["sessions"]:
            try:
                created_at = datetime.fromisoformat(session["created_at"]).timestamp()
                if created_at > cutoff_time:
                    sessions_to_keep.append(session)
                else:
                    # Remove os arquivos da sessão
                    session_dir = os.path.join(self.temp_dir, session["id"])
                    if os.path.exists(session_dir):
                        shutil.rmtree(session_dir)
            except (ValueError, KeyError):
                # Se houver erro no formato da data, mantém a sessão
                sessions_to_keep.append(session)
        
        self.sessions["sessions"] = sessions_to_keep
        self._save_metadata()
    
    def delete_session(self, session_id: str) -> bool:
        """
        Remove uma sessão específica.
        
        Args:
            session_id: ID da sessão a ser removida
            
        Returns:
            True se a sessão foi removida, False caso contrário
        """
        for i, session in enumerate(self.sessions["sessions"]):
            if session["id"] == session_id:
                # Remove os arquivos da sessão
                session_dir = os.path.join(self.temp_dir, session_id)
                if os.path.exists(session_dir):
                    shutil.rmtree(session_dir)
                
                # Remove a sessão dos metadados
                self.sessions["sessions"].pop(i)
                self._save_metadata()
                return True
        
        return False
