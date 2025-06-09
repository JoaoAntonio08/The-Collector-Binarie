"""
Módulo para implementação do diálogo Sobre Nós.
Este módulo fornece informações sobre o The Collector Binarie,
com suporte a internacionalização (pt/en) e centralização.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QApplication, QDesktopWidget
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

class AboutDialog(QDialog):
    """
    Diálogo com informações sobre o The Collector Binarie.
    Suporta Português e Inglês, e abre centralizado.
    """
    
    def __init__(self, parent=None):
        """
        Inicializa o diálogo.
        
        Args:
            parent: Widget pai
        """
        super().__init__(parent)
        
        # Textos para internacionalização
        self._setup_texts()
        
        # Configurações da janela
        self.current_lang = "pt" # Padrão Português
        self.setWindowTitle(self.texts[self.current_lang]["title"])
        self.setMinimumSize(600, 450) # Tamanho mínimo para acomodar conteúdo
        self.setModal(True)
        
        # Configuração da interface
        self._setup_ui()
        
        # Aplica textos iniciais
        self._update_texts()
        
        # Centraliza a janela
        self._center_window()
    
    def _setup_texts(self):
        """Define os textos para Português e Inglês."""
        self.texts = {
            "pt": {
                "title": "Sobre Nós",
                "dialog_title": "The Collector Binarie",
                "subtitle": "Linguagem V1B0RA",
                "content": """
<h3>Conteúdo Autoral</h3>

<p>O <b>The Collector Binarie</b> (ou <b>TH Binarie</b>) é uma IDE inovadora desenvolvida para facilitar o aprendizado e uso da linguagem V1B0RA (pronuncia-se "vi one bi zero ar ei" ou simplesmente "víbora").</p>

<p>A linguagem V1B0RA representa uma abordagem única para programação, inspirada no código binário mas com uma sintaxe mais acessível e intuitiva. O nome é uma referência bem-humorada à linguagem Python, já que ambas são "cobras" no mundo da programação - uma brincadeira com os zeros e uns do código binário.</p>

<h3>Recursos Principais</h3>

<p>Nossa IDE oferece um ambiente completo para desenvolvimento, com recursos como:</p>
<ul>
<li>Editor de código com destaque de sintaxe</li>
<li>Explorador de arquivos estilo workspace</li>
<li>Terminal interativo integrado</li>
<li>Tradução bidirecional entre texto e código binário</li>
<li>Guia de referência integrado</li>
<li>Múltiplos temas visuais</li>
</ul>

<h3>Filosofia</h3>

<p>Acreditamos que o aprendizado de programação deve ser acessível a todos. Nossa IDE foi projetada com foco na experiência do usuário, tornando o processo de codificação mais intuitivo e agradável.</p>

<p>Valorizamos a comunidade de desenvolvedores e incentivamos a colaboração e o compartilhamento de conhecimento. O The Collector Binarie é uma ferramenta para todos que desejam explorar o fascinante mundo da programação de uma perspectiva diferente.</p>

<h3>Agradecimentos</h3>

<p>Agradecemos a todos os desenvolvedores, testadores e entusiastas que contribuíram para tornar este projeto uma realidade. Seu feedback e suporte são fundamentais para o contínuo aprimoramento desta ferramenta.</p>

<p><i>© 2025 The Collector Binarie. Todos os direitos reservados.</i></p>
""",
                "close_button": "Fechar",
                "lang_pt": "Português",
                "lang_en": "English"
            },
            "en": {
                "title": "About Us",
                "dialog_title": "The Collector Binarie",
                "subtitle": "V1B0RA Language",
                "content": """
<h3>Original Content</h3>

<p><b>The Collector Binarie</b> (or <b>TH Binarie</b>) is an innovative IDE developed to facilitate the learning and use of the V1B0RA language (pronounced "vi one bi zero ar ei" or simply "viper").</p>

<p>The V1B0RA language represents a unique approach to programming, inspired by binary code but with a more accessible and intuitive syntax. The name is a humorous reference to the Python language, as both are "snakes" in the programming world – a play on the zeros and ones of binary code.</p>

<h3>Main Features</h3>

<p>Our IDE offers a complete development environment, with features such as:</p>
<ul>
<li>Code editor with syntax highlighting</li>
<li>Workspace-style file explorer</li>
<li>Integrated interactive terminal</li>
<li>Bidirectional translation between text and binary code</li>
<li>Integrated reference guide</li>
<li>Multiple visual themes</li>
</ul>

<h3>Philosophy</h3>

<p>We believe that learning to program should be accessible to everyone. Our IDE was designed with a focus on user experience, making the coding process more intuitive and enjoyable.</p>

<p>We value the developer community and encourage collaboration and knowledge sharing. The Collector Binarie is a tool for everyone who wants to explore the fascinating world of programming from a different perspective.</p>

<h3>Acknowledgments</h3>

<p>We thank all the developers, testers, and enthusiasts who contributed to making this project a reality. Your feedback and support are fundamental to the continuous improvement of this tool.</p>

<p><i>© 2025 The Collector Binarie. All rights reserved.</i></p>
""",
                "close_button": "Close",
                "lang_pt": "Português",
                "lang_en": "English"
            }
        }

    def _setup_ui(self):
        """Configura a interface do diálogo."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Layout para botões de idioma
        lang_layout = QHBoxLayout()
        lang_layout.addStretch()
        self.pt_button = QPushButton(self.texts["pt"]["lang_pt"])
        self.pt_button.clicked.connect(lambda: self._switch_language("pt"))
        self.pt_button.setCheckable(True)
        self.pt_button.setChecked(self.current_lang == "pt")
        lang_layout.addWidget(self.pt_button)
        
        self.en_button = QPushButton(self.texts["pt"]["lang_en"])
        self.en_button.clicked.connect(lambda: self._switch_language("en"))
        self.en_button.setCheckable(True)
        self.en_button.setChecked(self.current_lang == "en")
        lang_layout.addWidget(self.en_button)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)
        
        # Área de rolagem para o conteúdo
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        # Widget de conteúdo
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(15)
        
        # Título
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.title_label)
        
        # Subtítulo
        self.subtitle_label = QLabel()
        self.subtitle_label.setFont(QFont("Arial", 14))
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.subtitle_label)
        
        # Separador
        separator = QLabel()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #555555;") # Cor pode ser ajustada pelo tema
        content_layout.addWidget(separator)
        
        # Conteúdo principal
        self.content_text = QLabel()
        self.content_text.setWordWrap(True)
        self.content_text.setTextFormat(Qt.RichText)
        self.content_text.setOpenExternalLinks(True)
        content_layout.addWidget(self.content_text)
        
        # Adiciona o widget de conteúdo à área de rolagem
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Botão de fechar
        self.close_button = QPushButton()
        self.close_button.clicked.connect(self.accept)
        self.close_button.setFixedWidth(100)
        main_layout.addWidget(self.close_button, 0, Qt.AlignCenter)

    def _update_texts(self):
        """Atualiza todos os textos da UI para o idioma atual."""
        lang_texts = self.texts[self.current_lang]
        self.setWindowTitle(lang_texts["title"])
        self.title_label.setText(lang_texts["dialog_title"])
        self.subtitle_label.setText(lang_texts["subtitle"])
        self.content_text.setText(lang_texts["content"])
        self.close_button.setText(lang_texts["close_button"])
        # Atualiza texto dos botões de idioma (se necessário, mas geralmente são fixos)
        self.pt_button.setText(self.texts["pt"]["lang_pt"])
        self.en_button.setText(self.texts["pt"]["lang_en"])
        
        # Atualiza estado dos botões de idioma
        self.pt_button.setChecked(self.current_lang == "pt")
        self.en_button.setChecked(self.current_lang == "en")

    def _switch_language(self, lang):
        """Muda o idioma atual e atualiza a UI."""
        if lang in self.texts and self.current_lang != lang:
            self.current_lang = lang
            self._update_texts()

    def _center_window(self):
        """Centraliza a janela na tela."""
        try:
            # Obtém a geometria da tela disponível
            screen_geometry = QApplication.desktop().availableGeometry(self)
            # Obtém a geometria da janela atual
            window_geometry = self.frameGeometry()
            # Calcula o ponto central
            center_point = screen_geometry.center()
            # Move o canto superior esquerdo da janela para o ponto central
            window_geometry.moveCenter(center_point)
            # Move a janela
            self.move(window_geometry.topLeft())
        except Exception as e:
            print(f"Erro ao centralizar a janela: {e}")

