from .Text import Text
from typing import Callable
from src.services.output import Color, Symbols
from src.services.events import Keys
from typing import TYPE_CHECKING, List, Tuple, Callable

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Button(Text):
    """
    Инициализация компонента Кнопка
    
    Args:
        x: Координата x компонента
        y: Координата y компонента
        width: Ширина компонента
        text: Текст компонента
        action: Действие, выполняемое при нажатии на компонент
        fg_color: Цвет текста (по умолчанию Color.WHITE)
        bg_color: Цвет фона (по умолчанию Color.RESET)
    """
    def __init__(self, x: int,
                 y: int,
                 width: int,
                 text: str,
                 action: Callable[[], None],
                 fg_color: str = Color.WHITE,
                 bg_color: str = Color.RESET):
        
        super().__init__(x, y, text, fg_color, bg_color)
        
        self.reactive('width', width)
        self.reactive('action', action)
        self.reactive('selected', False)
        
        self.process_text()
        
        self._events.append((Keys.ENTER, self.action))
        
    def process_text(self):
        self.width = max(len(self.text), self.width)
        self.text = f"{self.text:^{self.width}}"
        
    def draw(self, screen: 'Screen'):
        if self.selected:
            screen.draw_text(self.x, self.y, self.text, self.fg_color, self.bg_color)
        else:
            screen.draw_text(self.x, self.y, self.text, self.fg_color, self.bg_color)
