from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel, DialogWindow
from src.services.frontend.ui.general import Text
from src.services.frontend.ui.input import Selector
from src.services.output import Color
from src.services.events import Keys
from src.services.utils import ToArtConverter

class LangSettingScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_mounted = False
        
        self.components_order = [
            self.lang_selector,
        ]
        self.current_component_index = 0
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.UP, self.move_up)
        self.bind_key(Keys.DOWN, self.move_down)
        
    def move_up(self):
        if self.components_order[self.current_component_index].active: return
        
        self.components_order[self.current_component_index].set_selected(False)
        self.current_component_index = (self.current_component_index - 1) % len(self.components_order)
        self.components_order[self.current_component_index].set_selected(True)
        
    def move_down(self):
        if self.components_order[self.current_component_index].active: return
        
        self.components_order[self.current_component_index].set_selected(False)
        self.current_component_index = (self.current_component_index + 1) % len(self.components_order)
        self.components_order[self.current_component_index].set_selected(True)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.with_redirect_to_dialog_window_preset(f"{self._locale_manager['interface.dialog_window.return_back']}?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW, "settings")
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text=f"{self._locale_manager['interface.dialog_window.return_back']}?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
        
        title_art = ToArtConverter.text_to_art(self._locale_manager['interface.settings.lang_settings.title'])
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        self.settings_panel = Panel(self.get_w() // 3, self.title.y + self.title.height + 2, 80, 20, "", border_color=Color.BRIGHT_BLACK, title_color=Color.BRIGHT_BLACK)
        self.add_child(self.settings_panel)
        
        locales = self._locale_manager.get_all_locales_as_tuple()
        
        self.lang_selector = Selector(
            x=self.settings_panel.x + 4,
            y=self.settings_panel.y + 2,
            width=10,
            label_title=f"{self._locale_manager['interface.settings.lang_settings.lang_selector']}:",
            enter_data_event_name="lang_selector_event",
            selection_type="none-current-none",
            label_selected_color=Color.BRIGHT_YELLOW,
            label_active_color=Color.YELLOW,
            value_active_color=Color.BRIGHT_CYAN,
            options=locales)
        
        self.add_child(self.lang_selector)
        self.lang_selector.set_option(self._global_metadata_manager.get_value("current_lang", "ru"))
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    "↑↓: " + self._locale_manager['interface.bottom.navigation'] + ", " + \
                    "Enter: " + self._locale_manager['interface.bottom.enter'] + ", " + \
                    "Esc: " + self._locale_manager['interface.bottom.back'] + ", " + \
                    "F1: " + self._locale_manager['interface.bottom.performance_monitor'], Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.help_panel)
        
        self.on_event("lang_selector_event", self.set_global_meta_uphead)
        
    def set_global_meta_uphead(self, data: dict):
        self._global_metadata_manager.set_value('current_lang', data['value'])
        
        self.with_info_dialog_window_preset(
            f"{self._locale_manager['interface.info_window.lang_was_changed']}\n\n" + \
            f"{self._locale_manager['interface.info_window.need_to_reload']}", \
            (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7))
        
    def on_mount(self):
        self.components_order[self.current_component_index].set_selected(True)
        self.is_mounted = True
        
    def update(self):
        if not self.is_mounted:
            self.on_mount()
        
        