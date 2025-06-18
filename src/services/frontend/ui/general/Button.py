from .Text import Text
from typing import Callable
from src.services.output import Color, Symbols
from src.services.events import Keys
from typing import TYPE_CHECKING, List, Tuple, Callable

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Button(Text):
    def __init__(self, x: int,
                 y: int,
                 width: int,
                 text: str,
                 action: Callable[[], None],
                 fg_color: str = Color.WHITE,
                 bg_color: str = Color.RESET,
                 selected_color: str = Color.BRIGHT_WHITE,
                 selected_bg_color: str = Color.BRIGHT_BLACK,
                 need_selection: bool = False):
        
        super().__init__(x, y, text, fg_color, bg_color)
        
        self.reactive('width', width)
        self.reactive('action', action)
        self.reactive('need_selection', need_selection)
        
        self.computed('current_fg_color', lambda: selected_color if self.selected else fg_color, ['selected'])
        self.computed('current_bg_color', lambda: selected_bg_color if self.selected else bg_color, ['selected'])
        
        self.process_text()
        
        self._events.append((Keys.ENTER, self.process_action))
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
        selected_color: Цвет текста при выборе (по умолчанию Color.BRIGHT_WHITE)
        selected_bg_color: Цвет фона при выборе (по умолчанию Color.BRIGHT_BLACK)
        need_selection: Необходимость выбора (по умолчанию False)
    """
        
    def process_action(self):
        if self.need_selection and not self.selected: return
        self.action()
        
    def process_text(self):
        self.width = max(len(self.text), self.width)
        self.text = f"{self.text:^{self.width}}"
        
    def draw(self, screen: 'Screen'):
        if self.selected:
            screen.draw_text(self.x, self.y, self.text, self.current_fg_color, self.current_bg_color)
        else:
            screen.draw_text(self.x, self.y, self.text, self.current_fg_color, self.current_bg_color)
