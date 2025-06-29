from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel, Table
from src.services.frontend.ui.general import Text
from src.services.events import Keys
from src.services.output import Color
from src.services.utils import ToArtConverter
from src.services.backend.managers import ContentManager

class ModsScene(Screen):
    
    _content_manager = ContentManager.get_instance()
    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_mounted = False
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.with_redirect_to_dialog_window_preset(f"{self._locale_manager['interface.dialog_window.return_to_main_menu']}?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW)
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art(f"{self._locale_manager['interface.mods.title']}")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        self.saves_table = Table(10, 12, self.get_w() - 20, [
            self._locale_manager['interface.mods.table.mod_name'],
            self._locale_manager['interface.mods.table.mod_author'],
            self._locale_manager['interface.mods.table.mod_version'],
            self._locale_manager['interface.mods.table.mod_status'],
        ], [
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
        ], Alignment.CENTER, Alignment.LEFT, add_numeration=True, max_rows=5)
        
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    f"↑↓: {self._locale_manager['interface.bottom.navigation']}, " + \
                    f"Esc: {self._locale_manager['interface.bottom.back']}, " + \
                    f"F1: {self._locale_manager['interface.bottom.performance_monitor']}", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.saves_table)
        self.saves_table.set_active(False)
        
        self.add_child(self.help_panel)
        
        self.find_mods()
        
    def find_mods(self):
        content = self._content_manager.get_content()
        
        _mods = []
        _colors = []
        _keys = []
        
        for mod in content:
            _keys.append(mod['name'])
            _mods.append([
                mod['name'],
                mod['author'],
                mod['version'],
                f"[{self._locale_manager['interface.mods.table.mod_status.enabled']}]"
            ])
            _colors.append([
                (Color.WHITE, Color.RESET),
                (Color.WHITE, Color.RESET),
                (Color.WHITE, Color.RESET),
                (Color.WHITE, Color.RESET),
                (Color.BRIGHT_GREEN, Color.RESET),
            ])
        
        self.saves_table.set_rows(_keys, _mods, _colors)
    
    def update(self):
        pass