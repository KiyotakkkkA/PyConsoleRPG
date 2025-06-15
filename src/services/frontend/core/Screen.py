from typing import List, Dict, Callable, Set, Tuple, TYPE_CHECKING
from src.services.output import Color
from src.services.output.WinConsole import WinConsole
from src.services.events import EventListener
from src.services.events.KeyListener import KeyListener, Keys
from .ScreenPixel import ScreenPixel
from .Component import Component

if TYPE_CHECKING:
    from src.services.frontend.ui.containers.Tab import Tab


def hash_screen_pixel(char: str, fg_color: str, bg_color: str) -> int:
    return hash((char, fg_color, bg_color))

class Screen(EventListener):
    """
    Класс, представляющий экран
    """
    
    _instances = {}
    
    def __init__(self):
        super().__init__()
        self.win_console = WinConsole()
        self.width = self.win_console.width
        self.height = self.win_console.height
        
        self.front_buffer: List[List[ScreenPixel]] = [[ScreenPixel() for _ in range(self.width)] for _ in range(self.height)]
        self.back_buffer: List[List[ScreenPixel]] = [[ScreenPixel() for _ in range(self.width)] for _ in range(self.height)]
        
        self.children: List[Component] = []
        self.is_active = True
        self.performance_vision = False
        self.performance_checker = None
        
        self.key_handlers: Dict[Keys, Set[Callable]] = {}
        self.components_events: List[Tuple[Keys, Callable]] = []
        
        self.init()
        
        self.collect_bind_keys(self)
        
        self._instances[self.__class__.__name__] = self
        
        KeyListener().register_screen(self)
        
    def init(self):
        pass
    
    def on_event(self, event_name: str, callback: Callable):
        super().on_event(event_name, callback)
        
    def emit_event(self, event_name: str, data: dict | None):
        super().emit_event(event_name, data)
    
    @classmethod
    def get_instance(cls):
        """
        Получение экземпляра экрана
        
        Returns:
            Экземпляр экрана
        """
        return cls._instances.get(cls.__name__)
        
    def enable_performance_monitor(self, enable=True):
        """
        Включение или выключение отображения монитора производительности
        
        Args:
            enable: True для включения, False для выключения
        """
        from src.services.frontend.ui.utils import PerformanceChecker
        
        self.performance_vision = enable
        
        if enable and self.performance_checker is None:
            self.performance_checker = PerformanceChecker(0, 0, 30, 5)

    def update(self):
        pass
    
    def quit(self):
        self.is_active = False
        
    def on_key_press(self, key: Keys) -> None:
        """
        Обработка нажатия клавиши
        
        Args:
            key: Нажатая клавиша из перечисления Keys
        """
        self.emit_event('key_press', {'key': key})
        
        if key in self.key_handlers:
            for handler in self.key_handlers[key]:
                handler()
                
        for child in self.children:
            if hasattr(child, 'on_key_press') and callable(child.on_key_press):
                child.on_key_press(key)
    
    def bind_key(self, key: Keys, handler: Callable) -> None:
        """
        Привязка обработчика к нажатию клавиши
        
        Args:
            key: Клавиша из перечисления Keys
            handler: Функция-обработчик
        """
        if key not in self.key_handlers:
            self.key_handlers[key] = set()
        self.key_handlers[key].add(handler)
        
    def collect_bind_keys(self, Object: 'Screen | Component | Tab'):
        from src.services.frontend.ui.containers import Panel, Tab
        
        for child in Object.children:
            if len(child._events) > 0:
                self.components_events.extend(child._events)
                
            if isinstance(child, Panel):
                self.collect_bind_keys(child)
            if isinstance(child, Tab):
                for tab in child.tabs:
                    self.collect_bind_keys(tab.panel)
            
        for event in self.components_events:
            self.bind_key(event[0], event[1])
        
    def unbind_key(self, key: Keys, handler: Callable) -> None:
        """
        Отвязка обработчика от нажатия клавиши
        
        Args:
            key: Клавиша из перечисления Keys
            handler: Функция-обработчик
        """
        if key in self.key_handlers and handler in self.key_handlers[key]:
            self.key_handlers[key].remove(handler)
        
    def add_child(self, child: Component) -> None:
        child._screen = self
        self.children.append(child)
        
    def unbind_child(self, child: Component) -> None:
        if child in self.children:
            self.children.remove(child)
    
    def clear_buffer(self, buffer: List[List[ScreenPixel]], char: str = " ", fg_color: str = Color.WHITE, bg_color: str = Color.RESET) -> None:
        """Очистка буфера и установка значений по умолчанию"""
        for y in range(self.height):
            for x in range(self.width):
                buffer[y][x].char = char
                buffer[y][x].fg_color = fg_color
                buffer[y][x].bg_color = bg_color
    
    def set_pixel(self, x: int, y: int, char: str, fg_color: str = Color.WHITE, bg_color: str = Color.RESET) -> None:
        """Установка пикселя в back_buffer"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.back_buffer[y][x].char = char
            self.back_buffer[y][x].fg_color = fg_color
            self.back_buffer[y][x].bg_color = bg_color
    
    def draw_rectangle(self, x: int, y: int, width: int, height: int, char: str = "█", fg_color: str = Color.WHITE, bg_color: str = Color.RESET) -> None:
        """Отрисовка прямоугольника в back_buffer"""
        for cy in range(max(0, y), min(self.height, y + height)):
            for cx in range(max(0, x), min(self.width, x + width)):
                self.set_pixel(cx, cy, char, fg_color, bg_color)
    
    def draw_text(self, x: int, y: int, text: str, fg_color: str = Color.WHITE, bg_color: str = Color.RESET) -> None:
        """Отрисовка текста в back_buffer"""
        # Проверяем, содержит ли текст специальные иконки
        if not text:
            return
        
        # Используем простой вывод, символ за символом, каждый символ в своей ячейке
        cursor_pos = 0
        for char in text:
            if x + cursor_pos < self.width:
                self.set_pixel(x + cursor_pos, y, char, fg_color, bg_color)
                cursor_pos += 1
    
    def swap_buffers(self) -> None:
        """Обмен буферов и отрисовка front_buffer"""
        for y in range(self.height):
            for x in range(self.width):
                self.front_buffer[y][x].char = self.back_buffer[y][x].char
                self.front_buffer[y][x].fg_color = self.back_buffer[y][x].fg_color
                self.front_buffer[y][x].bg_color = self.back_buffer[y][x].bg_color
    
    def render(self) -> None:
        """Отрисовка front_buffer на экран с использованием оптимизированного метода WinConsole"""
        self.win_console.set_cursor_position(0, 0)
        self.win_console.set_cursor_visibility(False)
        
        self.win_console.write_output_buffer(self.front_buffer, self.width, self.height)
        

    def _update(self) -> None:
        """Обновление экрана: сначала отрисовка в back_buffer, затем swap и render"""
        KeyListener().update()
        
        self.clear_buffer(self.back_buffer) 
        
        self.update()
        
        for child in self.children:
            child.draw(self)
            
        if self.performance_vision and self.performance_checker is not None:
            self.performance_checker.update()
            self.performance_checker.draw(self)
        
        self.swap_buffers()
        self.render()
    
    def draw(self) -> None:
        """Основной цикл отрисовки с использованием WinAPI"""
        try:
            self.win_console.clear_screen()
            self.win_console.set_cursor_visibility(False)
            
            while self.is_active:
                self._update()
        finally:
            self.win_console.set_cursor_visibility(True)
            
    def get_w(self) -> int:
        return self.width
    
    def get_h(self) -> int:
        return self.height
        
            