from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QToolTip
from PyQt5.QtGui import QPainter, QColor, QFont, QTextFormat, QTextCursor
from PyQt5.QtCore import Qt, QRect, QSize, QTimer
from ui.syntax_highlighter import BinarySyntaxHighlighter
import re

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        self.setStyleSheet("background-color: #2e2e2e;")

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  Realce de sintaxe
        self.highlighter = BinarySyntaxHighlighter(self.document())

        #  Área de número de linha
        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Habilita detecção de movimento do mouse
        self.setMouseTracking(True)

        # Tooltip binário
        self.tooltip_timer = QTimer()
        self.tooltip_timer.setSingleShot(True)
        self.tooltip_timer.timeout.connect(self.show_binary_tooltip)
        self.last_mouse_pos = None

    def mouseMoveEvent(self, event):
        self.last_mouse_pos = event.pos()
        self.tooltip_timer.start(100)
        super().mouseMoveEvent(event)

    def show_binary_tooltip(self):
        cursor = self.cursorForPosition(self.last_mouse_pos)
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()

        if re.fullmatch(r'[01]{8}', word):
            meaning = self.highlighter.binary_keywords.get(word, "Comando desconhecido")
            QToolTip.showText(self.mapToGlobal(self.last_mouse_pos), f"{word} → {meaning}", self)
        else:
            QToolTip.hideText()

    def line_number_area_width(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2e2e2e"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.gray)
                painter.drawText(0, int(top), self.line_number_area.width() - 5,
                                 int(self.fontMetrics().height()), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor("#44475a")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


__all__ = ['CodeEditor']