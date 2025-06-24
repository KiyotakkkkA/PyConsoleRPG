from src.services.frontend.core import Component
from src.services.output import Color
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Text(Component):
    """
    Компонент для отображения текста
    """
    def __init__(self, x: int, y: int, text: str = "", 
                 fg_color: str = Color.WHITE, bg_color: str = Color.RESET,
                 paddings: tuple = (0, 0, 0, 0),
                 auto_break: bool = False,
                 max_width: int = None):
        """
        Инициализация компонента Text
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            text: Текст компонента
            fg_color: Цвет текста (по умолчанию Color.WHITE)
            bg_color: Цвет фона (по умолчанию Color.RESET)
            paddings: (pt, pb, pr, pl) по умолчанию (0, 0, 0, 0)
            auto_break: Автоматическое перенос строк (по умолчанию False)
            max_width: Максимальная ширина компонента (по умолчанию None)
        """
        lines = text.split('\n')
        width = max([len(line) for line in lines]) if lines else 0
        height = len(lines)
        
        super().__init__(x, y, width, height, paddings)
        
        self.reactive('text', text)
        self.reactive('fg_color', fg_color)
        self.reactive('bg_color', bg_color)
        
        self.reactive('auto_break', auto_break)
        self.reactive('max_width', max_width)
        
        self.lines: List[str] = []
        self.process_text()
    
    def process_text(self):
        """
        Обработка текста и разделение его на строки
        """
        if self.auto_break:
            _lines = []
            _words = self.text.replace('\n', ' ').split(' ')
            
            for word in _words:
                if not _lines or len(_lines[-1]) + len(word) + 1 > self.max_width:
                    _lines.append(word)
                else:
                    _lines[-1] += ' ' + word
            
            self.lines = _lines
            self.width = max([len(line) for line in self.lines]) if self.lines else 0
            self.height = len(self.lines)
            return
        
        self.lines = self.text.split('\n')
        self.width = max([len(line) for line in self.lines]) if self.lines else 0
        self.height = len(self.lines)
    
    def set_text(self, text: str):
        """
        Установка текста компонента
        
        Args:
            text: Новый текст
        """
        self.text = text
        self.process_text()
        
    def set_fg_color(self, color: str):
        """
        Установка цвета текста
        
        Args:
            color: Новый цвет текста
        """
        self.fg_color = color
        
    def set_bg_color(self, color: str):
        """
        Установка цвета фона
        
        Args:
            color: Новый цвет фона
        """
        self.bg_color = color
    
    def draw(self, screen: 'Screen'):
        """
        Отрисовка компонента на экране
        
        Args:
            screen: Экран, на который производится отрисовка
        """
        for i, line in enumerate(self.lines):
            y_pos = self.y + i
            if 0 <= y_pos < screen.height:
                screen.draw_text(self.x, y_pos, line, self.fg_color, self.bg_color)