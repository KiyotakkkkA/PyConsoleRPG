from src.services.frontend.core import Screen, ScreenManager
from src.services.frontend.ui.containers import Panel
from src.services.frontend.ui.general import Text, Menu
from src.services.output import Color
from src.services.events import Keys

from src.services.utils import ToArtConverter

class MainScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    @staticmethod
    def start_game():
        ScreenManager.set_current_screen("game")
    
    @staticmethod
    def exit():
        """Выход из игры"""
        exit()
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art("UPDATE TITLE")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        menu_x = self.get_w() // 2 - 2
        menu_y = self.title.y + self.title.height + 1
        
        self.menu = Menu(menu_x, menu_y, 40, paddings=(1, 1, 1, 1), gap=2)
        self.add_child(self.menu)
        
        self.menu.add_items([
            (("Новая игра", Color.WHITE), Keys.N, lambda: MainScene.start_game()),
            (("Загрузить игру", Color.WHITE), Keys.L, lambda: print("Загрузить игру")),
            (("Настройки", Color.WHITE), Keys.S, lambda: ScreenManager.set_current_screen("settings")),
            (("Управление", Color.WHITE), Keys.C, lambda: print("Управление")),
            (("Выход", Color.WHITE), Keys.Q, lambda: MainScene.exit()),
        ])
    
    def update(self):
        pass
        
        