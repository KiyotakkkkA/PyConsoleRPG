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
        
        self.is_in_dialog = False
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.ESCAPE, self.ask_to_return)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text="Вернуться в главное меню?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
        
        title_art = ToArtConverter.text_to_art("Настройки")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        menu_x = self.get_w() // 2 - 2
        menu_y = self.title.y + self.title.height + 1
        
        self.menu = Menu(menu_x, menu_y, paddings=(1, 1, 1, 1), gap=2)
        self.add_child(self.menu)
        
        self.menu.add_items([
            (("Графика", Color.WHITE), Keys.G, self.to_setting_graphic),
            (("Звук", Color.WHITE), Keys.A, self.to_setting_audio),
            (("Язык", Color.WHITE), Keys.L, self.to_setting_language),
        ])
        
        self.menu.set_selection(0)
        self.menu.set_active(True)
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Enter: Выбрать, Esc: Назад, F1: Монитор производительности", Color.BRIGHT_BLACK, Color.RESET)
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
        Game.screen_manager.navigate_to_screen("language_settings")
    
    def ask_to_return(self):
        if self.is_in_dialog: return
        
        self.is_in_dialog = True
        
        self.add_child(self.dialog_window)
        self.dialog_window.set_active(True)
        
        self.dialog_window.bind_yes(self.dialog_return_to_menu)
        self.dialog_window.bind_no(self.dialog_close_dialog_return_to_menu)
        
    def dialog_return_to_menu(self):
        from src.Game import Game
        
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        Game.screen_manager.navigate_to_screen('main')
            
    def dialog_close_dialog_return_to_menu(self):
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        
    def update(self):
        pass
        
        