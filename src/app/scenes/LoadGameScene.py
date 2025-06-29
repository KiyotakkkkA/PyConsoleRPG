from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel, DialogWindow, Table
from src.services.frontend.ui.general import Text
from src.services.events import Keys
from src.services.output import Color
from src.services.utils import ToArtConverter
import os
import json
import time

class LoadGameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_mounted = False
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.X, self.ask_to_delete_save)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        self.with_redirect_to_dialog_window_preset(f"{self._locale_manager['interface.dialog_window.return_to_main_menu']}?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW)
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art(f"{self._locale_manager['interface.load_game.title']}")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        sure_to_delete_text = "Вы уверены, что хотите удалить это сохранение?"
        self.sure_to_delete_window = DialogWindow(x=self.get_w() // 2 - 20,
                                                  y=self.get_h() // 2 - 25,
                                                  width=40,
                                                  height=9,
                                                  text=sure_to_delete_text,
                                                  ctype="YES_NO",
                                                  text_color=Color.BRIGHT_RED)
        
        self.saves_table = Table(10, 12, self.get_w() - 20, [
            self._locale_manager['interface.load_game.table.character'],
            self._locale_manager['interface.load_game.table.level'],
            self._locale_manager['interface.load_game.table.save_date'],
        ], [
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
        ], Alignment.CENTER, Alignment.LEFT, add_numeration=True, max_rows=5)
        
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    f"↑↓: {self._locale_manager['interface.bottom.navigation']}, " + \
                    f"Enter: {self._locale_manager['interface.bottom.load']}, " + \
                    f"Esc: {self._locale_manager['interface.bottom.back']}, " + \
                    f"F1: {self._locale_manager['interface.bottom.performance_monitor']}, " + \
                    f"X: {self._locale_manager['interface.bottom.delete_save']}", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.saves_table)
        self.saves_table.set_active(True)
        
        self.add_child(self.help_panel)
        
        self.find_saves()
        
    def find_saves(self):
        from src.Game import Game
        
        _data = {}
        
        for save in os.listdir(Game.SAVES_DIR):
            if not os.path.isdir(f"{Game.SAVES_DIR}/{save}"): continue
            
            for file in os.listdir(f"{Game.SAVES_DIR}/{save}"):
                if file == 'meta.json':
                    with open(f"{Game.SAVES_DIR}/{save}/meta.json", 'r', encoding='utf-8') as f:
                        _data[save] = json.load(f)
        
        _saves = []
        _colors = []
        _actions = []
        _keys = []
        
        for save in _data:
            _keys.append(save)
            _saves.append([
                save,
                str(_data[save]['player_level']),
                time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(_data[save]['last_save_time'])),
            ])
            _colors.append([
                (Color.WHITE, Color.RESET),
                (Color.WHITE, Color.RESET),
                (Color.WHITE, Color.RESET),
                (Color.BRIGHT_BLACK, Color.RESET),
            ])
            _actions.append(lambda save=save: self.load_game(save))
        
        self.saves_table.set_rows(_keys, _saves, _colors, _actions)
        
    def load_game(self, save_name: str):
        from src.Game import Game
        Game.CURRENT_LOADING_PLAYER = save_name
        if Game.load():
            self.emit_event("game_was_loaded", {'save_name': save_name})
            Game.screen_manager.navigate_to_screen("game")
        
    def ask_to_delete_save(self):        
        if self.is_in_dialog: return
        
        self.is_in_dialog = True
        
        self.add_child(self.sure_to_delete_window)
        self.sure_to_delete_window.set_active(True)
        
        data = self.saves_table.get_selected_row_data()
        if data:
            self.sure_to_delete_window.set_text(
                self._locale_manager['interface.dialog_window.are_you_ready_to_delete'] + "\n\n" + \
                self._locale_manager['interface.dialog_window.next_char_will_be_deleted'] + ":\n\n" + \
                f"[{data[1]}]"
            )
        
        self.sure_to_delete_window.bind_yes(self.dialog_delete_save)
        self.sure_to_delete_window.bind_no(self.dialog_close_delete_save)
        
    def dialog_delete_save(self):
        from src.Game import Game
        if Game.delete_save(self.saves_table.get_selected_row_data()[1]):
            self.sure_to_delete_window.set_active(False)
            self.unbind_child(self.sure_to_delete_window)
            self.is_in_dialog = False
            self.find_saves()
        
    def dialog_close_delete_save(self):
        self.sure_to_delete_window.set_active(False)
        self.unbind_child(self.sure_to_delete_window)
        self.is_in_dialog = False
        
    def update(self):
        pass