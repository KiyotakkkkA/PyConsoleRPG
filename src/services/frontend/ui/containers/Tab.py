from src.services.frontend.ui.containers import Panel
from src.services.frontend.core.Component import Component
from src.services.output import Color
from src.services.events import Keys
from src.config import KEYS_CODES_NAME
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen


class TabItem:
    def __init__(self, name: str, panel: Panel, key: int):
        """
        Инициализация компонента Таб
        
        Args:
            name: Название таба
            panel: Панель, связанная с табом
            key: Клавиша, привязанная к табу
        """
        self.name = name
        self.panel = panel
        self.key = key

class Tab(Component):
    def __init__(self, x: int,
                 y: int,
                 width: int,
                 height: int,
                 paddings: Tuple[int, int, int, int] = (1, 1, 1, 1),
                 inactive_tab_color: str = Color.RESET,
                 active_tab_color: str = Color.WHITE,
                 control_keys: Tuple[int, int] = (Keys.LEFT, Keys.RIGHT)):
        """
        Инициализация компонента Таб
        
        Args:
            x: Координата x
            y: Координата y
            width: Ширина
            height: Высота
            paddings: Отступы
            inactive_tab_color: Цвет неактивного таба
            active_tab_color: Цвет активного таба
            control_keys: Ключи для навигации
        """
        super().__init__(x, y, width, height, paddings)
        
        self.reactive('active_index', 0)
        self.reactive('tabs', [])
        self.reactive('keys_to_tab_indexes', {})
        
        self.reactive('inactive_tab_color', inactive_tab_color)
        self.reactive('active_tab_color', active_tab_color)
        
        self.reactive('control_keys', control_keys)
        
        self.bind_key(self.control_keys[0], self.move_left)
        self.bind_key(self.control_keys[1], self.move_right)
        
    def move_left(self):
        self.active_index = (self.active_index - 1) % len(self.tabs)
        
    def move_right(self):
        self.active_index = (self.active_index + 1) % len(self.tabs)
        
    def move_with_key(self, key: int):
        if key in self.keys_to_tab_indexes:
            self.active_index = self.keys_to_tab_indexes[key]
        
    def calculate(self):
        self._calculate_self_size()
        
    def add_tab(self, name: str, panel: Panel, key: int):
        tab_item = TabItem(
            name=name,
            panel=panel,
            key=key
        )
        self.tabs.append(tab_item)
        self.keys_to_tab_indexes[key] = len(self.tabs) - 1
        tab_item.panel.x = self.x + self.paddings[3]
        tab_item.panel.y = self.y + self.paddings[0] + 1
        tab_item.panel.width = self.width - self.paddings[2] - self.paddings[3]
        tab_item.panel.height = self.height - self.paddings[1] - self.paddings[2] - 1
        tab_item.panel.border_color = Color.BLACK
        
        self.bind_key(key, lambda: self.move_with_key(key))
        
    def add_tabs(self, tabs: List[Tuple[str, Panel, int]]):
        for tab in tabs:
            self.add_tab(tab[0], tab[1], tab[2])
        
    def draw(self, screen: 'Screen') -> None:
        self.calculate()
        gap = self.width // (len(self.tabs) + 1)
        
        screen.draw_text(self.x + self.paddings[3], self.y + self.paddings[0], '─' * (self.width - self.paddings[2] - self.paddings[3]), Color.WHITE, Color.RESET)
        
        for i, tab in enumerate(self.tabs):
            screen.draw_text(self.x + self.paddings[3] + gap * (i + 1), self.y + self.paddings[0], f"{tab.name} [{KEYS_CODES_NAME[tab.key.value]}]", 
                             self.active_tab_color if self.active_index == i else self.inactive_tab_color, Color.RESET)
        
        active_tab = self.tabs[self.active_index]
        active_tab.panel.draw(screen)
