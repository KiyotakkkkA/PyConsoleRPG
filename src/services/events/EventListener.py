from abc import ABC, abstractmethod
from .EventSystem import EventSystem
from typing import Callable


class EventListener(ABC):
    event_system = EventSystem()
        
    def on_event(self, event_name: str, callback: Callable):
        """
        Подписка на событие
        
        Args:
            event_name: Имя события
            callback: Обработчик события
        """
        self.event_system.subscribe(event_name, callback)
        
    def emit_event(self, event_name: str, data: dict | None = None):
        """
        Вызов события
        
        Args:
            event_name: Имя события
            data: Данные события
        """
        if data is None:
            data = {}
        self.event_system.emit(event_name, data)
    
