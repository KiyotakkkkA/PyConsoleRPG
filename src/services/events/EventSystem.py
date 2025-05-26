from typing import Callable

class EventSystem:
    instance = None
    events = {}
    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(EventSystem, cls).__new__(cls)
        return cls.instance
    
    def subscribe(self, event_name: str, callback: Callable):
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable):
        if event_name in self.events:
            self.events[event_name].remove(callback)
    
    def emit(self, event_name: str, *args, **kwargs):
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(*args, **kwargs)
    