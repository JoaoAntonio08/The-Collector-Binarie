import re
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

class BinarySyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []

        # Estilos
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff79c6"))
        keyword_format.setFontWeight(QFont.Bold)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))
        comment_format.setFontItalic(True)

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#8be9fd"))

        # Regras (adaptar conforme suas palavras-chave binárias ou comandos futuros)
        self.binary_keywords = {
        # Dígitos
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

        # Palavras-chave
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
        "10001111": "(",
        "10010000": ")",
        "10010001": ":",
        "10010010": "print()",
        "00100000": "espaco",
        "10010011": "_",    # Underline (_)
        "10010100": "{",    # Chave aberta ({)
        "10010101": "}",    # Chave fechada (})
        "10010110": "[",    # Colchete aberto ([)
        "10010111": "]",    # Colchete fechado (])
        "10011000": "'",    # Aspas simples (')
        "10011001": ",",    # Vírgula (,)
        "10011010": ".",    # Ponto final (.)
        "10011011": ";",    # Ponto e vírgula (;)
        "10011100": "\\",   # Barra invertida (\)
        "10011101": "%",    # Módulo (%)
        "10011110": "!",    # Exclamação (!)
        "10011111": "<",    # Menor que (<)
        "10100000": ">",    # Maior que (>)
        "10100001": "&",    # Operador lógico (AND)
        "10100010": "|"    # Operador lógico (OR)
        }
        #1. Palavras-chave binárias
        keyword_pattern = QRegExp(r'\b[01]{8}\b')
        self.highlighting_rules.append((keyword_pattern, keyword_format))

        # 2. Strings binárias entre aspas (ex: "01100001 01100010")
        self.highlighting_rules.append((QRegExp(r'"[01\s]*"'), string_format))

        # 3. Comentários: iniciados por // e vão até o fim da linha
        self.highlighting_rules.append((QRegExp(r'//[^\n]*'), comment_format))

    def highlightBlock(self, text):
        # 1. Palavras binárias com ou sem significado
        pattern = r'\b[01]{8}\b'
        for match in re.finditer(pattern, text):
            word = match.group()
            start = match.start()
            length = len(word)

            fmt = QTextCharFormat()
            if word in self.binary_keywords:
                fmt.setForeground(QColor("#ff79c6"))  # Comando válido
            else:
                fmt.setForeground(QColor("gray"))
                fmt.setUnderlineStyle(QTextCharFormat.SingleUnderline)
                fmt.setUnderlineColor(QColor("red"))

            self.setFormat(start, length, fmt)

        # 2. Strings entre aspas
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))
        for match in re.finditer(r'"[01\s]*"', text):
            self.setFormat(match.start(), len(match.group()), string_format)

        # 3. Comentários
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))
        comment_format.setFontItalic(True)
        for match in re.finditer(r'//[^\n]*', text):
            self.setFormat(match.start(), len(match.group()), comment_format)

        # Aplica as demais regras (strings, comentários, etc.)
        for pattern, fmt in self.highlighting_rules:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, fmt)
                index = pattern.indexIn(text, index + length)