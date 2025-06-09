from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel, Tab, DialogWindow, Table
from src.services.frontend.ui.general import Text, Menu, SeparatorItem
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color
import time

class GameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.is_in_dialog = False
        
        self.temp_items_activities = []
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.LEFT, self.to_control_panel)
        self.bind_key(Keys.RIGHT, self.to_main_panel)
        self.bind_key(Keys.ESCAPE, self.ask_to_exit)
        
    def game_collect_resource(self, resource_id: str):
        """
        Сбор ресурсов
        
        Args:
            resource_id: ID ресурса
        """
        from src.Game import Game
        Game.player.collect_resource(resource_id)
        
        self.control_activities.set_selection(0)
        
    def game_move_to_location(self, location_id: str):
        """
        Перемещение игрока в указанную локацию
        
        Args:
            location_id: ID локации
        """
        from src.Game import Game
        if Game.game_state['current_relax_time'] > 0: return
        Game.game_state['start_time'] = time.time()
        Game.game_state['frame_count'] = 0
        
        Game.player.move_to_location(location_id)
        Game.game_state['current_relax_time'] = Game.player.get_location_relax_time()
        
        self.control_activities.set_selection(0)
    
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def to_control_panel(self):
        """Переключение активной корневой панели"""
        if self.is_in_dialog: return
        self.main_panel.selected = False
        self.action_panel.selected = True
        self.control_activities.is_active = True
        self.control_activities.set_selection(0)
        self.inventory_table.set_active(False)
        
        # перебиндинг клавиш
        self.unbind_key(Keys.UP, self.inventory_table.move_up)
        self.unbind_key(Keys.DOWN, self.inventory_table.move_down)
        
        self.control_activities.bind_key(Keys.UP, self.control_activities.move_up)
        self.control_activities.bind_key(Keys.DOWN, self.control_activities.move_down)
        
    def to_main_panel(self):
        """Переключение активной корневой панели"""
        if self.is_in_dialog: return
        self.main_panel.selected = True
        self.action_panel.selected = False
        self.control_activities.is_active = False
        self.control_activities.flush_selection()
        self.inventory_table.set_active(True)
        
        # перебиндинг клавиш
        self.control_activities.unbind_key(Keys.UP, self.control_activities.move_up)
        self.control_activities.unbind_key(Keys.DOWN, self.control_activities.move_down)
        
        self.bind_key(Keys.UP, self.inventory_table.move_up)
        self.bind_key(Keys.DOWN, self.inventory_table.move_down)
        
    def set_control_panel(self): # Панель навигации
        control_panel_w = self.get_w() // 5
        self.control_panel = Panel(0, 0, control_panel_w, self.get_h(), " НАВИГАЦИЯ ", " ", Alignment.CENTER, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        
        actions_panel_y = self.control_panel.y + 2
        self.action_panel = Panel(x=self.control_panel.x + 1,
                              y=actions_panel_y,
                              width=self.control_panel.width - 4,
                              height=1,
                              title=" Действия ",
                              filler=" ",
                              title_alignment=Alignment.LEFT,
                              border_color=Color.BRIGHT_BLACK,
                              border_color_selected=Color.BRIGHT_YELLOW,
                              title_color=Color.YELLOW,
                              auto_resize=True)
        
        self.control_activities = Menu(x=self.action_panel.x + 1,
                                       y=self.action_panel.y,
                                       inactive_menu_color=Color.BRIGHT_BLACK,
                                       active_menu_color=Color.BRIGHT_WHITE,
                                       alignment=Alignment.LEFT,
                                       gap=1)
        
        self.player_panel_y = self.action_panel.y + self.action_panel.height + 1
        self.player_panel = Panel(self.action_panel.x,
                                  self.player_panel_y,
                                  self.action_panel.width,
                                  10,
                                  " Персонаж ",
                                  " ",
                                  Alignment.LEFT,
                                  border_color=Color.BRIGHT_BLACK,
                                  border_color_selected=Color.BRIGHT_YELLOW,
                                  title_color=Color.YELLOW)
        
        self.relax_time = Text(self.player_panel.x + 2, self.player_panel.height - 1, "Отдых {}", Color.BRIGHT_BLACK, Color.RESET)
        
        self.player_level_addition = Text(self.player_panel.x + 2, self.player_panel.y + 2, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.player_level_label = Text(self.player_level_addition.x + self.player_level_addition.width + 1, self.player_panel.y, "Уровень:", Color.WHITE, Color.RESET)
        self.player_level = Text(self.player_level_label.x + self.player_level_label.width + 1, self.player_panel.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        
        self.player_exp_to_next_level_addition = Text(self.player_panel.x + 2, self.player_panel.y + 3, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.player_exp_to_next_level_label = Text(self.player_exp_to_next_level_addition.x + self.player_exp_to_next_level_addition.width + 1, self.player_panel.y, "До повышения:", Color.WHITE, Color.RESET)
        self.player_current_exp = Text(self.player_exp_to_next_level_label.x + self.player_exp_to_next_level_label.width + 1, self.player_panel.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        self.player_exp_to_next_level = Text(self.player_current_exp.x + self.player_current_exp.width + 1, self.player_panel.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        
        self.player_health_addition = Text(self.player_panel.x + 2, self.player_panel.y + 4, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.player_health_label = Text(self.player_health_addition.x + self.player_health_addition.width + 1, self.player_panel.y, "Здоровье:", Color.WHITE, Color.RESET)
        self.player_health_max = Text(self.player_health_label.x + self.player_health_label.width + 1, self.player_panel.y, "", Color.BRIGHT_RED, Color.RESET)
        self.player_health = Text(self.player_health_max.x + self.player_health_max.width + 1, self.player_panel.y, "", Color.BRIGHT_RED, Color.RESET)
        
        self.player_energy_addition = Text(self.player_panel.x + 2, self.player_panel.y + 6, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.player_energy_label = Text(self.player_energy_addition.x + self.player_energy_addition.width + 1, self.player_panel.y, "Энергия:", Color.WHITE, Color.RESET)
        self.player_energy_max = Text(self.player_energy_label.x + self.player_energy_label.width + 1, self.player_panel.y, "", Color.BRIGHT_GREEN, Color.RESET)
        self.player_energy = Text(self.player_energy_max.x + self.player_energy_max.width + 1, self.player_panel.y, "", Color.BRIGHT_GREEN, Color.RESET)
        
        self.player_astrum_addition = Text(self.player_panel.x + 2, self.player_panel.y + 8, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.player_astrum_label = Text(self.player_astrum_addition.x + self.player_astrum_addition.width + 1, self.player_panel.y, "Аструм:", Color.WHITE, Color.RESET)
        self.player_astrum_max = Text(self.player_astrum_label.x + self.player_astrum_label.width + 1, self.player_panel.y, "", Color.BRIGHT_BLUE, Color.RESET)
        self.player_astrum = Text(self.player_astrum_max.x + self.player_astrum_max.width + 1, self.player_panel.y, "", Color.BRIGHT_BLUE, Color.RESET)
        
        self.control_panel.add_child(self.action_panel)
        self.action_panel.add_child(self.control_activities)
        self.control_panel.add_child(self.player_panel)
        
        self.player_panel.add_child(self.relax_time)
        
        self.player_panel.add_child(self.player_level_addition)
        self.player_panel.add_child(self.player_level_label)
        self.player_panel.add_child(self.player_level)
        
        self.player_panel.add_child(self.player_exp_to_next_level_addition)
        self.player_panel.add_child(self.player_exp_to_next_level_label)
        self.player_panel.add_child(self.player_current_exp)
        self.player_panel.add_child(self.player_exp_to_next_level)
        
        self.player_panel.add_child(self.player_health_addition)
        self.player_panel.add_child(self.player_health_label)
        self.player_panel.add_child(self.player_health_max)
        self.player_panel.add_child(self.player_health)
        
        self.player_panel.add_child(self.player_energy_addition)
        self.player_panel.add_child(self.player_energy_label)
        self.player_panel.add_child(self.player_energy_max)
        self.player_panel.add_child(self.player_energy)
        
        self.player_panel.add_child(self.player_astrum_addition)
        self.player_panel.add_child(self.player_astrum_label)
        self.player_panel.add_child(self.player_astrum_max)
        self.player_panel.add_child(self.player_astrum)
        
    def set_main_panel(self): # Основная панель
        main_panel_w = self.get_w() * 4 // 5
        self.main_panel = Panel(self.control_panel.get_width(), 0, main_panel_w, self.get_h(), "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        
    def set_help_panel(self): # Панель помощи
        self.help_panel_height = 3
        self.help_panel_w = self.main_panel.width
        self.help_panel = Panel(self.control_panel.get_width(), self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Tab: Переключение вкладок, Enter: Подтвердить, Esc: Назад, F1: Монитор производительности, ←→: Переключение активных панелей", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
    def set_connections_main(self): # Вкладка локации - Перемещения
        from src.Game import Game
        
        connections = []
        gap = 1
        conns = Game.game_state["current_location_data"]()["connections"]
        player_level = Game.player.current_level
        
        for connection in conns:
            
            errors: List[Text] = []
            
            reqs = {
                'level': {
                    'req': lambda req=conns[connection]['level']: req,
                    'complete': lambda req=conns[connection]['level']: not req or req <= player_level,
                    'error': lambda req=conns[connection]['level']: f"Необходим уровень: {req}"
                }
            }
            
            text = Text(self.main_connections.x + 1, self.main_connections.y + gap, conns[connection]["name"], Color.WHITE, Color.RESET)
            
            if not reqs['level']['complete']():
                errors.append(Text(self.main_connections.x + 1, self.main_connections.y + gap + 1, "  [!] " + reqs['level']['error'](), Color.BRIGHT_RED, Color.RESET))
            
            text.fg_color = Color.BRIGHT_BLACK if errors else Color.WHITE
            
            gap += len(errors) + 1
            
            connections.append(text)
            connections.extend(errors)
        
        self.main_connections.set_children(connections)
        
    def set_resources_main(self): # Вкладка локации - Ресурсы
        from src.Game import Game
        
        resources = []
        gap = 1
        res = Game.game_state["current_location_data"]()["resources"]
        player_level = Game.player.current_level
        
        for resource in res:
            
            errors: List[Text] = []
            
            reqs = {
                'level': {
                    'req': lambda req=res[resource]['level_need']: req,
                    'complete': lambda req=res[resource]['level_need']: not req or req <= player_level,
                    'error': lambda req=res[resource]['level_need']: f"Необходим уровень: {req}"
                }
            }
            
            amount = res[resource]['amount']
            
            text_name = Text(self.resources_panel.x + 1, self.resources_panel.y + gap, res[resource]["name"], Color.WHITE, Color.RESET)
            text_count = Text(text_name.x + text_name.width + 1, self.resources_panel.y + gap, f"[x{amount}]", Color.WHITE, Color.RESET)
            text_rarity = Text(text_count.x + text_count.width + 1, self.resources_panel.y + gap, f"[{res[resource]['rarity'].value[0]}]", res[resource]['rarity'].value[2], Color.RESET)
            
            if amount <= 0:
                errors.append(Text(self.resources_panel.x + 1, self.resources_panel.y + gap + 1, "  " + "ЗАКОНЧИЛСЯ", Color.BRIGHT_RED, Color.RESET))
            
            if not reqs['level']['complete']():
                errors.append(Text(self.resources_panel.x + 1, self.resources_panel.y + gap + 1, "  [!] " + reqs['level']['error'](), Color.BRIGHT_RED, Color.RESET))
            
            text_name.fg_color = Color.BRIGHT_BLACK if errors or amount <= 0 else Color.WHITE
            text_count.fg_color = Color.BRIGHT_BLACK if errors or amount <= 0 else Color.BRIGHT_YELLOW
            text_rarity.fg_color = Color.BRIGHT_BLACK if errors or amount <= 0 else res[resource]['rarity'].value[2]
            
            gap += len(errors) + 1
            
            resources.append(text_name)
            resources.append(text_count)
            resources.append(text_rarity)
            resources.extend(errors)
        
        if not resources:
            resources.append(Text(self.resources_panel.x + 1, self.resources_panel.y + 1, "Пусто...", Color.BRIGHT_BLACK, Color.RESET))
        
        self.resources_panel.set_children(resources)
        
    def set_connections_control(self): # Панель навигации - перемещения
        from src.Game import Game
        
        self.temp_items_activities = []
        data = Game.game_state["current_location_data"]()
        
        conns = data["connections"]
        
        player_level = Game.player.current_level
        
        for connection in conns:            
            reqs = {
                'level': {
                    'req': lambda req=conns[connection]['level']: req,
                    'complete': lambda req=conns[connection]['level']: not req or req <= player_level,
                }
            }
            if not reqs['level']['complete'](): continue
            self.temp_items_activities.append(((f"Идти в: {conns[connection]['name']}", Color.WHITE), None, lambda conn=conns[connection]['id']: self.game_move_to_location(conn)))
        
    def set_resources_control(self): # Панель навигации - ресурсы
        from src.Game import Game
        
        data = Game.game_state["current_location_data"]()
        _tmp = []
        
        res = data["resources"]
        player_level = Game.player.current_level
        
        start_len = len(self.temp_items_activities)
        
        for resource in res:
            reqs = {
                'level': {
                    'req': lambda req=res[resource]['level_need']: req,
                    'complete': lambda req=res[resource]['level_need']: not req or req <= player_level,
                }
            }
            if not reqs['level']['complete']() or res[resource]['amount'] <= 0: continue
            _tmp.append(((f"Собрать: {res[resource]['name']} [x{res[resource]['amount']}]", Color.WHITE), None, lambda res=resource: self.game_collect_resource(res)))
            
        end_len = len(self.temp_items_activities) + len(_tmp)
        
        if start_len != end_len:
            self.temp_items_activities.append((SeparatorItem("-", 0, Color.BRIGHT_BLACK), None, None))
        
        self.control_activities.set_items(self.temp_items_activities + _tmp)
        
    def set_player_panel(self): # Панель навигации - панель игрока
        from src.Game import Game
        
        self.player_panel.set_y(self.action_panel.y + self.action_panel.height)
        self.player_panel.set_height(self.control_panel.height - self.action_panel.height - 6)
        
        self.relax_time.set_y(self.player_panel.y + 1)
        if Game.game_state['current_relax_time'] > 0:
            self.relax_time.set_fg_color(Color.BRIGHT_RED)
            self.relax_time.set_text(f"| ПЕРЕМЕЩЕНИЕ - {float(Game.game_state['current_relax_time']):.2f} сек. |")
        else:
            self.relax_time.set_fg_color(Color.BRIGHT_GREEN)
            self.relax_time.set_text("| ГОТОВ К ПЕРЕМЕЩЕНИЮ |")
        
        level_y = self.player_panel.y + 3
        exp_y = level_y + 1
        health_y = exp_y + 2
        energy_y = health_y + 1
        astrum_y = energy_y + 1
        
        self.player_level_addition.set_y(level_y)
        self.player_level_label.set_y(level_y)
        self.player_level.set_y(level_y)
        self.player_level.set_text(f"{Game.player.current_level}")
        
        self.player_exp_to_next_level_addition.set_y(exp_y)
        self.player_exp_to_next_level_label.set_y(exp_y)
        self.player_current_exp.set_y(exp_y)
        self.player_current_exp.set_text(f"{Game.player.current_exp}")
        self.player_exp_to_next_level.set_y(exp_y)
        self.player_exp_to_next_level.set_x(self.player_current_exp.x + self.player_current_exp.width)
        self.player_exp_to_next_level.set_text(f"/ {Game.player.exp_to_next_level}")
        
        self.player_health_addition.set_y(health_y)
        self.player_health_label.set_y(health_y)
        self.player_health_max.set_y(health_y)
        self.player_health.set_y(health_y)
        self.player_health.set_text(f"{Game.player.health}")
        self.player_health_max.set_x(self.player_health.x + self.player_health.width)
        self.player_health_max.set_text(f"/ {Game.player.max_health}")
        
        self.player_energy_addition.set_y(energy_y)
        self.player_energy_label.set_y(energy_y)
        self.player_energy_max.set_y(energy_y)
        self.player_energy.set_y(energy_y)
        self.player_energy.set_text(f"{Game.player.energy}")
        self.player_energy_max.set_x(self.player_energy.x + self.player_energy.width)
        self.player_energy_max.set_text(f"/ {Game.player.max_energy}")
        
        self.player_astrum_addition.set_y(astrum_y)
        self.player_astrum_label.set_y(astrum_y)
        self.player_astrum_max.set_y(astrum_y)
        self.player_astrum.set_y(astrum_y)
        self.player_astrum.set_text(f"{Game.player.astrum}")
        self.player_astrum_max.set_x(self.player_astrum.x + self.player_astrum.width)
        self.player_astrum_max.set_text(f"/ {Game.player.max_astrum}")
        
        Game.time_count_with_fps()
        
    def set_tab_location(self): # Вкладка локации
        name_location_y = self.tab1.y + 3
        self.name_location = Text(self.tab1.x + 1, name_location_y, '', Color.WHITE, Color.RESET)
        
        name_region_y = name_location_y
        self.name_region = Text(self.name_location.x + self.name_location.width + 1, name_region_y, '', Color.BRIGHT_GREEN, Color.RESET)
        
        description_location_y = name_region_y + 2
        self.description_location = Text(self.tab1.x + 1, description_location_y, '', Color.BRIGHT_BLACK, Color.RESET)
        
        self.main_connections = Panel(x=self.tab1.x + 1,
                                y=description_location_y + 2,
                                width=self.tab1.width // 2,
                                height=10,
                                title="Все переходы:",
                                filler=" ",
                                title_alignment=Alignment.LEFT,
                                border_color=Color.BLACK,
                                border_color_selected=Color.BLACK,
                                title_color=Color.YELLOW)
        
        self.resources_panel = Panel(x=self.main_connections.x + self.main_connections.width + 2,
                                y=self.main_connections.y,
                                width=self.tab1.width // 2 - 3,
                                height=10,
                                title="Ресурсы на локации:",
                                filler=" ",
                                title_alignment=Alignment.LEFT,
                                border_color=Color.BLACK,
                                border_color_selected=Color.BLACK,
                                title_color=Color.YELLOW)
        
        self.tab1.add_child(self.name_location)
        self.tab1.add_child(self.name_region)
        self.tab1.add_child(self.description_location)
        self.tab1.add_child(self.main_connections)
        self.tab1.add_child(self.resources_panel)
        
    def set_tab_player(self):
        self.characteristics_panel = Panel(x=self.tab1.x + 1,
                          y=self.tab1.y + 3,
                          width=1,
                          height=self.tab1.height - 7,
                          title=" Характеристики ",
                          filler=" ",
                          title_alignment=Alignment.LEFT,
                          border_color=Color.BRIGHT_BLACK,
                          border_color_selected=Color.BRIGHT_BLACK,
                          title_color=Color.YELLOW)
        
        self.speed_characteristic_addition = Text(self.characteristics_panel.x + 2, self.characteristics_panel.y + 2, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.speed_characteristic = Text(self.speed_characteristic_addition.x + self.speed_characteristic_addition.width + 1, self.characteristics_panel.y + 2, "Скорость: ", Color.WHITE, Color.RESET)
        self.speed_characteristic_value = Text(self.speed_characteristic.x + self.speed_characteristic.width + 1, self.speed_characteristic.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        self.speed_description = Text(self.speed_characteristic_addition.x, self.speed_characteristic_value.y + 1, "- Увеличение этого параметра\nуменьшает время перезарядки перемещения", Color.BRIGHT_BLACK, Color.RESET)
        
        self.constitution_characteristic_addition = Text(self.characteristics_panel.x + 2, self.speed_description.y + 2, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.constitution_characteristic = Text(self.constitution_characteristic_addition.x + self.constitution_characteristic_addition.width + 1, self.speed_description.y + 2, "Телосложение: ", Color.WHITE, Color.RESET)
        self.constitution_characteristic_value = Text(self.constitution_characteristic.x + self.constitution_characteristic.width + 1, self.constitution_characteristic.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        self.constitution_description = Text(self.constitution_characteristic_addition.x, self.constitution_characteristic_value.y + 1, "- Увеличение этого параметра\nувеличивает максимальное здоровье", Color.BRIGHT_BLACK, Color.RESET)
        
        self.endurance_characteristic_addition = Text(self.characteristics_panel.x + 2, self.constitution_description.y + 2, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.endurance_characteristic = Text(self.endurance_characteristic_addition.x + self.endurance_characteristic_addition.width + 1, self.constitution_description.y + 2, "Выносливость: ", Color.WHITE, Color.RESET)
        self.endurance_characteristic_value = Text(self.endurance_characteristic.x + self.endurance_characteristic.width + 1, self.endurance_characteristic.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        self.endurance_description = Text(self.endurance_characteristic_addition.x, self.endurance_characteristic_value.y + 1, "- Увеличение этого параметра\nувеличивает максимальную энергию", Color.BRIGHT_BLACK, Color.RESET)
        
        self.intelligence_characteristic_addition = Text(self.characteristics_panel.x + 2, self.endurance_description.y + 2, "[*]", Color.BRIGHT_MAGENTA, Color.RESET)
        self.intelligence_characteristic = Text(self.intelligence_characteristic_addition.x + self.intelligence_characteristic_addition.width + 1, self.endurance_description.y + 2, "Интеллект: ", Color.WHITE, Color.RESET)
        self.intelligence_characteristic_value = Text(self.intelligence_characteristic.x + self.intelligence_characteristic.width + 1, self.intelligence_characteristic.y, "", Color.BRIGHT_YELLOW, Color.RESET)
        self.intelligence_description = Text(self.intelligence_characteristic_addition.x, self.intelligence_characteristic_value.y + 1, "- Увеличение этого параметра\nувеличивает максимальный запас аструма\n(астрального вещества,\nнеобходимого для сотворения заклинаний)", Color.BRIGHT_BLACK, Color.RESET)
        
        
        self.tab2.add_child(self.characteristics_panel)
        self.characteristics_panel.add_child(self.speed_characteristic_addition)
        self.characteristics_panel.add_child(self.speed_characteristic)
        self.characteristics_panel.add_child(self.speed_characteristic_value)
        self.characteristics_panel.add_child(self.speed_description)
        
        self.characteristics_panel.add_child(self.constitution_characteristic_addition)
        self.characteristics_panel.add_child(self.constitution_characteristic)
        self.characteristics_panel.add_child(self.constitution_characteristic_value)
        self.characteristics_panel.add_child(self.constitution_description)
        
        self.characteristics_panel.add_child(self.endurance_characteristic_addition)
        self.characteristics_panel.add_child(self.endurance_characteristic)
        self.characteristics_panel.add_child(self.endurance_characteristic_value)
        self.characteristics_panel.add_child(self.endurance_description)
        
        self.characteristics_panel.add_child(self.intelligence_characteristic_addition)
        self.characteristics_panel.add_child(self.intelligence_characteristic)
        self.characteristics_panel.add_child(self.intelligence_characteristic_value)
        self.characteristics_panel.add_child(self.intelligence_description)
        
    def set_tab_inventory(self):
        self.inventory_table = Table(self.tab3.x + 2, self.tab3.y + 4, self.tab3.width - 5, [
            "Название",
            'Тип',
            'Редкость',
            "Кол-во",
            'Цена',
            "Вес",
        ], [
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
            (Color.YELLOW, Color.RESET),
        ], Alignment.CENTER, Alignment.LEFT, add_numeration=True, max_rows=10)
        
        self.tab3.add_child(self.inventory_table)
    
    def init(self):
        self.set_control_panel()
        self.set_main_panel()
        self.set_help_panel()
        
        self.dialog_window = None
        
        self.tab = Tab(x=self.main_panel.x,
                       y=self.main_panel.y,
                       width=self.main_panel.width,
                       height=self.main_panel.height - self.help_panel_height + 2,
                       paddings=(1, 1, 1, 1),
                       control_keys=(None, Keys.TAB),
                       inactive_tab_color=(Color.YELLOW),
                       active_tab_color=Color.BG_YELLOW,
                       border_color=Color.BRIGHT_BLACK)  
        
        self.tab1 = Panel(self.tab.x, self.tab.y, self.main_panel.get_width() - 4, self.get_h(), "", "", Alignment.LEFT)
        self.set_tab_location()
        
        self.tab2 = Panel(self.tab.x, self.tab.y, self.main_panel.get_width(), self.get_h(), "", "", Alignment.LEFT)
        self.set_tab_player()
        
        self.tab3 = Panel(self.tab.x, self.tab.y, self.main_panel.get_width(), self.get_h(), "", "", Alignment.LEFT, paddings=(0, 0, 0, 0))
        self.set_tab_inventory()
        
        self.tab4 = Panel(self.tab.x, self.tab.y, self.main_panel.get_width(), self.get_h(), "", ".", Alignment.LEFT)
        
        self.tab.add_tabs([
            ("Локация", self.tab1, Keys.L),
            ("Персонаж", self.tab2, Keys.P),
            ("Навыки", self.tab4, Keys.A),
            ("Инвентарь", self.tab3, Keys.I),
            ("Квесты", self.tab4, Keys.Q),
            ("Глоссарий", self.tab4, Keys.B),
            ('Уведомления', self.tab4, Keys.U)
        ])
        
        self.add_child(self.control_panel)
        self.add_child(self.main_panel)
        self.add_child(self.tab)
        self.add_child(self.help_panel)
        
        self.first_mounted = 0
        
        self.name_location_text = ""
        self.name_region_text = ""
        self.description_location_text = ""
        
        self.main_panel.selected = False
        self.action_panel.selected = True
        self.control_activities.is_active = True
        
        self.on_event("player_move", self.update_location_info)
        self.on_event("player_collect_resource", self.update_inventory_info)
        
        self.tab.disable_tab(2)
        self.tab.disable_tab(4)
        self.tab.disable_tab(5)
        self.tab.disable_tab(6)
        
        self.finalize()
        
    def finalize(self):
        from src.Game import Game
        
        Game.player.move_to_location(Game.player.current_location)
        
    def update_location_info(self, data):
        from src.Game import Game
        
        self.name_location_text = Game.game_state["current_location_data"]()["name"].upper() + "  -"
        self.name_region_text = Game.game_state["current_region_data"]()["name"]
        self.description_location_text = Game.game_state["current_location_data"]()["description"]
        
        self.name_location.set_text(self.name_location_text)
        self.name_region.set_text(self.name_region_text)
        self.description_location.set_text(self.description_location_text)
        
        self.name_region.set_x(self.name_location.abs_x + self.name_location.width + 2)
        
        self.set_connections_main()
        self.set_resources_main()
        self.set_connections_control()
        self.set_resources_control()
        self.set_player_panel()
        
    def update_inventory_info(self, data):
        from src.Game import Game
        
        inv = Game.player.inventory
        
        for item in inv:
            type = inv[item]["item"]["type"].value
            rarity = inv[item]["item"]["rarity"].value
            amount = inv[item]["amount"]
            price = inv[item]["item"]["price"]
            weight = inv[item]["item"]["weight"]
        
        self.inventory_table.add_row([
                inv[item]["item"]["name"],
                type[1],
                rarity[0],
                str(amount),
                f"{price * amount:.2f} мон.",
                f"{weight * amount:.2f} кг.",
            ], [
            (Color.BRIGHT_YELLOW, Color.RESET),
            (Color.WHITE, Color.RESET),
            (type[2], Color.RESET),
            (rarity[2], Color.RESET),
            (Color.WHITE, Color.RESET),
            (Color.WHITE, Color.RESET),
            (Color.WHITE, Color.RESET),
        ])
        
        self.update_location_info(data)
        
    def update_player_characteristics_info(self):
        from src.Game import Game
        
        self.speed_characteristic_value.set_text(f"{Game.player.speed}")
        self.constitution_characteristic_value.set_text(f"{Game.player.total_constitution}")
        self.endurance_characteristic_value.set_text(f"{Game.player.total_endurance}")
        self.intelligence_characteristic_value.set_text(f"{Game.player.total_intelligence}")
        
    def ask_to_exit(self):
        from src.Game import Game
        
        if self.dialog_window: return
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text="Вы уверены, что хотите выйти?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
        
        def exit_game():
            self.unbind_child(self.dialog_window)
            self.dialog_window = None
            self.is_in_dialog = False
            Game.screen_manager.navigate_to_screen('main')
            
        def close_dialog():
            self.unbind_child(self.dialog_window)
            self.dialog_window = None
            self.is_in_dialog = False
            
        
        self.dialog_window.bind_yes(exit_game)
        self.dialog_window.bind_no(close_dialog)
        
        self.is_in_dialog = True
        self.add_child(self.dialog_window)
                
    def update(self):
        self.set_player_panel()
        self.update_player_characteristics_info()
        
        if self.first_mounted < 2:
            self.first_mounted += 1
            self.update_location_info(None)
            self.control_activities.set_selection(0)
            
        