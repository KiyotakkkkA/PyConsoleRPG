from src.services.frontend.core import Component
from src.services.output import Color, Symbols
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.events import EventListener
from typing import TYPE_CHECKING, List, Tuple, Callable, override

if TYPE_CHECKING:
    from src.services.frontend.core import Screen

class Table(Component):
    def __init__(self, x,
                 y,
                 width,
                 headers: list[str],
                 title_text_colors: list[tuple[str, str]],
                 title_alignment: Alignment = Alignment.LEFT,
                 row_alignment: Alignment = Alignment.LEFT,
                 selected_row_color: str = Color.BG_BRIGHT_YELLOW,
                 max_rows: int = 5,
                 add_numeration: bool = True,
                 numeration_color: tuple[str, str] = (Color.YELLOW, Color.RESET),
                 overflowing_symbol: str = '...',
                 border_color: tuple[str, str] = Color.BRIGHT_BLACK,):
        """
        Инициализация компонента Таблица
        
        Args:
            x: Координата x
            y: Координата y
            width: Ширина
            headers: Список заголовков
            title_text_colors: Список цветов заголовков
            title_alignment: Выравнивание заголовков
            row_alignment: Выравнивание строк
            selected_row_color: Цвет выделенной строки
            max_rows: Максимальное одновременное количество строк
            add_numeration: Добавление нумерации строк
            overflowing_symbol: Символ, который будет использоваться для обозначения переполнения
            border_color: Цвет границы
        """
        super().__init__(x, y, width, 1, (0, 0, 0, 0))
        
        self.headers = headers
        self.title_alignment = title_alignment
        self.row_alignment = row_alignment
        self.add_numeration = add_numeration
        
        self.reactive('title_text_colors', title_text_colors)
        
        if self.add_numeration:
            self.headers.insert(0, "N")
            self.title_text_colors.insert(0, numeration_color)
            
        self.id = f"table_{hash(self)}"
        
        self.reactive('headers_data', {})
        self.reactive('rows_colors', [])
        self.reactive('rows', [])
        self.reactive('columns', [])
        self.reactive('rows_ids', {})
        self.reactive('selected_row_color', selected_row_color)
        self.reactive('numeration_color', numeration_color)
        self.reactive('overflowing_symbol', overflowing_symbol)
        self.reactive('border_color', border_color)
        self.reactive('total_rows_count', 0)
        self.reactive('actions', {})
        
        self.reactive('current_selected_row', 0)
        self.reactive('max_rows', max_rows)
        self.reactive('start_row', 0)
        self.reactive('end_row', 0)
        
        self.reactive('rules', {
            'panel_criteria': False,
            'tab_criteria': False
        })
        
        self._events.append((Keys.UP, self.move_up))
        self._events.append((Keys.DOWN, self.move_down))
        self._events.append((Keys.ENTER, self.process_action))
        
        self.height = 3
        
        self.count_headers_size()
        
    @override
    def set_active(self, active: bool):
        super().set_active(active)
        
        if active:
            self.set_selected_row(self.current_selected_row)
    
    def connect_to_tab(self, tab: 'Tab', tab_id: str, data: dict = None):
        """
        Подключение компонента МультиПанель к компоненту Таб
        Панель будет активна только если активна указанная вкладка
        
        Args:
            tab: Компонент Таб
            tab_id: ID вкладки
        """
        EventListener().on_event("tab_changed", lambda data: self.tab_config(tab, tab_id, data))
    
    def connect_to_panel(self, panel: 'Panel', data: dict = None):
        """
        Подключение компонента МультиПанель к компоненту Панель
        Панель будет активна только если активна указанная панель
        
        Args:
            panel: Компонент Панель
        """
        EventListener().on_event("panel_changed", lambda data: self.panel_config(panel, data))
        
    def tab_config(self, tab: 'Tab', tab_id: str, data: dict = None):
        if tab.get_active_tab().id == tab_id:
            self.rules['tab_criteria'] = True
        else:
            self.rules['tab_criteria'] = False
            
        array = [
            self.rules['tab_criteria'],
            self.rules['panel_criteria']
        ]
        
        self.set_active(all(array))
            
    def panel_config(self, panel: 'Panel', data: dict = None):
        if panel.selected:
            self.rules['panel_criteria'] = True
        else:
            self.rules['panel_criteria'] = False
            
        array = [
            self.rules['tab_criteria'],
            self.rules['panel_criteria']
        ]
        
        self.set_active(all(array))
        
    def set_selected_row(self, row: int):
        self.current_selected_row = max(0, min(row, len(self.rows) - 1))
        EventListener().emit_event("{}_row_selected".format(self.id), self.get_selected_row_data())
        
    def get_selected_row_data(self):
        if not self.active or len(self.rows) == 0: return None
        _arr = self.rows[self.current_selected_row][:]
        _arr.append(self.rows_ids[self.current_selected_row])
        return _arr
        
    def process_action(self):
        if not self.active or len(self.rows) == 0: return
        if self.current_selected_row in self.actions:
            if self.actions[self.current_selected_row]:
                self.actions[self.current_selected_row]()
        
    def move_up(self):
        if not self.active or len(self.rows) == 0: return
        self.set_selected_row(self.current_selected_row - 1)
        if self.current_selected_row < self.start_row:
            self.start_row -= 1
            self.end_row -= 1
        
    def move_down(self):
        if not self.active: return
        self.set_selected_row(self.current_selected_row + 1)
        if self.current_selected_row >= self.end_row:
            self.start_row += 1
            self.end_row += 1
            
    def truncate_text(self, text: str, max_width: int) -> str:
        """Обрезает текст с добавлением символа переполнения, если он не помещается"""
        max_text_width = max_width - 3 - len(self.overflowing_symbol)
        if len(text) > max_text_width:
            return text[:max_text_width] + self.overflowing_symbol
        return text
            
    def calculate_aligned_x(self, start_x: int, width: int, text_length: int, alignment: Alignment) -> int:
        """Вычисляет координату X с учетом выравнивания"""
        if alignment == Alignment.LEFT:
            return start_x + 1
        elif alignment == Alignment.RIGHT:
            return start_x + width - text_length - 1
        elif alignment == Alignment.CENTER:
            return start_x + (width // 2) - (text_length // 2)
        
    def count_headers_size(self):
        column_index = 0
        total_sum = sum(len(header) + 3 for header in self.headers)
        self.width = max(total_sum + 1, self.width)
        current_x = self.x
        
        for header in self.headers:
            relative_width = (len(header) + 3) / total_sum
            true_width = int(relative_width * self.width)
            text_x = self.calculate_aligned_x(current_x, true_width, len(header) + 2, self.title_alignment)
            
            self.headers_data[column_index] = {
                'relative_width': relative_width,
                'true_width': true_width,
                'text_x': text_x,
                'color': self.title_text_colors[column_index],
                'x': current_x,
                'y': self.y + 1
            }
            current_x += true_width
            column_index += 1
            
    def add_row(self, key, row: list[str], colors: list[tuple[str, str]] = [], action: Callable = None):
        if self.add_numeration:
            row.insert(0, str(len(self.rows) + 1))
        if not colors:
            colors = [(Color.WHITE, Color.RESET) for _ in range(len(row))]
        self.rows.append(row)
        self.rows_colors.append(colors)
        self.rows_ids[len(self.rows) - 1] = key
        self.end_row = min(self.max_rows, len(self.rows))
        self.total_rows_count = len(self.rows)
        self.actions[len(self.rows) - 1] = action
        
        self.height += 2
        
    def add_rows(self, keys: list[str], rows: list[list[str]] = [], colors: list[list[tuple[str, str]]] = [], actions: list[Callable] = []):
        for i in range(len(rows)):
            self.add_row(keys[i], rows[i], colors[i], actions[i] if i < len(actions) else None)
        
    def set_rows(self, keys: list[str], rows: list[list[str]], colors: list[list[tuple[str, str]]] = [], actions: list[Callable] = []):
        self.rows = []
        self.rows_colors = []
        self.actions = {}
        self.rows_ids = {}
        self.height = 3
        
        self.add_rows(keys, rows, colors, actions)
        
    def draw(self, screen: 'Screen'):
        screen.draw_text(self.x, self.y, Symbols.BORDERS.TOP_LEFT + Symbols.BORDERS.TOP * (self.width - 1) + Symbols.BORDERS.TOP_RIGHT, self.border_color, Color.RESET)
        for header in range(len(self.headers)):
            screen.draw_text(self.headers_data[header]['text_x'], self.headers_data[header]['y'], f" " + self.headers[header] + " ", self.headers_data[header]['color'][0], self.headers_data[header]['color'][1])
            screen.draw_text(self.headers_data[header]['x'], self.headers_data[header]['y'], Symbols.BORDERS.RIGHT, self.border_color, Color.RESET)
        screen.draw_text(self.x + self.width, self.y + 3 - 2, Symbols.BORDERS.RIGHT, self.border_color, Color.RESET)
        screen.draw_text(self.x, self.y + 3 - 1, Symbols.BORDERS.BOTTOM_LEFT + Symbols.BORDERS.BOTTOM * (self.width - 1) + Symbols.BORDERS.BOTTOM_RIGHT, self.border_color, Color.RESET)
        
        row_y = self.y + 3
        if self.total_rows_count > self.max_rows:
            screen.draw_text(self.x, row_y, Symbols.BORDERS.LEFT + ' ' * (self.width - 1) + Symbols.BORDERS.RIGHT, self.border_color, Color.RESET)
            screen.draw_text(self.x + 2, row_y, f"{self.start_row + 1} - {self.end_row} из {self.total_rows_count}", Color.BRIGHT_GREEN, Color.RESET)
            screen.draw_text(self.x, row_y + 1, Symbols.BORDERS.BOTTOM_LEFT + Symbols.BORDERS.BOTTOM * (self.width - 1) + Symbols.BORDERS.BOTTOM_RIGHT, self.border_color, Color.RESET)
            row_y += 2
        
        if not self.rows: return
        
        for i in range(self.start_row, self.end_row):            
            for j in range(len(self.rows[i])):
                screen.draw_text(self.headers_data[j]['x'], row_y, Symbols.BORDERS.LEFT, self.border_color, Color.RESET)
                
                text_x = self.calculate_aligned_x(self.headers_data[j]['x'], self.headers_data[j]['true_width'], len(self.rows[i][j]), self.row_alignment)
                
                fgcolor = self.selected_row_color if i == self.current_selected_row and self.active else self.rows_colors[i][j][0]
                bgcolor = self.selected_row_color if i == self.current_selected_row and self.active else self.rows_colors[i][j][1]
                
                text = self.truncate_text(self.rows[i][j], self.headers_data[j]['true_width'])
                
                screen.draw_text(text_x, row_y, f" {text} ", fgcolor, bgcolor)
            screen.draw_text(self.x + self.width, row_y, Symbols.BORDERS.RIGHT, self.border_color, Color.RESET)
            screen.draw_text(self.x, row_y + 1, Symbols.BORDERS.BOTTOM_LEFT + Symbols.BORDERS.BOTTOM * (self.width - 1) + Symbols.BORDERS.BOTTOM_RIGHT, self.border_color, Color.RESET)
            row_y += 2
            
            