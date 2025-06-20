from src.services.frontend.core import Screen, Alignment, AudioManager
from src.services.frontend.ui.containers import Panel, DialogWindow
from src.services.frontend.ui.general import Text
from src.services.frontend.ui.input import Selector
from src.services.output import Color
from src.services.events import Keys
from src.services.utils import ToArtConverter
import json

class AudioSettingScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_in_dialog = False
        self.is_mounted = False
        
        self.components_order = [
            self.bg_music_volume_selector,
        ]
        self.current_component_index = 0
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.ESCAPE, self.ask_to_return_to_settings)
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
        self.audio_manager = AudioManager.get_instance()
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text="Вернуться назад?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
        
        title_art = ToArtConverter.text_to_art("Настройка звука")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        self.settings_panel = Panel(self.get_w() // 3, self.title.y + self.title.height + 2, 80, 20, "", border_color=Color.BRIGHT_BLACK, title_color=Color.BRIGHT_BLACK)
        self.add_child(self.settings_panel)
        
        self.bg_music_volume_selector = Selector(
            x=self.settings_panel.x + 4,
            y=self.settings_panel.y + 2,
            width=10,
            label_title="Громкость музыки на заднем фоне",
            enter_data_event_name="bg_music_volume_selector_event",
            selection_type="minus-current-plus",
            label_selected_color=Color.BRIGHT_YELLOW,
            label_active_color=Color.YELLOW,
            min_value=0,
            max_value=10,
        )
        self.add_child(self.bg_music_volume_selector)
        
        self.bg_music_volume_selector.set_value(self.audio_manager.get_current_music_multiplier_as_int())
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Enter: Выбрать, Esc: Назад, F1: Монитор производительности", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.help_panel)
        
        self.on_event("bg_music_volume_selector_event", self.set_music_multiplier)
        
    def set_global_meta_uphead(self, data: dict):
        from src.Game import Game
        import json
    
        _dir = Game.SAVES_DIR
        try:
            with open(f"{_dir}/global.json", "r") as f:
                current_meta = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current_meta = {}

        current_meta['current_music_multiplier'] = data['value'] / 10
    
        with open(f"{_dir}/global.json", "w") as f:
            json.dump(current_meta, f)
        
    def set_music_multiplier(self, data: dict):
        self.audio_manager.apply_music_volume_multiplier(data['value'] / 10)
        self.set_global_meta_uphead(data)
        self.bg_music_volume_selector.set_active(False)
        self.bg_music_volume_selector.set_selected(True)
    
    def ask_to_return_to_settings(self):
        if self.is_in_dialog: return
        
        self.is_in_dialog = True
        
        self.add_child(self.dialog_window)
        self.dialog_window.set_active(True)
        
        self.dialog_window.bind_yes(self.dialog_return_to_settings)
        self.dialog_window.bind_no(self.dialog_close_dialog_return_to_settings)
        
    def dialog_return_to_settings(self):
        from src.Game import Game
        
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        Game.screen_manager.navigate_to_screen('settings')

    def dialog_close_dialog_return_to_settings(self):
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        
    def on_mount(self):
        self.components_order[self.current_component_index].set_selected(True)
        self.is_mounted = True
        
    def update(self):
        if not self.is_mounted:
            self.on_mount()
        
        