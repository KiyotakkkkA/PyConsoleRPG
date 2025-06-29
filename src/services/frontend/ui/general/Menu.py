from .Text import Text
from typing import Callable
from src.services.frontend.core.Component import Component
from src.services.output import Color
from src.services.events import Keys
from typing import Tuple, List, Callable
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
        
class SeparatorItem:
    def __init__(self, filler: str, width: int, color: str = Color.RESET):
        """
        Инициализация компонента Разделителя
        
        Args:
            filler: Заполнитель
            width: Ширина
            color: Цвет
        """
        self.filler = filler
        self.width = width
        self.color = color
        self.text = Text(x=0,
                         y=0,
                         text=filler * width,
                         fg_color=color)
        
class Menu(Component):
    def __init__(self, x: int,
                 y: int,
                 paddings: Tuple[int, int, int, int] = (1, 10, 1, 1),
                 gap: int = 1,
                 inactive_menu_color: str = Color.RESET,
                 active_menu_color: str = Color.YELLOW,
                 control_keys: Tuple[int, int, int] = (Keys.UP, Keys.DOWN, Keys.ENTER),
                 alignment: int = Alignment.CENTER,
                 allow_sound: bool = False,
                 selection_sound: str | None = 'selection.mp3',
                 auto_resize: bool = False,
                 max_width: int = None):
        """
        Инициализация компонента Меню
        
        Args:
            x: Координата x
            y: Координата y
            paddings: Отступы (pt, pb, pr, pl)
            gap: Расстояние между пунктами меню
            inactive_menu_color: Цвет неактивного пункта меню
            active_menu_color: Цвет активного пункта меню
            control_keys: Ключи для навигации
            alignment: Выравнивание пунктов меню
            selection_sound: Звук при выборе
            auto_resize: Автоматическое перенос строк
            max_width: Максимальная ширина компонента
        """
        super().__init__(x, y, 0, 0, paddings, auto_resize, max_width)
        
        self.reactive('active_index', -1)
        self.reactive('items', [])
        self.reactive('keys_to_item_indexes', {})
        self.reactive('max_len_row', 0)
        
        self.reactive('gap', gap)
        self.reactive('inactive_menu_color', inactive_menu_color)
        self.reactive('active_menu_color', active_menu_color)
        self.reactive('control_keys', control_keys)
        self.reactive('alignment', alignment)
        self.reactive('selection_sound', selection_sound)
        
        self._events.append((self.control_keys[0], self.move_up))
        self._events.append((self.control_keys[1], self.move_down))
        self._events.append((self.control_keys[2], self.execute_action))
        
        self.set_allow_sound(allow_sound)
        
    def flush_selection(self):
        """Сброс выбора"""
        self.active_index = -1
        
    def set_selection(self, index: int):
        """Установка выбора"""
        if self.items:
            self.active_index = index % len(self.items)
        
    def execute_action(self):
        if not self.active:
            return
        
        if self.items and self.active_index >= 0:
            self.items[self.active_index].action()
        else:
            self.items[len(self.items) - abs(self.active_index)].action()
        
    def move_with_key(self, key: int):
        if not self.active:
            return
        
        if self.items and key in self.keys_to_item_indexes:
            self.active_index = self.keys_to_item_indexes[key]
            self.play_sound(self.selection_sound)
            self.execute_action()
        
    def move_up(self):
        if not self.active:
            return
        
        if self.items:
            self.active_index = (self.active_index - 1) % len(self.items)
            while isinstance(self.items[self.active_index], SeparatorItem):
                self.active_index = (self.active_index - 1) % len(self.items)
            
            self.play_sound(self.selection_sound)
            
    def move_down(self):
        if not self.active:
            return
        
        if self.items:
            self.active_index = (self.active_index + 1) % len(self.items)
            while isinstance(self.items[self.active_index], SeparatorItem):
                self.active_index = (self.active_index + 1) % len(self.items)
            
            self.play_sound(self.selection_sound)
            
    def add_item(self, text: tuple[str, str] | SeparatorItem, key: int, action: Callable[[], None]):
        """
        Добавление пункта меню
        
        Args:
            text: Текст, отображаемый в пункте меню Кортеж (Текст, Цвет текста)
            key: Клавиша, привязанная к пункту меню
            action: Действие, выполняемое при нажатии на пункт меню
        """
        
        if isinstance(text, SeparatorItem):
            text.text.x = self.x + self.paddings[3]
            text.text.y = self.y + self.paddings[0] + 1 + self.gap * len(self.items)
            text.text.set_text(text.filler * (self.width))
            self.items.append(text)
            return
        
        menu_item = MenuItem(
            text=Text(x=0,
                      y=0,
                      text=f"{text[0]} {'[' + KEYS_CODES_NAME[key.value] + ']' if key else ''}",
                      fg_color=text[1],
                      auto_resize=self.auto_resize,
                      max_width=self.max_width),
            key=key,
            action=action
        )
        
        self.width = max(menu_item.text.get_width(), self.calculate_width())
        if self.max_width:
            self.width = min(self.width, self.max_width)
        
        self.height = self.paddings[0] + self.gap * len(self.items) + self.paddings[2]
        
        element_x = self.x + self.paddings[3]
        
        if self.alignment == Alignment.LEFT:
            element_x = self.x + self.paddings[3]
        elif self.alignment == Alignment.RIGHT:
            element_x = self.x + self.width - self.paddings[1] - menu_item.text.get_width()
        elif self.alignment == Alignment.CENTER:
            element_x = self.x + (self.width // 2) - (menu_item.text.get_width() // 2)
        
        menu_item.text.x = element_x
        menu_item.text.y = self.y + self.paddings[0] + 1 + self.gap * len(self.items)
        
        self.items.append(menu_item)
        
        for item in self.items:
            if isinstance(item, SeparatorItem):
                continue            
            
            if self.alignment == Alignment.LEFT:
                item.text.x = self.x + self.paddings[3]
            elif self.alignment == Alignment.RIGHT:
                item.text.x = self.x + self.width - self.paddings[1] - item.text.get_width()
            elif self.alignment == Alignment.CENTER:
                item.text.x = self.x + (self.width // 2) - (item.text.get_width() // 2 + 1)
        
        self.keys_to_item_indexes[key] = len(self.items) - 1
        if key:
            self._events.append((key, lambda: self.move_with_key(key)))
        
    def add_items(self, items: list[(tuple[str, tuple[str, str], int, Callable[[], None]]) | SeparatorItem]):
        """
        Добавление нескольких пунктов меню
        
        Args:
            items: Список кортежей (Название пункта меню, Текст, Цвет текста, Клавиша, Действие)
        """
        for item in items:
            self.add_item(*item)
            
    def set_items(self, items: list[(tuple[str, tuple[str, str], int, Callable[[], None]]) | SeparatorItem]):
        """
        Установка нескольких пунктов меню
        
        Args:
            items: Список кортежей (Название пункта меню, Текст, Цвет текста, Клавиша, Действие)
        """
        self.items = []
        self.keys_to_item_indexes = {}
        self.add_items(items)
            
    def calculate_width(self):
        return max([item.text.get_width() for item in self.items if isinstance(item, MenuItem)]) if self.items else 0
            
    def draw(self, screen: 'Screen') -> None:
        for i, item in enumerate(self.items):
            if self.active_index == i:
                item.text.fg_color = self.active_menu_color
            else:
                item.text.fg_color = self.inactive_menu_color
            item.text.draw(screen)
