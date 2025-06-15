from src.services.frontend.ui.containers import Panel
from src.services.frontend.core.Component import Component
from src.services.output import Color
from src.services.events import Keys
from src.config import KEYS_CODES_NAME
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen


class TabItem:
    def __init__(self, id: int, name: str, panel: Panel, key: int):
        """
        Инициализация компонента Таб
        
        Args:
            id: ID таба
            name: Название таба
            panel: Панель, связанная с табом
            key: Клавиша, привязанная к табу
        """
        self.id = id
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
                 disabled_tab_color: str = Color.BRIGHT_BLACK,
                 control_keys: Tuple[int, int] = (Keys.LEFT, Keys.RIGHT),
                 border_color: str = Color.RESET):
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
            disabled_tab_color: Цвет выключенного таба
            control_keys: Ключи для навигации
            border_color: Цвет рамки
        """
        super().__init__(x, y, width, height, paddings)
        
        self.reactive('active_index', 0)
        self.reactive('tabs', [])
        self.reactive('tabs_ids', {})
        self.reactive('active_tabs', {})
        self.reactive('keys_to_tab_indexes', {})
        
        self.reactive('inactive_tab_color', inactive_tab_color)
        self.reactive('active_tab_color', active_tab_color)
        self.reactive('disabled_tab_color', disabled_tab_color)
        self.reactive('border_color', border_color)
        
        self.reactive('control_keys', control_keys)
        
        if self.control_keys[0]:
            self._events.append((self.control_keys[0], self.move_left))
        if self.control_keys[1]:
            self._events.append((self.control_keys[1], self.move_right))
            
    def _rebuild_active_links(self):
        active_indexes = [i for i, state in self.active_tabs.items() if state['active']]
        for idx, tab_index in enumerate(active_indexes):
            prev_idx = active_indexes[idx - 1] if idx > 0 else active_indexes[-1]
            next_idx = active_indexes[idx + 1] if idx < len(active_indexes) - 1 else active_indexes[0]
            self.active_tabs[tab_index]['prev'] = prev_idx
            self.active_tabs[tab_index]['next'] = next_idx
        
    def move_left(self):
        if self.active_index in self.active_tabs:
            self.active_index = self.active_tabs[self.active_index]['prev']
        
    def move_right(self):
        if self.active_index in self.active_tabs:
            self.active_index = self.active_tabs[self.active_index]['next']
        
    def move_with_key(self, key: int):
        if key in self.keys_to_tab_indexes:
            index = self.keys_to_tab_indexes[key]
            if self.active_tabs[index]['active']:
                self.active_index = index
        
    def calculate(self):
        self._calculate_self_size()
        
    def disable_tab(self, index: int):
        if index in self.active_tabs:
            self.active_tabs[index]['active'] = False
            self._rebuild_active_links()
        
    def enable_tab(self, index: int):
        if index in self.active_tabs:
            self.active_tabs[index]['active'] = True
            self._rebuild_active_links()
        
    def add_tab(self, id: int, name: str, panel: Panel, key: int):
        tab_item = TabItem(
            id=id,
            name=name,
            panel=panel,
            key=key
        )
        self.tabs.append(tab_item)
        
        length = len(self.tabs)
        
        self.active_tabs[length - 1] = {
            'index': length - 1,
            'active': True,
            'prev': None if length == 1 else length - 2,
            'next': 0
        }
        
        if length > 1:
            self.active_tabs[length - 2]['next'] = length - 1
        self.active_tabs[0]['prev'] = length - 1
        
        self.keys_to_tab_indexes[key] = length - 1
        self.tabs_ids[id] = tab_item
        tab_item.panel.x = self.x + self.paddings[3]
        tab_item.panel.y = self.y + self.paddings[0] + 1
        tab_item.panel.width = self.width - self.paddings[2] - self.paddings[3]
        tab_item.panel.height = self.height - self.paddings[1] - self.paddings[2] - 1
        tab_item.panel.border_color = Color.BLACK
        
        if key:
            self._events.append((key, lambda: self.move_with_key(key)))
        
    def add_tabs(self, tabs: List[Tuple[int, str, Panel, int]]):
        for tab in tabs:
            self.add_tab(tab[0], tab[1], tab[2], tab[3])
            
    def get_tab_by_id(self, id: int):
        return self.tabs_ids[id]
    
    def get_selection_of_tab_by_id(self, id: int):
        return self.tabs[self.active_index].id == id
        
    def draw(self, screen: 'Screen') -> None:
        self.calculate()
        gap = self.width // (len(self.tabs) + 1)
        
        screen.draw_text(self.x + self.paddings[3], self.y + self.paddings[0], '─' * (self.width - self.paddings[2] - self.paddings[3]), self.border_color, Color.RESET)
        
        for i, tab in enumerate(self.tabs):
            color = self.disabled_tab_color if not self.active_tabs[i]['active'] else self.active_tab_color if self.active_index == i else self.inactive_tab_color
            screen.draw_text(self.x + self.paddings[3] + gap * (i + 1), self.y + self.paddings[0], f"{tab.name} [{KEYS_CODES_NAME[tab.key.value]}]", 
                             color, Color.RESET)
        
        active_tab = self.tabs[self.active_index]
        active_tab.panel.draw(screen)
