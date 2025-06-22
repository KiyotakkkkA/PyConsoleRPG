from src.services.frontend.core import Component, Alignment
from src.services.output import Color
from src.services.events import Keys, EventListener
from src.services.frontend.ui.containers import Tab
from src.config.Dictionary import KEYS_CODES_NAME
from ..input import Selector
from ..containers import Panel


class PanelItem:
    def __init__(self, key: str, name: str, panel: 'Panel'):
        self.key = key
        self.name = name
        self.panel = panel

class MultiPanel(Component):
    def __init__(self, 
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 key_to_activate: Keys,
                 label: str = "Вкладка",
                 label_color: str = Color.RESET,
                 label_selected_color: str = Color.BRIGHT_YELLOW,
                 label_active_color: str = Color.BG_BRIGHT_GREEN,
                 value_color: str = Color.RESET,
                 value_selected_color: str = Color.RESET,
                 value_active_color: str = Color.YELLOW):
        super().__init__(x, y, width, height)
        
        self.key_to_activate = key_to_activate
        
        self.id = f"multi_panel_{hash(self)}"
        
        self.reactive('label', label)
        self.reactive('label_color', label_color)
        self.reactive('label_selected_color', label_selected_color)
        self.reactive('label_active_color', label_active_color)
        self.reactive('value_color', value_color)
        self.reactive('value_selected_color', value_selected_color)
        self.reactive('value_active_color', value_active_color)
        
        self.reactive('panels', [])
        self.reactive('options', [])
        self.reactive('panels_ids', {})
        
        self.current_panel = None
        
        self.setup_selector()
        
        EventListener().on_event(f"{self.id}_selector_event", self.event_selector)
    
    """
    Инициализация компонента МультиПанель
    
    Args:
        x: Координата x компонента
        y: Координата y компонента
        width: Ширина компонента
        height: Высота компонента
        key_to_activate: Клавиша для активации
        label: Текст метки
        label_color: Цвет метки
        label_selected_color: Цвет метки при выборе
        label_active_color: Цвет метки при активности
        value_color: Цвет значения
        value_selected_color: Цвет значения при выборе
        value_active_color: Цвет значения при активности
    """
    
    def connect_to_tab(self, tab: 'Tab', tab_id: str):
        """
        Подключение компонента МультиПанель к компоненту Таб
        Панель будет активна только если активна указанная вкладка
        
        Args:
            tab: Компонент Таб
            tab_id: ID вкладки
        """
        
        EventListener().on_event("tab_changed", lambda data: self.tab_config(tab, tab_id, data['id']))
    
    def is_selector_active(self):
        """
        Проверка активности селектора
        
        Returns:
            Состояние активности селектора
        """
        return self.selector.active
    
    def get_is_panel_active_with_id(self, panel_id: str) -> bool:
        """
        Проверка активности панели по ID
        
        Args:
            panel_id: ID панели
        
        Returns:
            Состояние активности панели
        """
        return self.current_panel == panel_id
    
    def get_panel_by_id(self, panel_id: str) -> 'Panel':
        """
        Получение панели по ID
        
        Args:
            panel_id: ID панели
        
        Returns:
            Панель
        """
        return self.panels_ids[panel_id]
    
    def tab_config(self, tab: 'Tab', tab_id: str, data: dict | None):
        if tab.get_active_tab().id == tab_id:
            self.set_active(True)
        else:
            self.set_active(False)
    
    def choose_selector(self):
        if not self.active: return
        if self.selector.active: return
        self.selector.set_selected(True)
        
    def event_selector(self, data):
        self.current_panel = data['value']
        
    def setup_options(self):
        self.options = []
        for panel in self.panels:
            self.options.append((panel.key, panel.name))
            
    def add_panels(self, panels: list[tuple[str, str, 'Panel']], styling: tuple['Alignment', str, str] = (Alignment.CENTER, Color.BRIGHT_BLACK, Color.BRIGHT_YELLOW)):
        """
        Добавление вкладок в компонент МультиПанель
        
        Args:
            panels: Список кортежей, содержащих ключ, название и объект Panel
            styling: Кортеж, содержащий выравнивание, цвет границ и цвет границ при выборе
        """
        for panel in panels:
            if not self.current_panel:
                self.current_panel = panel[0]
            
            panel[2].x = self.x
            panel[2].y = self.y + 1
            panel[2].width = self.width
            panel[2].height = self.height
            panel[2].title_alignment = styling[0]
            panel[2].border_color = styling[1]
            panel[2].border_color_selected = styling[2]
            
            self.panels.append(PanelItem(panel[0], panel[1], panel[2]))
            self.options.append((panel[0], panel[1]))
            self.panels_ids[panel[0]] = panel[2]
            
    def setup_selector(self):
        self.selector = Selector(
            x=self.x,
            y=self.y,
            enter_data_event_name=f"{self.id}_selector_event",
            selection_type="prev-current-next",
            options=self.options,
            label_title=f"{self.label} [{KEYS_CODES_NAME[self.key_to_activate.value]}]:",
            label_color=self.label_color,
            label_selected_color=self.label_selected_color,
            label_active_color=self.label_active_color,
            value_color=self.value_color,
            value_selected_color=self.value_selected_color,
            value_active_color=self.value_active_color)
        
        self.selector.current_index = 0
        
        self.add_child(self.selector)
        
        self._events.append((self.key_to_activate, self.choose_selector))
    
    def draw(self, screen: 'Screen'):
        super().draw(screen)
        
        if self.current_panel:
            self.panels_ids[self.current_panel].draw(screen)