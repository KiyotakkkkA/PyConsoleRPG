from abc import ABC, abstractmethod
from .EventSystem import EventSystem
from typing import Callable


class EventListener(ABC):
    event_system = EventSystem()
        
    def on_event(self, event_name: str, callback: Callable):
        self.event_system.subscribe(event_name, callback)
        
    def emit_event(self, event_name: str, data: dict | None):
        if data is None:
            data = {}
        self.event_system.emit(event_name, data)
    
