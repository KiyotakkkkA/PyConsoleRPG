from src.services.frontend.core import Screen, Alignment
from src.services.frontend.ui.containers import Panel
from src.services.frontend.ui.general import Text, Button
from src.services.frontend.ui.input import Input, Selector
from src.services.events import Keys
from src.services.output import Color
from src.services.utils import ToArtConverter
import os

class NewGameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True

        self.is_mounted = False
        
        self.new_player_data = {
            'name': None,
            'race': None
        }
        
        self.components_order = [
            self.name_input,
            self.race_selector,
            self.new_game_button
        ]
        self.current_component_index = 0
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.UP, self.move_up)
        self.bind_key(Keys.DOWN, self.move_down)
        
    def flush_fields(self):
        self.name_input.flush()
        self.race_name_text.set_text(self._locale_manager['interface.new_game.race_name_text_not_selected'])
        self.race_desc_text.set_text("")
        
        for char in self._chars:
            getattr(self, f"race_{char}_value_text").set_text(self._locale_manager['interface.new_game.race_name_text_not_selected'])
            getattr(self, f"race_{char}_value_text").set_fg_color(Color.BRIGHT_BLACK)
        
    def before_mount(self):
        
        self.new_player_data = {
            'name': None,
            'race': None
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
        
    def set_characteristics_panel(self):
        
        self._chars = {
            'constitution': self._locale_manager['characteristics.constitution'],
            'intelligence': self._locale_manager['characteristics.intelligence'],
            'endurance': self._locale_manager['characteristics.endurance']
        }
        
        characteristics_panel_width = 50
        characteristics_panel_height = self.get_h() - 5
        self.characteristics_panel = Panel(self.get_w() - characteristics_panel_width - 3, 2, characteristics_panel_width, characteristics_panel_height, f" {self._locale_manager['interface.new_game.panel_chars_title']} ", border_color=Color.BRIGHT_BLACK, title_color=Color.YELLOW)
        
        y = self.characteristics_panel.y + 1
        
        for char in self._chars:
            race_addition_text_x = self.characteristics_panel.x + 2
            race_addition_text_y = y
            race_name_text_x = race_addition_text_x + len('[*] ')
            race_name_text_y = race_addition_text_y
            race_char_value_x = race_name_text_x + len(f"{self._chars[char]}: ")
            race_char_value_y = race_name_text_y
            
            setattr(self, f"race_{char}_addition_text", Text(race_addition_text_x, race_addition_text_y, "[*] ", Color.CYAN, Color.RESET))
            setattr(self, f"race_{char}_name_text", Text(race_name_text_x, race_name_text_y, f"{self._chars[char]}: ", Color.RESET, Color.RESET))
            setattr(self, f"race_{char}_value_text", Text(race_char_value_x, race_char_value_y, self._locale_manager['interface.new_game.race_name_text_not_selected'], Color.BRIGHT_BLACK, Color.RESET))
            
            self.characteristics_panel.add_child(getattr(self, f"race_{char}_addition_text"))
            self.characteristics_panel.add_child(getattr(self, f"race_{char}_name_text"))
            self.characteristics_panel.add_child(getattr(self, f"race_{char}_value_text"))
            
            y += 1
        
        self.add_child(self.characteristics_panel)
        
    def set_description_panel(self):
        description_panel_width = 50
        description_panel_height = self.get_h() - 5
        self.description_panel = Panel(3, 2, description_panel_width, description_panel_height, f" {self._locale_manager['interface.new_game.panel_desc_title']} ", border_color=Color.BRIGHT_BLACK, title_color=Color.YELLOW)
        
        race_info_text_x = self.description_panel.x + 2
        race_info_text_y = self.description_panel.y + 1
        race_name_text_x = race_info_text_x + 6
        race_name_text_y = race_info_text_y
        race_desc_text_x = race_info_text_x
        race_desc_text_y = race_info_text_y + 1
        
        
        self.race_info_text = Text(race_info_text_x, race_info_text_y, self._locale_manager['interface.new_game.race_info_text'], Color.BRIGHT_YELLOW, Color.RESET)
        self.race_name_text = Text(race_name_text_x, race_name_text_y, self._locale_manager['interface.new_game.race_name_text_not_selected'], Color.RESET, Color.RESET)
        self.race_desc_text = Text(race_desc_text_x, race_desc_text_y, "", Color.BRIGHT_BLACK, Color.RESET, auto_break=True, max_width=description_panel_width - race_info_text_x - 4)
        
        self.description_panel.add_child(self.race_info_text)
        self.description_panel.add_child(self.race_name_text)
        self.description_panel.add_child(self.race_desc_text)
        
        self.add_child(self.description_panel)
        
    def update_race(self, data: dict = None):
        from src.services.backend.registers import RegistryRace
        
        race = RegistryRace.get_instance().get_json_view()[data['value']]
        
        self.new_player_data['race'] = race['id']
        
        self.race_name_text.set_text(race['name'])
        self.race_desc_text.set_text(race['description'])
        
        for char in self._chars:
            value_text = getattr(self, f"race_{char}_value_text")
            value_text.set_text(str(race['race_chars'][char]))
            value_text.set_fg_color(self.pick_char_value_color(race['race_chars'][char]))
            
    def pick_char_value_color(self, char_value: int):
        if char_value < 10:
            return Color.BRIGHT_RED
        elif char_value == 10:
            return Color.BRIGHT_YELLOW
        else:
            return Color.BRIGHT_GREEN
        
    def init(self):
        from src.services.backend.registers import RegistryRace
        
        self.with_redirect_to_dialog_window_preset(f"{self._locale_manager['interface.dialog_window.return_to_main_menu']}?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW)
        
        self.main_panel = Panel(1, 1, self.get_w() - 2, self.get_h() - 2, "", border_color=Color.WHITE, title_color=Color.YELLOW)
        self.add_child(self.main_panel)
        
        self.set_description_panel()
        self.set_characteristics_panel()
        
        title_art = ToArtConverter.text_to_art(self._locale_manager['interface.new_game.title'])
        title_x = self.get_w() // 2 - len(title_art[0]) // 2 + 1
        title_y = self.get_h() // 10
        
        self.title = Text(title_x, title_y, "\n".join(title_art), Color.BRIGHT_YELLOW, Color.RESET)
        self.add_child(self.title)

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
        
        name_input_x = self.menu_panel.x + 3
        name_input_y = self.menu_panel.y + 2
        
        self.name_input = Input(x=name_input_x,
                                y=name_input_y,
                                width=self.menu_panel.width - 6,
                                label_title=f"{self._locale_manager['interface.new_game.char_name_input']}:",
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
        
        race_selector_x = name_input_x
        race_selector_y = name_input_y + self.name_input.height + 1
        
        opts = []
        races = RegistryRace.get_instance().get_json_view()
        for race in races:
            opts.append((race, races[race]['name']))
        
        self.race_selector = Selector(
            x=race_selector_x,
            y=race_selector_y,
            label_title=f"{self._locale_manager['interface.new_game.race_selector']}:",
            enter_data_event_name="race_selector_event",
            selection_type="none-current-none",
            label_color=Color.BRIGHT_BLACK,
            label_selected_color=Color.BRIGHT_YELLOW,
            label_active_color=Color.YELLOW,
            value_active_color=Color.BRIGHT_CYAN,
            options=opts)
        
        button_x = race_selector_x
        button_y = race_selector_y + self.race_selector.height + 1
        
        self.new_game_button = Button(x=button_x,
                                      y=button_y,
                                      width=1,
                                      text=f"[{self._locale_manager['interface.new_game.new_game_button']}]",
                                      action=self.new_game,
                                      fg_color=Color.BRIGHT_BLACK,
                                      bg_color=Color.RESET,
                                      selected_color=Color.BRIGHT_GREEN,
                                      selected_bg_color=Color.RESET,
                                      need_selection=True)
        
        self.help_panel_height = 3
        self.help_panel_w = self.get_w() - 2
        self.help_panel = Panel(1, self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, 
                    f"↑↓: {self._locale_manager['interface.bottom.navigation']}, " + \
                    f"Enter: {self._locale_manager['interface.bottom.enter']}, " + \
                    f"Esc: {self._locale_manager['interface.bottom.back']}, " + \
                    f"F1: {self._locale_manager['interface.bottom.performance_monitor']}", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
        self.add_child(self.name_input)
        self.add_child(self.race_selector)
        self.add_child(self.new_game_button)
        self.add_child(self.help_panel)
        
        self.on_event("enter_name", self.enter_name_event)
        self.on_event("race_selector_event", self.update_race)
        
    def validate_data_name(self, name: str):
        from src.Game import Game
        
        if not name:
            return {
                'status': False,
                'message': self._locale_manager['interface.error_window.empty_name']
            }
        if os.path.exists(f"{Game.SAVES_DIR}/{name}"):
            return {
                'status': False,
                'message': self._locale_manager['interface.error_window.character_already_exists']
            }
        return {
            'status': True,
            'message': 'Данные валидны'
        }
        
    def validate_data_race(self, race: str):
        if not race:
            return {
                'status': False,
                'message': self._locale_manager['interface.error_window.empty_race']
            }
        return {
            'status': True,
            'message': 'Данные валидны'
        }
        
    def validate_data(self):
        validation_name = self.validate_data_name(self.new_player_data['name'])
        if not validation_name['status']:
            return validation_name
        
        validation_race = self.validate_data_race(self.new_player_data['race'])
        if not validation_race['status']:
            return validation_race
        
        return {
            'status': True,
            'message': 'Данные валидны'
        }
    
    def new_game(self):
        from src.Game import Game
        
        validation = self.validate_data()
        if not validation['status']:
            self.with_error_dialog_window_preset(
                text=validation['message'],
                pos=(self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25),
                size=(40, 7)
            )
            return
        
        self.emit_event("new_game_was_created", {'save_name': self.new_player_data['name']})
        Game.new_game(self.new_player_data)
    
    def enter_name_event(self, data):
        self.new_player_data['name'] = data['value']
        self.name_input.set_selected(True)
        
    def on_mount(self):
        self.components_order[self.current_component_index].set_active(True)
        self.is_mounted = True
        
    def update(self):
        if not self.is_mounted:
            self.on_mount()