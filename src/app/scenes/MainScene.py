from src.services.frontend.core import Screen, ScreenManager
from src.services.frontend.ui.containers import Panel
from src.services.frontend.ui.general import Text, Menu
from src.services.output import Color
from src.services.events import Keys
import json

from src.services.utils import ToArtConverter

class MainScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    @staticmethod
    def new_game():
        ScreenManager.navigate_to_screen("new_game")
        
    @staticmethod
    def continue_game():
        from src.Game import Game
        
        with open(f"{Game.SAVES_DIR}/global.json", "r") as f:
            data = json.load(f)
        
        save_name = data['last_character']
        Game.CURRENT_LOADING_PLAYER = save_name
        
        if Game.load():
            ScreenManager.navigate_to_screen("game")
        
    @staticmethod
    def settings():
        ScreenManager.navigate_to_screen("settings")
        
    @staticmethod
    def controls():
        ScreenManager.navigate_to_screen("controls")
        
    @staticmethod
    def load_game():
        ScreenManager.navigate_to_screen("load_game")
    
    @staticmethod
    def exit():
        from src.Game import Game
        Game.save()
        """Выход из игры"""
        exit()
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art("Обновление")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        menu_x = self.get_w() // 2 - 2
        menu_y = self.title.y + self.title.height + 1
        
        self.menu = Menu(menu_x, menu_y, paddings=(1, 1, 1, 1), gap=2)
        self.add_child(self.menu)
        
        self.menu.add_items([
            (("Продолжить игру", Color.WHITE), Keys.Q, lambda: MainScene.continue_game()),
            (("Новая игра", Color.WHITE), Keys.N, lambda: MainScene.new_game()),
            (("Загрузить игру", Color.WHITE), Keys.L, lambda: MainScene.load_game()),
            (("Настройки", Color.WHITE), Keys.S, lambda: MainScene.settings()),
            (("Управление", Color.WHITE), Keys.C, lambda: MainScene.controls()),
            (("Выход", Color.WHITE), Keys.Q, lambda: MainScene.exit()),
        ])
        
        self.menu.set_selection(0)
        self.menu.set_active(True)
        
        