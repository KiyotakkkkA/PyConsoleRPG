from typing import List, Dict, Callable, Set, Tuple, TYPE_CHECKING
from src.services.output import Color, WinConsole
from src.services.events import EventListener, KeyListener, Keys
from src.services.backend.managers import LocaleManager, GlobalMetadataManager
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
    
    _locale_manager = LocaleManager.get_instance()
    _global_metadata_manager = GlobalMetadataManager.get_instance()
    
    def __init__(self):
        super().__init__()
        
        self.win_console = WinConsole()
        self.width = self.win_console.width
        self.height = self.win_console.height
        
        self.front_buffer: List[List[ScreenPixel]] = [[ScreenPixel() for _ in range(self.width)] for _ in range(self.height)]
        self.back_buffer: List[List[ScreenPixel]] = [[ScreenPixel() for _ in range(self.width)] for _ in range(self.height)]
        
        self.children: List[Component] = []
        self.is_active = True
        self.is_in_dialog = False
        self.performance_vision = False
        self.performance_checker = None
        
        self.key_handlers: Dict[Keys, Set[Callable]] = {}
        self.components_events: List[Tuple[Keys, Callable]] = []
        
        self.init()
        
        self.collect_bind_keys(self)
        
        self._instances[self.__class__.__name__] = self
        
        KeyListener().register_screen(self)
        
    def with_error_dialog_window_preset(self, text: str,
                                       pos: Tuple[int, int],
                                       size: Tuple[int, int],
                                       text_color: str = Color.BRIGHT_RED):
        """
        Добавляет на экран предустановленный компонент DialogWindow с для отображения ошибок
        
        Args:
            text: Текст, отображаемый в диалоговом окне
            pos: Позиция диалогового окна (x, y)
            size: Размер диалогового окна (ширина, высота)
            text_color: Цвет текста в диалоговом окне
        """
        from src.services.frontend.ui.containers import DialogWindow
        
        if self.is_in_dialog: return
        
        self.error_dialog_window = DialogWindow(x=pos[0],
                                          y=pos[1],
                                          width=size[0],
                                          height=size[1],
                                          text=text,
                                          ctype="OK",
                                          text_color=text_color)
        
        self.is_in_dialog = True
        
        self.add_child(self.error_dialog_window)
        self.error_dialog_window.set_active(True)
        
        self.error_dialog_window.bind_yes(self.error_dialog_window_close_dialog)
        
    def with_info_dialog_window_preset(self, text: str,
                                       pos: Tuple[int, int],
                                       size: Tuple[int, int],
                                       text_color: str = Color.BRIGHT_YELLOW):
        """
        Добавляет на экран предустановленный компонент DialogWindow с для отображения сообщений
        
        Args:
            text: Текст, отображаемый в диалоговом окне
            pos: Позиция диалогового окна (x, y)
            size: Размер диалогового окна (ширина, высота)
            text_color: Цвет текста в диалоговом окне
        """
        from src.services.frontend.ui.containers import DialogWindow
        
        if self.is_in_dialog: return
        
        self.info_dialog_window = DialogWindow(x=pos[0],
                                          y=pos[1],
                                          width=size[0],
                                          height=size[1],
                                          text=text,
                                          ctype="OK",
                                          text_color=text_color)
        
        self.is_in_dialog = True
        
        self.add_child(self.info_dialog_window)
        self.info_dialog_window.set_active(True)
        
        self.info_dialog_window.bind_yes(self.info_dialog_window_close_dialog)
        
    def with_redirect_to_dialog_window_preset(self, text: str,
                                              pos: Tuple[int, int],
                                              size: Tuple[int, int],
                                              text_color: str = Color.BRIGHT_YELLOW,
                                              screen_name: str = 'main'):
        """
        Добавляет на экран предустановленный компонент DialogWindow с для переключения между экранами
        Активация по нажатию клавиши ESC
        
        Args:
            text: Текст, отображаемый в диалоговом окне
            pos: Позиция диалогового окна (x, y)
            size: Размер диалогового окна (ширина, высота)
            text_color: Цвет текста в диалоговом окне
            screen_name: Имя экрана, на который переключается при нажатии на "Да"
        """
        from src.services.frontend.ui.containers import DialogWindow
        
        self.redirect_dialog_window = DialogWindow(x=pos[0],
                                          y=pos[1],
                                          width=size[0],
                                          height=size[1],
                                          text=text,
                                          ctype="YES_NO",
                                          text_color=text_color)
        
        self.bind_key(Keys.ESCAPE, lambda name=screen_name: self.redirect_dialog_window_ask_to_return(name))
    
    def redirect_dialog_window_ask_to_return(self, screen_name: str):
        if self.is_in_dialog: return
        
        self.is_in_dialog = True
        
        self.add_child(self.redirect_dialog_window)
        self.redirect_dialog_window.set_active(True)
        
        self.redirect_dialog_window.bind_yes(lambda name=screen_name: self.redirect_dialog_window_return_to_menu(name))
        self.redirect_dialog_window.bind_no(self.redirect_dialog_window_close_dialog)
    
    def redirect_dialog_window_return_to_menu(self, screen_name: str):
        from src.Game import Game
        
        self.redirect_dialog_window.set_active(False)
        self.unbind_child(self.redirect_dialog_window)
        self.is_in_dialog = False
        Game.screen_manager.navigate_to_screen(screen_name)
            
    def redirect_dialog_window_close_dialog(self):
        self.redirect_dialog_window.set_active(False)
        self.unbind_child(self.redirect_dialog_window)
        self.is_in_dialog = False
        
    def info_dialog_window_close_dialog(self):
        self.info_dialog_window.set_active(False)
        self.unbind_child(self.info_dialog_window)
        self.is_in_dialog = False
        
    def error_dialog_window_close_dialog(self):
        self.error_dialog_window.set_active(False)
        self.unbind_child(self.error_dialog_window)
        self.is_in_dialog = False
        
    def init(self):
        """Выполняется 1 раз при создании экрана"""
        pass
    
    def before_mount(self):
        """Выполняется перед включением экрана"""
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
        """Выполняется каждую итерацию цикла игры"""
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
        from src.services.frontend.ui.containers import Panel, Tab, DialogWindow
        
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
        if not text:
            return
        
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
            if not child.visible:
                continue
            
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
        
            