from src.services.frontend.core import Screen, Alignment
from src.services.events import Keys
from src.services.frontend.ui.containers import Table
from src.services.output import Color

class SettingsScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.inventory_table = Table(10, 10, self.get_w() - 20, [
            "Название",
            'Тип',
            'Редкость',
            "Кол-во",
            'Цена',
            "Вес",
        ], [
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
        ], Alignment.CENTER, Alignment.LEFT)
        
        self.inventory_table.add_rows([
            [
                f"Название {_}",
                "Тип",
                "Редкость",
                "Кол-во",
                "Цена",
                "Вес",
            ] for _ in range(10)
        ])
        
        self.add_child(self.inventory_table)
        
    def update(self):
        pass