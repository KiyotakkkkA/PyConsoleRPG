from src.entities.interfaces import Computable
from typing import List, Any, Dict, Set, Callable, Tuple
from src.services.events.KeyListener import KeyListener, Keys
from src.services.storage.State import State
from src.services.backend.managers import LocaleManager
from src.config.Config import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.frontend.core.Screen import Screen

class Component(Computable):
    """
    Класс, представляющий компонент, наследуемый от Computable
    """
    
    _base_sounds_dir = Config.SOUNDS_DIR
    
    _locale_manager = LocaleManager.get_instance()
    
    def __init__(self, x: int, y: int, width: int, height: int, paddings: tuple = (1, 1, 1, 1)):
        """
        Инициализация компонента
        
        Args:
            x: Координата x компонента
            y: Координата y компонента
            width: Ширина компонента
            height: Высота компонента
            paddings: (pt, pb, pr, pl) по умолчанию (1, 1, 1, 1)
        """
        self.event_handlers: Dict[str, Set[Callable]] = {}
        self.key_handlers: Dict[Keys, Set[Callable]] = {}
        
        self._changed = True
        self._cache = {}
        self._screen: 'Screen' = None
        self._events: List[Tuple[Keys, Callable]] = []
        
        super().__init__()
        
        self.reactive('allow_sound', False)
        
        self.reactive('width', width)
        self.reactive('height', height)
        self.reactive('paddings', paddings)
        
        self.reactive('active', False)
        self.reactive('selected', False)
        self.reactive('events_enabled', True)
        self.reactive('visible', True)
        
        self.reactive('children', [])
        self.reactive('parent', None)
        self.reactive('_components', {})
        
        self.reactive('x', x)
        self.reactive('y', y)
        self.reactive('abs_x', x)
        self.reactive('abs_y', y)
        
        self.computed('inner_width', lambda: self.width - self.paddings[2] - self.paddings[3], ['width', 'paddings'])
        self.computed('inner_height', lambda: self.height - self.paddings[0] - self.paddings[1], ['height', 'paddings'])
    
    def set_visible(self, visible: bool):
        """
        Устанавливает видимость компонента и определяет, нужно ли рендерить компонент
        
        Args:
            visible: Флаг, определяющий видимость компонента
        """
        self.visible = visible
        
    def set_allow_sound(self, allow_sound: bool):
        """
        Устанавливает возможность воспроизведения звука
        
        Args:
            allow_sound: Флаг, разрешающий воспроизведение звука
        """
        self.allow_sound = allow_sound
        
    def play_sound(self, sound: str = None):
        """
        Проигрывает звук
        
        Args:
            sound: Имя файла звука
        """
        from src.services.frontend.core.managers.AudioManager import AudioManager
        
        if self.allow_sound and sound:
            AudioManager.get_instance().play_sound(f"{self._base_sounds_dir}/{sound}")
            
    def set_events_enabled(self, events_enabled: bool):
        """
        Устанавливает возможность обработки событий
        
        Args:
            events_enabled: Флаг, разрешающий обработку событий
        """
        self.events_enabled = events_enabled
    
    def set_active(self, active: bool):
        """
        Устанавливает активность компонента
        
        Args:
            active: Флаг активности
        """
        self.active = active
        
    def set_selected(self, selected: bool):
        """
        Устанавливает выделенность компонента
        
        Args:
            selected: Флаг выделенности
        """
        self.selected = selected
        
    def on_event(self, event_name: str, handler: callable):
        """
        Подписка на событие
        
        Args:
            event_name: Имя события
            handler: Обработчик события
        """
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = set()
        self.event_handlers[event_name].add(handler)
    
    def unsubscribe(self, event_name: str, handler: callable):
        """
        Отписка от события
        
        Args:
            event_name: Имя события
            handler: Обработчик события
        """
        if event_name in self.event_handlers and handler in self.event_handlers[event_name]:
            self.event_handlers[event_name].remove(handler)
    
    def emit_event(self, event_name: str, data: Any = None):
        """
        Генерация события
        
        Args:
            event_name: Имя события
            data: Данные события
        """
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                handler(data)
                
    def add_children(self, children: List['Component'], names: List[str] = None):
        """
        Добавление списка дочерних компонентов
        
        Args:
            children: Список компонентов, которые будут добавлены
            names: Список имен для компонентов
        """
        new_children = self.children.copy()
        new_children.extend(children)
        
        for i, child in enumerate(children):
            State._components_counter += 1
            if names is not None:
                self._components[names[i]] = child
                child.parent = self
            else:
                self._components[f"{type(child).__name__}{State._components_counter}"] = child
                child.parent = self
        self.children = new_children
        
    def add_child(self, child: 'Component', name: str = None):
        """
        Добавление дочернего компонента
        
        Args:
            child: Компонент, который будет добавлен
            name: Имя компонента
        """
        State._components_counter += 1
        self.children.append(child)
        if name is not None:
            self._components[name] = child
        else:
            self._components[f"{type(child).__name__}{State._components_counter}"] = child
        
        child.parent = self
        child._screen = self._screen
            
    def set_child(self, child: 'Component', name: str = None):
        """
        Установка дочернего компонента
        
        Args:
            child: Компонент, который будет установлен
            name: Имя компонента
        """
        self._components[name] = child
        
    def unbind_child(self, child: 'Component'):
        """
        Отвязка дочернего компонента
        
        Args:
            child: Компонент, который будет отвязан
        """
        self.children.remove(child)
        child.parent = None
        
    def get_child_by_name(self, name: str):
        """
        Получение дочернего компонента по имени
        
        Args:
            name: Имя компонента
        """
        return self._components[name]
    
    def get_all_components_names(self):
        return self._components
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_abs_x(self):
        return self.abs_x
    
    def get_abs_y(self):
        return self.abs_y
    
    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def set_height(self, height: int):
        self.height = height
        
    def set_width(self, width: int):
        self.width = width
        
    def set_x(self, x: int):
        self.x = x
        self.abs_x = x
        
    def set_y(self, y: int):
        self.y = y
        self.abs_y = y
    
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
        
        KeyListener().register_component(self)
    
    def unbind_key(self, key: Keys, handler: Callable) -> None:
        """
        Отвязка обработчика от нажатия клавиши
        
        Args:
            key: Клавиша из перечисления Keys
            handler: Функция-обработчик
        """
        if key in self.key_handlers and handler in self.key_handlers[key]:
            self.key_handlers[key].remove(handler)
            
        if all(len(handlers) == 0 for handlers in self.key_handlers.values()):
            KeyListener().unregister_component(self)
            
    def _calculate_self_size(self):
        for child in self.children:
            child.y = child.abs_y + self.paddings[0]
            child.x = child.abs_x + self.paddings[3]
            
            if child.abs_y + self.paddings[0] + self.paddings[1] + child.height >= self.abs_y + self.height:
                self.height = child.abs_y + self.paddings[0] + self.paddings[1] + child.height - self.abs_y + self.paddings[2]
            if child.abs_x + self.paddings[3] + self.paddings[2] + child.width >= self.abs_x + self.width:
                self.width = child.abs_x + self.paddings[3] + self.paddings[2] + child.width - self.abs_x + self.paddings[2]

    def mark_changed(self):
        """Отмечает компонент как измененный и все связанные компоненты"""
        self._changed = True
        
        if self.parent is not None:
            self.parent._changed = True
        
        if hasattr(self, '_cache'):
            self._cache = {}
    
    def draw(self, screen):
        """
        Отрисовка компонента на экран
        
        Args:
            screen: Экран, на который производится отрисовка
        """
        
        if self._changed:
            if self.parent is None:
                for child in self.children:
                    child._changed = True
            
            for child in self.children:
                child._changed = True
                child.draw(screen)
                
            self._changed = False
        else:
            for child in self.children:
                if child._changed:
                    child.draw(screen)