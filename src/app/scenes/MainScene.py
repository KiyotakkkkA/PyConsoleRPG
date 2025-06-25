from src.services.frontend.core import Screen, ScreenManager, Alignment
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
    def mods():
        ScreenManager.navigate_to_screen("mods")
    
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
        
        title_art = ToArtConverter.text_to_art(self._locale_manager['interface.main_menu.title'])
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        menu_x = self.get_w() // 2 - 2
        menu_y = self.title.y + self.title.height + 1
        
        self.menu = Menu(menu_x, menu_y, paddings=(1, 1, 1, 1), gap=2)
        self.add_child(self.menu)
        
        self.menu.add_items([
            ((self._locale_manager['interface.main_menu.continue_game'], Color.WHITE), Keys.Q, lambda: MainScene.continue_game()),
            ((self._locale_manager['interface.main_menu.new_game'], Color.WHITE), Keys.N, lambda: MainScene.new_game()),
            ((self._locale_manager['interface.main_menu.load_game'], Color.WHITE), Keys.L, lambda: MainScene.load_game()),
            ((self._locale_manager['interface.main_menu.settings'], Color.WHITE), Keys.S, lambda: MainScene.settings()),
            ((self._locale_manager['interface.main_menu.controls'], Color.WHITE), Keys.C, lambda: MainScene.controls()),
            ((self._locale_manager['interface.main_menu.mods'], Color.WHITE), Keys.M, lambda: MainScene.mods()),
            ((self._locale_manager['interface.main_menu.exit'], Color.WHITE), Keys.Q, lambda: MainScene.exit()),
        ])
        
        self.menu.set_selection(0)
        self.menu.set_active(True)
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    f"↑↓: {self._locale_manager['interface.bottom.navigation']}, " + \
                    f"Enter: {self._locale_manager['interface.bottom.enter']}, " + \
                    f"F1: {self._locale_manager['interface.bottom.performance_monitor']}", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.help_panel)
        
        