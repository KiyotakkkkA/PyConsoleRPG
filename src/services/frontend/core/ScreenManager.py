from .Screen import Screen
from typing import Dict, Optional, List
from src.services.events import KeyListener

class ScreenManager:
    """
    Класс, представляющий менеджер экранов
    """
    _screens: Dict[str, 'Screen'] = {}
    _current_screen: Optional[str] = None
    _current_screen_instance: Optional['Screen'] = None
    _screen_history: List[str] = []  # История экранов для возврата назад
    _active_instances: Dict[str, 'Screen'] = {}  # Словарь активных экземпляров экранов

    @classmethod
    def add_screen(cls, name: str, screen: 'Screen'):
        """
        Добавляет экран
        
        Args:
            name: Имя экрана
            screen: Экран
        """
        cls._screens[name] = screen
        
    @classmethod
    def add_screens(cls, screens: Dict[str, 'Screen']):
        """
        Добавляет несколько экранов
        
        Args:
            screens: Словарь экранов
        """
        cls._screens.update(screens)
        
    @classmethod
    def remove_screen(cls, name: str):
        """
        Удаляет экран полностью
        
        Args:
            name: Имя экрана
        """
        if name in cls._screens:
            if name in cls._active_instances:
                KeyListener().unregister_screen(cls._active_instances[name])
                del cls._active_instances[name]
            
            if name in cls._screen_history:
                cls._screen_history.remove(name)
                
            del cls._screens[name]
            
        
    @classmethod
    def set_current_screen(cls, name: str, add_to_history: bool = True):
        """
        Устанавливает текущий экран
        
        Args:
            name: Имя экрана
            add_to_history: Добавлять ли текущий экран в историю
        """
        if cls._current_screen:
            if cls._current_screen_instance:
                KeyListener().unregister_screen(cls._current_screen_instance)
            if add_to_history and cls._current_screen not in cls._screen_history:
                cls._screen_history.append(cls._current_screen)
        
        cls._current_screen = name
        
        if name in cls._active_instances:
            cls._current_screen_instance = cls._active_instances[name]
        else:
            cls._current_screen_instance = cls._screens[name]()
            cls._active_instances[name] = cls._current_screen_instance
        
        KeyListener().register_screen(cls._current_screen_instance)
        
        cls.draw()
        
    @classmethod
    def get_current_screen(cls) -> 'Screen':
        """
        Получает текущий экран
        
        Returns:
            Экран
        """
        return cls._current_screen_instance
            
    @classmethod
    def draw(cls):
        """
        Отрисовывает текущий экран
        """
        if cls._current_screen and cls._current_screen in cls._screens:
            cls._current_screen_instance.draw()
            
    @classmethod
    def go_back(cls):
        """
        Возвращается к предыдущему экрану в истории
        
        Returns:
            bool: True если успешно выполнен переход назад, False если истории нет
        """
        if cls._screen_history:
            previous_screen = cls._screen_history.pop()
            if previous_screen in cls._screens:
                cls.set_current_screen(previous_screen, add_to_history=False)
                return True
        return False
        
    @classmethod
    def navigate_to_screen(cls, name: str, add_to_history: bool = True):
        """
        Произвольно перемещается к указанному экрану по его имени
        
        Args:
            name: Имя экрана, на который нужно переключиться
            add_to_history: Добавлять ли текущий экран в историю
            
        Returns:
            bool: True если экран найден и переключение произошло, False если экран не найден
        """
        if name in cls._screens:
            cls.set_current_screen(name, add_to_history=add_to_history)
            return True
        return False
        
    @classmethod
    def clear_history(cls):
        """
        Очищает историю экранов
        """
        cls._screen_history = []
        
    @classmethod
    def clear_inactive_screens(cls):
        """
        Очищает все неактивные экраны из памяти
        """
        screens_to_clear = [name for name in cls._active_instances if name != cls._current_screen]
        for name in screens_to_clear:
            if name in cls._active_instances:
                KeyListener().unregister_screen(cls._active_instances[name])
                del cls._active_instances[name]