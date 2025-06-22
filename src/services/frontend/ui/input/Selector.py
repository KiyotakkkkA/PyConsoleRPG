from src.services.frontend.core import Component
from src.services.frontend.ui.general import Text
from src.services.output import Color
from src.services.events import Keys
from typing import TYPE_CHECKING, List, Tuple, Callable
from src.services.events import EventSystem

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Selector(Component):
    
    __selection_types = {
        'none-current-none': True,
        'minus-current-plus': True,
        'prev-current-next': True,
    }
    
    def __init__(self, x: int,
                 y: int,
                 enter_data_event_name: str = "enter_data",
                 label_title: str = "",
                 label_color: str = Color.RESET,
                 label_selected_color: str = Color.RESET,
                 label_active_color: str = Color.RESET,
                 value_color: str = Color.RESET,
                 value_selected_color: str = Color.RESET,
                 value_active_color: str = Color.YELLOW,
                 selection_type: str = 'prev-current-next',
                 min_value: int = 0,
                 max_value: int = 10,
                 options: list[tuple[str, str]] = []):
        """
        Инициализация компонента Selector
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            label_title: Текст заголовка
            label_color: Цвет заголовка
            label_selected_color: Цвет заголовка при фокусе
            label_active_color: Цвет заголовка при активности
            value_color: Цвет значения
            value_selected_color: Цвет значения при фокусе
            value_active_color: Цвет значения при активности
            enter_data_event_name: Имя события, которое будет генерироваться при нажатии Enter
            min_value: Минимальное значение для типа minus-current-plus
            max_value: Максимальное значение для типа minus-current-plus
            options: Список вариантов для типов prev-current-next и none-current-none (value, name)
            selection_type: Тип оформления
            - Возможные значения selection_type:
                none-current-none: Нет оформления
                minus-current-plus: - < data > +
                prev-current-next: prev < data > next
        """
        super().__init__(x, y, 1, 1, (0, 0, 0, 0))
        
        self.reactive('enter_data_event_name', enter_data_event_name)
        self.reactive('label_title', label_title)
        self.reactive('label_color', label_color)
        self.reactive('label_selected_color', label_selected_color)
        self.reactive('label_active_color', label_active_color)
        self.reactive('value_color', value_color)
        self.reactive('value_selected_color', value_selected_color)
        self.reactive('value_active_color', value_active_color)
        self.reactive('selection_type', selection_type)
        self.reactive('min_value', min_value)
        self.reactive('max_value', max_value)
        self.reactive('options', options)
        
        self.reactive('current_index', 0)
        self.reactive('current_value', min_value)
        
        self.computed('current_label_color', self._calculate_current_label_color, ['selected', 'active'])
        self.computed('current_value_color', self._calculate_current_value_color, ['selected', 'active'])
        
        if not selection_type in self.__selection_types:
            raise ValueError(f"Invalid selection_type: {selection_type}")
        
        if selection_type == 'minus-current-plus' and options:
            raise ValueError("Options are not allowed for selection_type 'minus-current-plus'")
        
        self.label = Text(x=x, y=y, text=label_title, fg_color=label_color)
        self.width = self.label.width + 1
        
        self.prev = Text(x=1, y=y, text="", fg_color=Color.RESET)
        self.width += self.prev.width + 1
        self.prev_bracket = Text(x=1, y=y, text="", fg_color=Color.BRIGHT_BLACK)
        self.width += self.prev_bracket.width + 1
        self.current = Text(x=1, y=y, text="", fg_color=label_color)
        self.width += self.current.width + 1
        self.next_bracket = Text(x=1, y=y, text="", fg_color=Color.BRIGHT_BLACK)
        self.width += self.next_bracket.width + 1
        self.next = Text(x=1, y=y, text="", fg_color=Color.RESET)
        self.width += self.next.width + 1
        
        self.add_child(self.label)
        self.add_child(self.prev)
        self.add_child(self.prev_bracket)
        self.add_child(self.current)
        self.add_child(self.next_bracket)
        self.add_child(self.next)
        
        self._events.append((Keys.LEFT, self._select_backward))
        self._events.append((Keys.RIGHT, self._select_forward))
        self._events.append((Keys.ENTER, self._on_enter))
        
    def set_label_text(self, text: str):
        """
        Установка текста заголовка
        
        Args:
            text: Текст заголовка
        """
        self.label.set_text(text)
        
    def get_value(self):
        """
        Получение текущего значения
        
        Returns:
            int: Текущее значение
        """
        if self.is_type_minus_current_plus():
            return self.current_value
        return self.options[self.current_index][0]
    
    def set_value(self, value: int):
        """
        Установка численного значения [работает только в режиме minus-current-plus]
        
        Args:
            value: Значение
        """
        if not self.is_type_minus_current_plus():
            return
        
        self.current_value = min(max(value, self.min_value), self.max_value)
        
    def set_option(self, key: str):
        """
        Установка опции по ключу [работает только в режиме prev-current-next и none-current-none]
        
        Args:
            key: Ключ опции
        """
        if not self.is_type_prev_current_next() and not self.is_type_none_current_none():
            return
        
        for option in self.options:
            if option[0] == key:
                self.current_index = self.options.index(option)
                return
        
    def _on_enter(self):
        if self.selected and not self.active:
            self.set_active(True)
            return
        
        if self.active:
            EventSystem().emit(self.enter_data_event_name, {'value': self.get_value()})
            self.set_active(False)
        
    def _select_forward(self):
        if not self.active:
            return
        
        if self.is_type_none_current_none() or self.is_type_prev_current_next():
            self.current_index = min(self.current_index + 1, len(self.options) - 1)
            return
        
        self.current_value = min(self.current_value + 1, self.max_value)
            
    def _select_backward(self):
        if not self.active:
            return
        
        if self.is_type_none_current_none() or self.is_type_prev_current_next():
            self.current_index = max(self.current_index - 1, 0)
            return
        
        self.current_value = max(self.current_value - 1, self.min_value)  
    
    def is_type_none_current_none(self):
        return self.selection_type == "none-current-none"
    
    def is_type_minus_current_plus(self):
        return self.selection_type == "minus-current-plus"
    
    def is_type_prev_current_next(self):
        return self.selection_type == "prev-current-next"
        
    def _configure_none_current_none_mode(self, screen: 'Screen'):
        self.prev_bracket.set_text("<")
        
        data_to_display = f" {self.options[self.current_index][1]} "
        self.current.set_text(data_to_display)
    
        self.next_bracket.set_text(">")
        
        self._pos_config()
        self._color_config()
        
    def _configure_minus_current_plus_mode(self, screen: 'Screen'):
        self.prev.set_text("-")
        self.prev.set_fg_color(Color.BRIGHT_RED if self.current_value > self.min_value and self.active else Color.BLACK)
        
        self.prev_bracket.set_text("<")
        
        data_to_display = f"{self.current_value}"
        self.current.set_text(data_to_display)
        
        self.next_bracket.set_text(">")
        
        self.next.set_text("+")
        self.next.set_fg_color(Color.BRIGHT_GREEN if self.current_value < self.max_value and self.active else Color.BLACK)
        
        self._pos_config()
        self._color_config()
        
    def _configure_prev_current_next_mode(self, screen: 'Screen'):
        if self.current_index == 0:
            self.prev.set_text("")
        else:
            self.prev.set_text(self.options[self.current_index - 1][1])
            
        self.prev_bracket.set_text("<")
            
        data_to_display = f"{self.options[self.current_index][1]}"
        self.current.set_text(data_to_display)
        
        self.next_bracket.set_text(">")
            
        if self.current_index == len(self.options) - 1:
            self.next.set_text("")
        else:
            self.next.set_text(self.options[self.current_index + 1][1])
            
        self._pos_config()
        self._color_config()
    
    def _pos_config(self):
        self.prev.set_x(self.label.x + self.label.width + 1)
        self.prev_bracket.set_x(self.prev.x + self.prev.width + 1)
        self.current.set_x(self.prev_bracket.x + self.prev_bracket.width + 1)
        self.next_bracket.set_x(self.current.x + self.current.width + 1)
        self.next.set_x(self.next_bracket.x + self.next_bracket.width + 1)
        
    def _color_config(self):
        self.label.set_fg_color(self.current_label_color)
        self.current.set_fg_color(self.current_value_color)
        
    def _calculate_current_value_color(self):
        if self.selected and not self.active:
            return self.value_selected_color
        elif self.active:
            return self.value_active_color
        else:
            return self.value_color
        
    def _calculate_current_label_color(self):
        if self.selected and not self.active:
            return self.label_selected_color
        elif self.active:
            return self.label_active_color
        else:
            return self.label_color
        
    def draw(self, screen: 'Screen'):
        self.label.draw(screen)
        
        if self.is_type_none_current_none():
            self._configure_none_current_none_mode(screen)
        elif self.is_type_minus_current_plus():
            self._configure_minus_current_plus_mode(screen)
        elif self.is_type_prev_current_next():
            self._configure_prev_current_next_mode(screen)
        
        self.prev.draw(screen)
        self.prev_bracket.draw(screen)
        self.current.draw(screen)
        self.next_bracket.draw(screen)
        self.next.draw(screen)
        

            