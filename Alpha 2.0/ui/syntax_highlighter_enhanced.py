"""
Módulo aprimorado para realce de sintaxe binária com validação e sublinhado vermelho para comandos inválidos.
Este módulo estende o realce de sintaxe original para adicionar validação em tempo real
e destacar visualmente comandos inválidos com sublinhado vermelho.
"""

import re
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtCore import QRegExp, Qt, QTimer

from binary_syntax_parser import BinarySyntaxParser

class BinarySyntaxHighlighterEnhanced(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        # Inicializa o parser de sintaxe binária
        self.parser = BinarySyntaxParser()
        self.binary_keywords = self.parser.binary_keywords
        
        # Formatos de texto para diferentes elementos
        self.formats = {
            'keyword': self._create_format(QColor("#ff79c6"), bold=True),
            'comment': self._create_format(QColor("#6272a4"), italic=True),
            'string': self._create_format(QColor("#f1fa8c")),
            'number': self._create_format(QColor("#8be9fd")),
            'operator': self._create_format(QColor("#ff79c6")),
            'invalid': self._create_format(QColor("#ff5555"), underline=True),
            'control': self._create_format(QColor("#bd93f9"), bold=True),
            'function': self._create_format(QColor("#50fa7b"), bold=True),
            'variable': self._create_format(QColor("#8be9fd")),
        }
        
        # Regras de realce
        self.highlighting_rules = []
        
        # 1. Palavras-chave binárias
        keyword_pattern = QRegExp(r'\b[01]{8}\b')
        self.highlighting_rules.append((keyword_pattern, self.formats['keyword']))
        
        # 2. Strings binárias entre aspas (ex: "01100001 01100010")
        self.highlighting_rules.append((QRegExp(r'"[01\s]*"'), self.formats['string']))
        
        # 3. Comentários: iniciados por // e vão até o fim da linha
        self.highlighting_rules.append((QRegExp(r'//[^\n]*'), self.formats['comment']))
        
        # Categorias especiais de tokens binários
        self.control_tokens = [
            "11010000",  # BINSTART
            "11010001",  # BINEND
            "11010010",  # BINVAR
            "11010011",  # BINFUNC
            "11010100",  # BINIF
            "11010101",  # BINELSE
            "11010110",  # BINLOOP
            "11010111",  # BINBREAK
            "11011000",  # BINCONT
            "11011001",  # BINRET
        ]
        
        self.function_tokens = [
            "11011010",  # BINPRINT
            "11011011",  # BININPUT
        ]
        
        # Lista para armazenar erros encontrados
        self.errors = []
        
        # Timer para validação com delay
        self.validation_timer = QTimer()
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.validate_document)
        
    def _create_format(self, color, bold=False, italic=False, underline=False):
        """
        Cria um formato de texto com as propriedades especificadas.
        
        Args:
            color: Cor do texto
            bold: Se True, texto em negrito
            italic: Se True, texto em itálico
            underline: Se True, texto sublinhado
            
        Returns:
            QTextCharFormat configurado
        """
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        
        if bold:
            fmt.setFontWeight(QFont.Bold)
        
        if italic:
            fmt.setFontItalic(True)
        
        if underline:
            fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)
            fmt.setUnderlineColor(color)
        
        return fmt
    
    def highlightBlock(self, text):
        """
        Realça um bloco de texto.
        
        Args:
            text: Texto a ser realçado
        """
        # Reseta os erros para este bloco
        self.errors = []
        
        # 1. Palavras binárias com ou sem significado
        pattern = r'\b[01]{8}\b'
        for match in re.finditer(pattern, text):
            word = match.group()
            start = match.start()
            length = len(word)
            
            # Determina o formato com base no tipo de token
            if word in self.binary_keywords:
                if word in self.control_tokens:
                    fmt = self.formats['control']
                elif word in self.function_tokens:
                    fmt = self.formats['function']
                else:
                    fmt = self.formats['keyword']
            else:
                fmt = self.formats['invalid']
                self.errors.append((self.currentBlock().blockNumber() + 1, start, length, f"Token desconhecido: '{word}'"))
            
            self.setFormat(start, length, fmt)
        
        # 2. Strings entre aspas
        for match in re.finditer(r'"[01\s]*"', text):
            self.setFormat(match.start(), len(match.group()), self.formats['string'])
        
        # 3. Comentários
        for match in re.finditer(r'//[^\n]*', text):
            self.setFormat(match.start(), len(match.group()), self.formats['comment'])
        
        # Aplica as demais regras (strings, comentários, etc.)
        for pattern, fmt in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)
        
        # Agenda validação do documento completo
        self.validation_timer.start(500)  # 500ms de delay para não sobrecarregar durante digitação
    
    def validate_document(self):
        """
        Valida o documento completo e destaca erros de sintaxe.
        """
        # Obtém o texto completo do documento
        doc = self.document()
        text = doc.toPlainText()
        
        # Valida a sintaxe usando o parser
        syntax_errors = self.parser.validate_binary_syntax(text)
        
        # Limpa formatações de erro anteriores
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()
        
        # Aplica formatação de erro para cada erro de sintaxe
        for line_num, error_msg in syntax_errors:
            # Posiciona o cursor no início da linha com erro
            cursor.setPosition(doc.findBlockByLineNumber(line_num - 1).position())
            
            # Seleciona a linha inteira
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            
            # Aplica o formato de erro
            format_error = QTextCharFormat()
            format_error.setUnderlineStyle(QTextCharFormat.WaveUnderline)
            format_error.setUnderlineColor(QColor("#ff5555"))
            format_error.setToolTip(error_msg)
            
            # Armazena o erro para referência
            self.errors.append((line_num, 0, cursor.selectedText().length(), error_msg))
        
        cursor.endEditBlock()
        
        # Emite sinal de que o documento foi modificado para atualizar a visualização
        doc.markContentsDirty(0, doc.characterCount())
    
    def get_errors(self):
        """
        Retorna a lista de erros encontrados.
        
        Returns:
            Lista de tuplas (linha, posição, comprimento, mensagem)
        """
        return self.errors
