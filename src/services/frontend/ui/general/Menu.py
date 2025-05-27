from .Text import Text
from typing import Callable
from src.services.frontend.core.Component import Component
from src.services.output import Color
from src.services.events import Keys
from typing import Tuple
from src.services.frontend.core import Alignment
from src.config import KEYS_CODES_NAME

class MenuItem:
    def __init__(self, text: Text, key: int, action: Callable[[], None]):
        """
        Инициализация компонента Пункта Меню
        
        Args:
            text: Текст, отображаемый в пункте меню
            key: Клавиша, привязанная к пункту меню
            action: Действие, выполняемое при нажатии на пункт меню
        """
        self.text = text
        self.key = key
        self.action = action
        
class Menu(Component):
    def __init__(self, x: int,
                 y: int,
                 height: int,
                 paddings: Tuple[int, int, int, int] = (1, 1, 1, 1),
                 gap: int = 1,
                 inactive_menu_color: str = Color.RESET,
                 active_menu_color: str = Color.YELLOW,
                 control_keys: Tuple[int, int, int] = (Keys.UP, Keys.DOWN, Keys.ENTER),
                 alignment: int = Alignment.CENTER):
        """
        Инициализация компонента Меню
        
        Args:
            x: Координата x
            y: Координата y
            width: Ширина
            height: Высота
            paddings: Отступы
            gap: Расстояние между пунктами меню
            inactive_menu_color: Цвет неактивного пункта меню
            active_menu_color: Цвет активного пункта меню
            control_keys: Ключи для навигации
            alignment: Выравнивание пунктов меню
        """
        super().__init__(x, y, 0, height, paddings)
        
        self.reactive('active_index', 0)
        self.reactive('items', [])
        self.reactive('keys_to_item_indexes', {})
        
        self.reactive('gap', gap)
        self.reactive('inactive_menu_color', inactive_menu_color)
        self.reactive('active_menu_color', active_menu_color)
        self.reactive('control_keys', control_keys)
        self.reactive('alignment', alignment)
        
        self.bind_key(self.control_keys[0], self.move_up)
        self.bind_key(self.control_keys[1], self.move_down)
        self.bind_key(self.control_keys[2], self.execute_action)
        
    def execute_action(self):
        if self.active_index >= 0:
            self.items[self.active_index].action()
        else:
            self.items[len(self.items) - abs(self.active_index)].action()
        
    def move_with_key(self, key: int):
        if key in self.keys_to_item_indexes:
            self.active_index = self.keys_to_item_indexes[key]
            self.execute_action()
        
    def move_up(self):
        self.active_index = (self.active_index - 1) % len(self.items)
            
    def move_down(self):
        self.active_index = (self.active_index + 1) % len(self.items)
            
    def add_item(self, text: tuple[str, str], key: int, action: Callable[[], None]):
        """
        Добавление пункта меню
        
        Args:
            text: Текст, отображаемый в пункте меню Кортеж (Текст, Цвет текста)
            key: Клавиша, привязанная к пункту меню
            action: Действие, выполняемое при нажатии на пункт меню
        """
        
        self.width = max(len(text[0]), self.calculate_width())
        
        element_x = self.x + self.paddings[3]
        
        if self.alignment == Alignment.LEFT:
            element_x = self.x + self.paddings[3]
        elif self.alignment == Alignment.RIGHT:
            element_x = self.x + self.width - self.paddings[1] - len(text[0])
        elif self.alignment == Alignment.CENTER:
            element_x = self.x + (self.width // 2) - (len(text[0]) // 2)
        
        menu_item = MenuItem(
            text=Text(x=element_x,
                      y=self.y + self.paddings[0] + self.gap * len(self.items),
                      text=f"{text[0]} [{KEYS_CODES_NAME[key.value]}]",
                      fg_color=text[1]),
            key=key,
            action=action
        )
        self.items.append(menu_item)
        
        for item in self.items:
            if self.alignment == Alignment.LEFT:
                item.text.x = self.x + self.paddings[3]
            elif self.alignment == Alignment.RIGHT:
                item.text.x = self.x + self.width - self.paddings[1] - len(item.text.text)
            elif self.alignment == Alignment.CENTER:
                item.text.x = self.x + (self.width // 2) - (len(item.text.text) // 2 + 1)
        
        self.keys_to_item_indexes[key] = len(self.items) - 1
        self.bind_key(key, lambda: self.move_with_key(key))
        
    def add_items(self, items: list[tuple[str, tuple[str, str], int, Callable[[], None]]]):
        """
        Добавление нескольких пунктов меню
        
        Args:
            items: Список кортежей (Название пункта меню, Текст, Цвет текста, Клавиша, Действие)
        """
        for item in items:
            self.add_item(*item)
            
    def calculate_width(self):
        return max([len(item.text.text) for item in self.items]) if self.items else 0
            
    def calculate(self):
        self._calculate_self_size()
            
    def draw(self, screen: 'Screen') -> None:
        self.calculate()
        for item in self.items:
            if self.active_index == self.keys_to_item_indexes[item.key]:
                item.text.fg_color = self.active_menu_color
            else:
                item.text.fg_color = self.inactive_menu_color
            item.text.draw(screen)
