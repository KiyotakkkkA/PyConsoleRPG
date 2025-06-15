from src.services.frontend.core import Component
from src.services.frontend.ui.general import Text
from src.services.output import Color
from src.services.events import Keys
from typing import TYPE_CHECKING
from src.services.events import EventSystem

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Input(Component):
    
    __allowed_literals = {
        'a': Keys.A,
        'b': Keys.B,
        'c': Keys.C,
        'd': Keys.D,
        'e': Keys.E,
        'f': Keys.F,
        'g': Keys.G,
        'h': Keys.H,
        'i': Keys.I,
        'j': Keys.J,
        'k': Keys.K,
        'l': Keys.L,
        'm': Keys.M,
        'n': Keys.N,
        'o': Keys.O,
        'p': Keys.P,
        'q': Keys.Q,
        'r': Keys.R,
        's': Keys.S,
        't': Keys.T,
        'u': Keys.U,
        'v': Keys.V,
        'w': Keys.W,
        'x': Keys.X,
        'y': Keys.Y,
        'z': Keys.Z,
        '0': Keys.NUM_0,
        '1': Keys.NUM_1,
        '2': Keys.NUM_2,
        '3': Keys.NUM_3,
        '4': Keys.NUM_4,
        '5': Keys.NUM_5,
        '6': Keys.NUM_6,
        '7': Keys.NUM_7,
        '8': Keys.NUM_8,
        '9': Keys.NUM_9,
        
    }
    
    __allowed_keys = {}
    
    __allowed_enter_types = {
        "text": True,
        "solo_key": True,
    }
    
    __allowed_solo_keys_brackets = {
        'br_square': {
            'open': '[',
            'close': ']',
        },
        'br_round': {
            'open': '(',
            'close': ')',
        },
        'br_curly': {
            'open': '{',
            'close': '}',
        },
        'br_quote': {
            'open': '"',
            'close': '"',
        },
        'br_apostrophe': {
            'open': "'",
            'close': "'",
        },
        'br_angle': {
            'open': '<',
            'close': '>',
        },
        'br_none': {
            'open': '',
            'close': '',
        },
    }
    
    def __init__(self, x: int,
                 y: int,
                 width: int,
                 label_title: str = "",
                 label_color: str = Color.RESET,
                 label_selected_color: str = Color.RESET,
                 label_active_color: str = Color.RESET,
                 input_color: str = Color.RESET,
                 input_selected_color: str = Color.RESET,
                 input_active_color: str = Color.RESET,
                 enter_type: str = "text",
                 enter_data_event_name: str = "enter_data",
                 solo_key_brackets: str = "br_none",
                 end_symbol="_"):
        """
        Инициализация компонента Input
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            width: Ширина компонента
            label_title: Заголовок компонента
            label_color: Цвет заголовка ввода
            label_selected_color: Цвет заголовка ввода при фокусе
            label_active_color: Цвет заголовка ввода при активности
            input_color: Цвет текста ввода
            input_selected_color: Цвет текста ввода при фокусе
            input_active_color: Цвет текста ввода при активности
            enter_type: Тип ввода ("text" или "solo_key")
            solo_key_brackets: Тип скобок для одиночного ключа
            enter_data_event_name: Имя события, которое будет генерироваться при нажатии Enter
            end_symbol: Символ, который будет добавляться в конец вводимого текста
            - Возможные значения для solo_key_brackets:
                br_square: []\n
                br_round: ()\n
                br_curly: {}\n
                br_quote: ""\n
                br_apostrophe: ''\n
                br_angle: <>\n
        """
        super().__init__(x, y, width, 1, (0, 0, 0, 0))
        
        self.reactive('selected', False)
        self.reactive('active', False)
        self.reactive('input_value', "")
        self.reactive('enter_type', enter_type)
        self.reactive('label_color', label_color)
        self.reactive('input_color', input_color)
        self.reactive('label_selected_color', label_selected_color)
        self.reactive('input_selected_color', input_selected_color)
        self.reactive('label_active_color', label_active_color)
        self.reactive('input_active_color', input_active_color)
        self.reactive('end_symbol', end_symbol)
        self.reactive('solo_key_brackets', solo_key_brackets)
        self.reactive('enter_data_event_name', enter_data_event_name)
        
        if not enter_type in self.__allowed_enter_types:
            raise ValueError(f"Invalid enter_type: {enter_type}")
        
        if not solo_key_brackets in self.__allowed_solo_keys_brackets:
            raise ValueError(f"Invalid solo_key_brackets: {solo_key_brackets}")
        
        self.label_title = Text(x=x, y=y, text=label_title, fg_color=label_color)
        self.input_text = Text(x=x + self.label_title.width + 1, y=y, text="", fg_color=input_color)
        self.add_child(self.label_title)
        self.add_child(self.input_text)
        
        self._process_keys_to_symbols()
        
        self._events.append((Keys.BACKSPACE, self._on_backspace))
        self._events.append((Keys.ENTER, self._on_enter))
        
        self._bind_to_keys()
    
    def set_selected(self, selected: bool):
        """
        Установка фокуса на компоненте
        
        Args:
            selected: Флаг фокуса
        """
        self.selected = selected
    
    def set_active(self, active: bool):
        """
        Установка активности компонента
        
        Args:
            active: Флаг активности
        """
        self.active = active
        
    def set_label_width(self, width: int):
        """
        Установка ширины заголовка
        
        Args:
            width: Ширина заголовка
        """
        self.label_title.width = width
        self.input_text.x = self.x + self.label_title.width + 1
        
    def get_input_value(self) -> str:
        """
        Получение значения ввода
        
        Returns:
            str: Значение ввода
        """
        return self.input_value
        
    def _set_text(self, text: str):
        self.input_value = text
        data_to_display = text
        
        if self._is_type_a_text() and self.active:
            data_to_display = self.input_value + self.end_symbol
        
        elif self._is_type_a_solo_key():
            data_to_display = f"{self.__allowed_solo_keys_brackets[self.solo_key_brackets]['open']} {self.input_value or ' '} {self.__allowed_solo_keys_brackets[self.solo_key_brackets]['close']}"
            self.active = False
            
        self.input_text.set_text(data_to_display)
        
    def _on_backspace(self):
        if not self.active:
            return
        
        self.input_value = self.input_value[:-1]
        self._set_text(self.input_value)
        
    def _is_type_a_solo_key(self):
        return self.enter_type == "solo_key"
    
    def _is_type_a_text(self):
        return self.enter_type == "text"
        
    def _on_enter(self):
        
        if not self.selected:
            return
        
        if not self.active:
            if self._is_type_a_solo_key():
                self._set_text('')
            self.active = True
            return
        
        if self._is_type_a_text():
            self._on_enter_text()
        elif self._is_type_a_solo_key():
            self._on_enter_solo_key()
            
    def _on_enter_text(self):
        if self.active:
            self.active = False
            
            self._set_text(self.input_text.text[:-1])
            
            EventSystem().emit(self.enter_data_event_name, {'value': self.input_text.text[:-1]})
            
    def _on_enter_solo_key(self):
        if self.active:
            self.active = False
            EventSystem().emit(self.enter_data_event_name, {'value': self.input_value})
            
    def _on_key_press(self, key: int):
        if not self.active:
            return
        
        self.input_value += self.__allowed_keys[key]
        self._set_text(self.input_value)
        
    def _process_keys_to_symbols(self):
        for k, v in self.__allowed_literals.items():
            self.__allowed_keys[v] = k
            
    def _bind_to_keys(self):
        for key, value in self.__allowed_literals.items():
            self._events.append((value, lambda value=value: self._on_key_press(value)))
    
    def draw(self, screen: 'Screen'):
        self.label_title.fg_color = self.label_active_color if self.active else self.label_selected_color if self.selected else self.label_color
        self.input_text.fg_color = self.input_active_color if self.active else self.input_selected_color if self.selected else self.input_color
        
        self.label_title.draw(screen)
        self.input_text.draw(screen)
            