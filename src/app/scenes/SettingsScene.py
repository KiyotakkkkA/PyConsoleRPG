from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel, DialogWindow
from src.services.frontend.ui.general import Text, Menu
from src.services.output import Color
from src.services.events import Keys
from src.services.utils import ToArtConverter

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
        self.with_redirect_to_dialog_window_preset(f"{self._locale_manager['interface.dialog_window.return_to_main_menu']}?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW)
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art(self._locale_manager['interface.settings.title'])
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        menu_x = self.get_w() // 2 - 2
        menu_y = self.title.y + self.title.height + 1
        
        self.menu = Menu(menu_x, menu_y, paddings=(1, 1, 1, 1), gap=2)
        self.add_child(self.menu)
        
        self.menu.add_items([
            ((self._locale_manager['interface.settings.graphic'], Color.WHITE), Keys.G, self.to_setting_graphic),
            ((self._locale_manager['interface.settings.audio'], Color.WHITE), Keys.A, self.to_setting_audio),
            ((self._locale_manager['interface.settings.language'], Color.WHITE), Keys.L, self.to_setting_language),
        ])
        
        self.menu.set_selection(0)
        self.menu.set_active(True)
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    f"↑↓: {self._locale_manager['interface.bottom.navigation']}, " + \
                    f"Enter: {self._locale_manager['interface.bottom.enter']}, " + \
                    f"Esc: {self._locale_manager['interface.bottom.back']}, " + \
                    f"F1: {self._locale_manager['interface.bottom.performance_monitor']}", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.help_panel)
        
    def to_setting_audio(self):
        from src.Game import Game
        Game.screen_manager.navigate_to_screen("audio_settings")
        
    def to_setting_graphic(self):
        from src.Game import Game
        Game.screen_manager.navigate_to_screen("graphic_settings")
        
    def to_setting_language(self):
        from src.Game import Game
        Game.screen_manager.navigate_to_screen("lang_settings")
        
    def update(self):
        pass
        
        