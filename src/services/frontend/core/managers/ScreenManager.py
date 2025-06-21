from ..Screen import Screen
from .AudioManager import AudioManager
from typing import Dict, Optional, List, Any
from src.services.events import KeyListener
from src.config.Config import Config

class ScreenManager:
    """
    Класс, представляющий менеджер экранов
    """
    _instance = None
    
    _audio_manager = AudioManager.get_instance()
    
    _screens: Dict[str, Dict[str, Any]] = {}
    _current_screen: Optional[str] = None
    _current_screen_instance: Optional['Screen'] = None
    _screen_history: List[str] = []  # История экранов для возврата назад
    _active_instances: Dict[str, 'Screen'] = {}  # Словарь активных экземпляров экранов
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def add_screen(cls, name: str, screens_dict: Dict[str, Any]):
        """
        Добавляет экран
        
        Args:
            name: Имя экрана
            screen: Экран
        """
        cls._screens[name] = {
            "screen": screens_dict["screen"],
            "bg_music": cls.path_to_bg_music(name, screens_dict["bg_music"])}
        
    @classmethod
    def path_to_bg_music(cls, name: str, music_file: str):
        """
        Устанавливает музыку для экрана
        
        Args:
            name: Имя экрана
            music_file: Путь к файлу музыки
        """
        return f"{Config.BG_MUSIC_DIR}/{music_file}" if music_file else None
        
    @classmethod
    def add_screens(cls, screens: Dict[str, Dict[str, Any]]):
        """
        Добавляет несколько экранов
        
        Args:
            screens: Словарь экранов
        """
        for name, screen in screens.items():
            cls.add_screen(name, screen)
        
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
            cls._current_screen_instance = cls._screens[name]["screen"]()
            cls._active_instances[name] = cls._current_screen_instance
                   
        KeyListener().register_screen(cls._current_screen_instance)
        
        if cls._screens[name]["bg_music"]:
            cls._audio_manager.play_music(cls._screens[name]["bg_music"])
        else:
            cls._audio_manager.stop_music()
        
        cls._current_screen_instance.before_mount()
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