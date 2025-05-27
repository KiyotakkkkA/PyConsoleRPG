from .Screen import Screen
from typing import Dict, Optional
from src.services.events import KeyListener

class ScreenManager:
    _screens: Dict[str, 'Screen'] = {}
    _current_screen: Optional[str] = None

    @classmethod
    def add_screen(cls, name: str, screen: 'Screen'):
        cls._screens[name] = screen
        
    @classmethod
    def add_screens(cls, screens: Dict[str, 'Screen']):
        cls._screens.update(screens)
        
    @classmethod
    def remove_screen(cls, name: str):
        if name in cls._screens:
            KeyListener().unregister_screen(cls._screens[name])
            del cls._screens[name]
        
    @classmethod
    def set_current_screen(cls, name: str):
        if cls._current_screen:
            cls.remove_screen(cls._current_screen)
        cls._current_screen = name
        cls.draw()
        
    @classmethod
    def get_current_screen(cls) -> 'Screen':
        return cls._screens[cls._current_screen]
            
    @classmethod
    def draw(cls):
        if cls._current_screen and cls._current_screen in cls._screens:
            cls._screens[cls._current_screen].draw()