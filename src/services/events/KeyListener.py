import msvcrt
from enum import Enum
from typing import Dict, Callable, Optional, List
import weakref
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.frontend.core.Component import Component
    from src.services.frontend.core.Screen import Screen

class Keys(Enum):
    """
    Перечисление клавиш с их ASCII кодами
    """
    # Буквы
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122
    
    # Цифры
    NUM_0 = 48
    NUM_1 = 49
    NUM_2 = 50
    NUM_3 = 51
    NUM_4 = 52
    NUM_5 = 53
    NUM_6 = 54
    NUM_7 = 55
    NUM_8 = 56
    NUM_9 = 57
    
    # Специальные клавиши
    ENTER = 13
    ESCAPE = 27
    SPACE = 32
    BACKSPACE = 8
    TAB = 9
    
    UP = 72
    DOWN = 80
    LEFT = 75
    RIGHT = 77
    
    # Функциональные клавиши
    F1 = 59
    F2 = 60
    F3 = 61
    F4 = 62
    F5 = 63
    F6 = 64
    F7 = 65
    F8 = 66
    F9 = 67
    F10 = 68
    F11 = 133
    F12 = 134


class KeyListener:
    """
    Класс для прослушивания клавиатуры и привязки действий к клавишам
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KeyListener, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """
        Инициализация слушателя клавиш
        """
        self.key_bindings: Dict[int, List[Callable]] = {}
        self.components: "weakref.WeakSet['Component']" = weakref.WeakSet()
        self.screens: "weakref.WeakSet['Screen']" = weakref.WeakSet()
        self.last_key: Optional[int] = None
        self.is_special_key = False
        self._cache = {x.value: x for x in Keys}
    
    def bind_key(self, key: Keys, callback: Callable) -> None:
        """
        Привязка функции к клавише
        
        Args:
            key: Клавиша из перечисления Keys
            callback: Функция, которая будет вызвана при нажатии клавиши
        """
        if key.value not in self.key_bindings:
            self.key_bindings[key.value] = []
        self.key_bindings[key.value].append(callback)
    
    def unbind_key(self, key: Keys, callback: Callable) -> None:
        """
        Отвязка функции от клавиши
        
        Args:
            key: Клавиша из перечисления Keys
            callback: Функция, которая нужно отвязать
        """
        if key.value in self.key_bindings and callback in self.key_bindings[key.value]:
            self.key_bindings[key.value].remove(callback)
    
    def register_component(self, component: 'Component') -> None:
        """
        Регистрация компонента для получения событий клавиатуры
        
        Args:
            component: Компонент, который будет получать события
        """
        self.components.add(component)
    
    def unregister_component(self, component: 'Component') -> None:
        """
        Отмена регистрации компонента
        
        Args:
            component: Компонент, который больше не будет получать события
        """
        self.components.discard(component)
    
    def register_screen(self, screen: 'Screen') -> None:
        """
        Регистрация экрана для получения событий клавиатуры
        
        Args:
            screen: Экран, который будет получать события
        """
        self.screens.add(screen)
    
    def unregister_screen(self, screen: 'Screen') -> None:
        """
        Отмена регистрации экрана
        
        Args:
            screen: Экран, который больше не будет получать события
        """
        self.screens.discard(screen)
    
    def check_key(self) -> Optional[Keys]:
        """
        Проверка нажатой клавиши
        
        Returns:
            Нажатая клавиша из перечисления Keys или None, если клавиша не нажата
        """
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            
            if key == 224 or key == 0:
                self.is_special_key = True
                self.last_key = ord(msvcrt.getch())
                return self._cache.get(self.last_key)
            else:
                self.is_special_key = False
                self.last_key = key
                return self._cache.get(key)
        
        return None
    
    def process_key(self) -> None:
        """
        Обработка нажатой клавиши и вызов привязанных функций
        """
        key = self.check_key()
        
        if key is not None:
            key_code = key.value
            
            if key_code in self.key_bindings:
                for callback in self.key_bindings[key_code]:
                    callback()
            
            for component in self.components:
                component.emit_event('key_press', {'key': key})
            
            for screen in self.screens:
                if hasattr(screen, 'on_key_press') and callable(screen.on_key_press):
                    screen.on_key_press(key)
    
    def update(self) -> None:
        """
        Метод обновления, который должен вызываться в главном цикле приложения
        """
        self.process_key()
        
    def get_last_key(self) -> Optional[Keys]:
        """
        Получение последней нажатой клавиши
        
        Returns:
            Последняя нажатая клавиша из перечисления Keys или None
        """
        if self.last_key is not None:
            return self._cache.get(self.last_key)
        return None