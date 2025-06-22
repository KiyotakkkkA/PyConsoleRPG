from src.services.frontend.core import Screen, Alignment
from src.services.events import Keys
from src.services.output import Color
from src.services.frontend.ui.containers import MultiPanel
from src.services.frontend.ui.containers import Panel

class ControlsScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        pass
        
    def update(self):
        pass
        
        