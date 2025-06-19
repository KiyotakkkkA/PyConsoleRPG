from .Panel import Panel
from src.services.frontend.core import Alignment
from src.services.output import Color
from src.services.frontend.ui.general import Button, Text
from src.services.events import Keys
from typing import Callable, Tuple, List

class DialogWindow(Panel):
    
    __phrases = {
        'OK': 'Хорошо [1]',
        'YES': 'Да [1]',
        'NO': 'Нет [2]',
        'CANCEL': 'Отмена [3]'
    }
    
    def __init__(self, x: int, y: int, width: int,
                 height: int, filler=" ",
                 text: str = "",
                 ctype: str = "OK",
                 paddings: tuple = (1, 1, 1, 1),
                 border_color: str = Color.WHITE,
                 filler_color: str = Color.RESET,
                 text_color: str = Color.WHITE):
        """
        Инициализация компонента Диалоговое окно
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            width: Ширина компонента
            height: Высота компонента
            text: Текст компонента
            type: Тип компонента (по умолчанию 'OK')
            filler: Заполнитель компонента (по умолчанию ' ')
            paddings: (pt, pb, pr, pl) по умолчанию (1, 1, 1, 1)
            border_color: Цвет границ компонента (по умолчанию Color.WHITE)
            filler_color: Цвет заполнителя компонента (по умолчанию Color.RESET)
            text_color: Цвет текста компонента (по умолчанию Color.WHITE)
        """
        super().__init__(x, y, width, height, '', filler, Alignment.LEFT, paddings, border_color, filler_color)
        
        self.reactive('text', text)
        self.reactive('ctype', ctype)
        self.reactive('text_color', text_color)
        self.reactive('buttons', [])
        
        self._types = {
            "OK": [
                Button(self.x + 2, self.y + self.height - 2, 1, self.__phrases['OK'], lambda: None)
            ],
            "YES_NO": [
                Button(self.x + 2, self.y + self.height - 2, 1, self.__phrases['YES'], lambda: None),
                Button(self.x + (self.width - len(self.__phrases['NO'])) // 2, self.y + self.height - 2, 1, self.__phrases['NO'], lambda: None)
            ],
            "YES_NO_CANCEL": [
                Button(self.x + 2, self.y + self.height - 2, 1, self.__phrases['YES'], lambda: None),
                Button(self.x + self.width // 3 - (len(self.__phrases['NO']) // 2), self.y + self.height - 2, 1, self.__phrases['NO'], lambda: None),
                Button(self.x + self.width // 3 * 2 - (len(self.__phrases['CANCEL']) // 2), self.y + self.height - 2, 1, self.__phrases['CANCEL'], lambda: None)
            ]
        }
        
        self.text = Text(self.x + 2, self.y + 1, self.text, self.text_color, Color.RESET)
        
        self.buttons = self._types[self.ctype]
        
        self.set_children(self.buttons)
        
        self.add_child(self.text)
        
    def set_text_color(self, color: str):
        self.text_color = color
        self.text.fg_color = color
    
    def set_text(self, text: str):
        self.text.set_text(text)
        
    def bind_yes(self, action: Callable[[], None]):
        if self.ctype == "OK" or self.ctype == "YES_NO" or self.ctype == "YES_NO_CANCEL":
            self.buttons[0].action = action
            self._screen.bind_key(Keys.NUM_1, lambda: self.process_action(action))
    
    def bind_no(self, action: Callable[[], None]):
        if self.ctype == "YES_NO" or self.ctype == "YES_NO_CANCEL":
            self.buttons[1].action = action
            self._screen.bind_key(Keys.NUM_2, lambda: self.process_action(action))
    
    def bind_cancel(self, action: Callable[[], None]):
        if self.ctype == "YES_NO_CANCEL":
            self.buttons[2].action = action
            self._screen.bind_key(Keys.NUM_3, lambda: self.process_action(action))
            
    def process_action(self, action: Callable[[], None]):
        if not self.active: return
        action()

        
        