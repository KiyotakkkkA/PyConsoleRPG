from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel, DialogWindow
from src.services.frontend.ui.general import Text, Button
from src.services.frontend.ui.input import Input
from src.services.events import Keys
from src.services.output import Color
from src.services.utils import ToArtConverter
import os

class NewGameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_in_dialog = False
        self.is_mounted = False
        
        self.new_player_data = {
            'name': None
        }
        
        self.components_order = [
            self.name_input,
            self.new_game_button
        ]
        self.current_component_index = 0
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.ESCAPE, self.ask_to_return)
        self.bind_key(Keys.UP, self.move_up)
        self.bind_key(Keys.DOWN, self.move_down)
        
    def flush_fields(self):
        self.name_input.flush()
        
    def before_mount(self):
        
        self.new_player_data = {
            'name': None
        }
        
        self.flush_fields()
        
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
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        title_art = ToArtConverter.text_to_art("Новая игра")
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text="Вернуться в главное меню?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
    
        error_window_width = 20
        self.error_window = DialogWindow(x=self.get_w() // 2 - error_window_width // 2,
                                          y=self.get_h() // 2 - 25,
                                          width=error_window_width,
                                          height=7,
                                          text="",
                                          ctype="OK",
                                          text_color=Color.BRIGHT_RED)

        panel_w = 70
        panel_h = 8
        self.menu_panel = Panel(x=(self.get_w() - panel_w) // 2,
                                y=(self.get_h() - panel_h) // 2 - 10,
                                width=panel_w,
                                height=panel_h,
                                title="",
                                border_color=Color.WHITE,
                                title_color=Color.YELLOW)
        self.add_child(self.menu_panel)
        
        input_x = self.menu_panel.x + 3
        input_y = self.menu_panel.y + 2
        
        self.name_input = Input(x=input_x,
                                y=input_y,
                                width=self.menu_panel.width - 6,
                                label_title="Введите имя персонажа: ",
                                label_color=Color.BRIGHT_BLACK,
                                label_selected_color=Color.BRIGHT_YELLOW,
                                label_active_color=Color.YELLOW,
                                input_color=Color.WHITE,
                                input_selected_color=Color.BRIGHT_WHITE,
                                input_active_color=Color.BRIGHT_WHITE,
                                enter_type="text",
                                enter_data_event_name="enter_name",
                                solo_key_brackets="br_none",
                                end_symbol="_",
                                max_length=15)
        
        
        self.new_game_button = Button(x=input_x,
                                      y=input_y + self.name_input.height + 2,
                                      width=1,
                                      text="[Начать игру]",
                                      action=self.new_game,
                                      fg_color=Color.BRIGHT_BLACK,
                                      bg_color=Color.RESET,
                                      selected_color=Color.BRIGHT_GREEN,
                                      selected_bg_color=Color.RESET,
                                      need_selection=True)
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Enter: Выбрать, Esc: Назад, F1: Монитор производительности", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.name_input)
        self.add_child(self.new_game_button)
        self.add_child(self.help_panel)
        
        self.on_event("enter_name", self.enter_name_event)
        
    def validate_data_name(self, name: str):
        from src.Game import Game
        
        if not name:
            return {
                'status': False,
                'message': 'Введите имя персонажа'
            }
        if os.path.exists(f"{Game.SAVES_DIR}/{name}"):
            return {
                'status': False,
                'message': 'Сохранение с таким именем уже существует'
            }
        return {
            'status': True,
            'message': 'Данные валидны'
        }
        
    def validate_data(self):
        validation = self.validate_data_name(self.new_player_data['name'])
        if not validation['status']:
            return validation
        return {
            'status': True,
            'message': 'Данные валидны'
        }
    
    def new_game(self):
        from src.Game import Game
        
        validation = self.validate_data()
        if not validation['status']:
            self.error_window.set_text(validation['message'])
            self.error_window.set_active(True)
            self.add_child(self.error_window)
            
            self.error_window.bind_yes(self.dialog_accept_error)
            self.new_game_button.set_selected(False)
            return
        
        self.emit_event("new_game_was_created", {'save_name': self.new_player_data['name']})
        Game.new_game(self.new_player_data)
    
    def enter_name_event(self, data):
        self.new_player_data['name'] = data['value']
        self.name_input.set_selected(True)
        
    def ask_to_return(self):
        if self.is_in_dialog: return
        
        self.is_in_dialog = True
        
        self.add_child(self.dialog_window)
        self.dialog_window.set_active(True)
        
        self.dialog_window.bind_yes(self.dialog_return_to_menu)
        self.dialog_window.bind_no(self.dialog_close_dialog)
    
    def dialog_return_to_menu(self):
        from src.Game import Game
        
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        Game.screen_manager.navigate_to_screen('main')
            
    def dialog_close_dialog(self):
        self.dialog_window.set_active(False)
        self.unbind_child(self.dialog_window)
        self.is_in_dialog = False
        
    def dialog_accept_error(self):
        self.error_window.set_active(False)
        self.unbind_child(self.error_window)
        self.is_in_dialog = False
        self.new_game_button.set_selected(True)
        
    def on_mount(self):
        self.components_order[self.current_component_index].set_active(True)
        self.is_mounted = True
        
    def update(self):
        if not self.is_mounted:
            self.on_mount()