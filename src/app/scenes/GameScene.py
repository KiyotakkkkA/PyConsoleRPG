from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel, Tab, DialogWindow, Table, MultiPanel
from src.services.frontend.ui.general import Text, Menu, SeparatorItem
from src.services.frontend.ui.input import Selector
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color
from src.services.events import EventListener
from src.services.backend.managers import GlobalMetadataManager
import time

class GameScene(Screen):
    
    _event_listener = EventListener()
    
    def set_global_meta_uphead(data: dict):
        GlobalMetadataManager.get_instance().set_value('last_character', data['save_name'])
            
    _event_listener.on_event("game_was_loaded", set_global_meta_uphead)
    _event_listener.on_event("new_game_was_created", set_global_meta_uphead)
    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.current_selector = None
        
        self.current_display = 'chars'
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.LEFT, self.to_control_panel)
        self.bind_key(Keys.RIGHT, self.to_main_panel)
        
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
        if Game.game_state.state['current_relax_time'] > 0: return
        Game.game_state.state['start_time'] = time.time()
        Game.game_state.state['frame_count'] = 0
        
        Game.player.move_to_location(location_id)
        Game.game_state.state['current_relax_time'] = Game.player.get_location_relax_time()
        
        self.control_activities.set_selection(0)
    
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def to_control_panel(self):
        """Переключение активной корневой панели"""
        if not self.main_panel.selected and not self.action_panel.selected: return
        if self.player_multi_panel.is_selector_active(): return
        
        if self.is_in_dialog: return
        self.main_panel.set_selected(False)
        self.action_panel.set_selected(True)
        self.control_activities.set_active(True)
        self.control_activities.set_selection(0)
        
        self.update_inventory_item_description(None)
        
        self.emit_event("panel_changed", None)
        
    def to_main_panel(self):
        """Переключение активной корневой панели"""
        if not self.main_panel.selected and not self.action_panel.selected: return
        if self.player_multi_panel.is_selector_active(): return
        
        if self.is_in_dialog: return
        self.main_panel.set_selected(True)
        self.action_panel.set_selected(False)
        self.control_activities.set_active(False)
        self.control_activities.flush_selection()
        
        self.update_inventory_item_description(None)
        
        self.emit_event("panel_changed", None)
        
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
                                       gap=1,
                                       auto_resize=True,
                                       max_width=self.action_panel.width - 4)
        
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
        
        self._stats_general = [
            {
                'id': 'name',
                'label': "Имя: ",
                'value': "",
                'description': "",
                'color': Color.BRIGHT_YELLOW
            },
            {
                'id': 'race',
                'label': "Раса: ",
                'value': "",
                'description': "",
                'color': Color.BRIGHT_YELLOW
            }
        ]
        
        self._stats_level = [
            {
                'id': 'level',
                'label': "Уровень: ",
                'value': "",
                'description': "",
                'color': Color.BRIGHT_YELLOW
            },
            {
                'id': 'current_exp',
                'label': "До повышения: ",
                'value': "",
                'description': "",
                'color': Color.BRIGHT_YELLOW
            }
        ]
        
        self._stats_indicators = [
            {
                'id': 'health',
                'label': "Здоровье: ",
                'value': "",
                'color': Color.BRIGHT_RED
            },
            {
                'id': 'energy',
                'label': "Энергия: ",
                'value': "",
                'color': Color.BRIGHT_GREEN
            },
            {
                'id': 'astrum',
                'label': "Аструм: ",
                'value': "",
                'color': Color.CYAN
            }
        ]
        
        y = self.player_panel.y + 1
        for stat in self._stats_general:
            setattr(self, f"player_{stat['id']}_addition", Text(self.player_panel.x + 2, y, "[*]", Color.BRIGHT_MAGENTA, Color.RESET))
            setattr(self, f"player_{stat['id']}_label", Text(getattr(self, f"player_{stat['id']}_addition").x + getattr(self, f"player_{stat['id']}_addition").width + 1, y, stat['label'], Color.WHITE, Color.RESET))
            setattr(self, f"player_{stat['id']}", Text(getattr(self, f"player_{stat['id']}_label").x + getattr(self, f"player_{stat['id']}_label").width + 1, y, "", stat['color'], Color.RESET))
            
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_addition"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_label"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}"))
            
            y += 2
            
        for stat in self._stats_level:
            setattr(self, f"player_{stat['id']}_addition", Text(self.player_panel.x + 2, y, "[*]", Color.BRIGHT_MAGENTA, Color.RESET))
            setattr(self, f"player_{stat['id']}_label", Text(getattr(self, f"player_{stat['id']}_addition").x + getattr(self, f"player_{stat['id']}_addition").width + 1, y, stat['label'], Color.WHITE, Color.RESET))
            setattr(self, f"player_{stat['id']}", Text(getattr(self, f"player_{stat['id']}_label").x + getattr(self, f"player_{stat['id']}_label").width + 1, y, "", stat['color'], Color.RESET))
            
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_addition"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_label"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}"))
            
            y += 2
        
        for stat in self._stats_indicators:
            setattr(self, f"player_{stat['id']}_addition", Text(self.player_panel.x + 2, y, "[*]", Color.BRIGHT_MAGENTA, Color.RESET))
            setattr(self, f"player_{stat['id']}_label", Text(getattr(self, f"player_{stat['id']}_addition").x + getattr(self, f"player_{stat['id']}_addition").width + 1, y, stat['label'], Color.WHITE, Color.RESET))
            setattr(self, f"player_{stat['id']}", Text(getattr(self, f"player_{stat['id']}_label").x + getattr(self, f"player_{stat['id']}_label").width + 1, y, "", stat['color'], Color.RESET))
            
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_addition"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}_label"))
            self.player_panel.add_child(getattr(self, f"player_{stat['id']}"))
            
            y += 2
        
        self.control_panel.add_child(self.action_panel)
        self.action_panel.add_child(self.control_activities)
        self.control_panel.add_child(self.player_panel)
        
        self.player_panel.add_child(self.relax_time)
        
    def set_main_panel(self): # Основная панель
        main_panel_w = self.get_w() * 4 // 5
        self.main_panel = Panel(self.control_panel.get_width(), 0, main_panel_w, self.get_h(), "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        
    def set_help_panel(self): # Панель помощи
        self.help_panel_height = 3
        self.help_panel_w = self.main_panel.width
        self.help_panel = Panel(self.control_panel.get_width(), self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, paddings=(1, 0, 0, 0))
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Tab: Переключение вкладок, Enter: Подтвердить, Esc: Назад, F1: Монитор производительности, ←→: Переключение активных панелей", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
    def set_connections_main(self):  # Вкладка локации - Перемещения
        from src.Game import Game
        
        # Получаем данные один раз
        location_data = Game.game_state.computable["current_location_data"]()
        conns = location_data["connections"]
        player_level = Game.player.current_level
        
        connections = []
        gap = 1
        base_x = self.main_connections.x + 1
        base_y = self.main_connections.y
        
        for connection_id in conns:
            connection_data = conns[connection_id]
            level_req = connection_data.get('level')
            has_required_level = not level_req or level_req <= player_level
            
            main_text = self.temp_main_connections_for_text.get(
                "{}".format(connection_id),
                Text(base_x, base_y + gap, 
                connection_data["name"], 
                Color.WHITE if has_required_level else Color.BRIGHT_BLACK, 
                Color.RESET)
            )
            connections.append(main_text)
            gap += 1
            
            if not has_required_level:
                error_text = self.temp_main_connections_for_text.get(
                    "{}".format(connection_id),
                    Text(base_x, base_y + gap,
                    f"  [!] Необходим уровень: {level_req}",
                    Color.BRIGHT_RED, Color.RESET)
                )
                connections.append(error_text)
                gap += 1
        
        self.main_connections.set_children(connections)
        
        for text in self.temp_main_connections_for_text.values():
            del text
        
        self.temp_main_connections_for_text.clear()

    def set_resources_main(self):  # Вкладка локации - Ресурсы (+ события респавна ресурса)
        from src.Game import Game
        
        location_data = Game.game_state.computable["current_location_data"]()
        res_dict = location_data["resources"]
        loc_id = location_data["id"]
        player_level = Game.player.current_level
        current_time = time.time()
        
        loc_res_meta = Game.game_state.loc_res_meta.get(loc_id, {})
        respawning_resources = Game.game_state.state.get('respawning_resources', {}).get(loc_id, {})
        
        resources = []
        respawned = []
        gap = 1
        base_x = self.resources_panel.x + 1
        base_y = self.resources_panel.y
        
        for resource_id in res_dict:
            resource_config = res_dict[resource_id]
            res_data = Game.get_item_by_id(resource_id)
            
            level_req = res_data.get('level_need')
            has_required_level = not level_req or level_req <= player_level
            
            amount = loc_res_meta.get(resource_id, {}).get('amount', resource_config['amount'])
            
            time_diff = 0
            respawn_info = respawning_resources.get(resource_id)
            if respawn_info:
                time_diff = respawn_info['respawn_time'] - (current_time - respawn_info['collected_time'])
                if time_diff <= 0:
                    respawned.append((resource_id, time_diff))
            
            is_available = has_required_level and amount > 0
            main_color = Color.WHITE if is_available else Color.BRIGHT_BLACK
            count_color = Color.BRIGHT_YELLOW if is_available else Color.BRIGHT_BLACK
            rarity_color = res_data['rarity'].value[2] if is_available else Color.BRIGHT_BLACK
            
            current_x = base_x
            current_y = base_y + gap
            
            text_name = self.temp_main_resources_for_text.get(
                "{}_name".format(resource_id),
                Text(current_x, current_y, res_data["name"], main_color, Color.RESET)
            )
            current_x += text_name.width + 1
            
            text_count = self.temp_main_resources_for_text.get(
                "{}_count".format(resource_id),
                Text(current_x, current_y, f"[x{amount}]", count_color, Color.RESET)
            )
            current_x += text_count.width + 1
            
            text_rarity = self.temp_main_resources_for_text.get(
                "{}_rarity".format(resource_id),
                Text(current_x, current_y, f"[{res_data['rarity'].value[0]}]", rarity_color, Color.RESET)
            )
            
            resources.extend([text_name, text_count, text_rarity])
            gap += 1
            
            error_text = None
            level_error = None
            
            if amount <= 0:
                error_text = self.temp_main_resources_for_text.get(
                    "{}_error".format(resource_id),
                    Text(base_x, base_y + gap,
                    f"  ЗАКОНЧИЛСЯ - восстановится через {time_diff:.2f} сек.",
                    Color.BRIGHT_RED, Color.RESET)
                )
                resources.append(error_text)
                gap += 1
            
            if not has_required_level:
                level_error = self.temp_main_resources_for_text.get(
                    "{}_level_error".format(resource_id),
                    Text(base_x, base_y + gap,
                    f"  [!] Необходим уровень: {level_req}",
                    Color.BRIGHT_RED, Color.RESET)
                )
                resources.append(level_error)
                gap += 1

            del res_data
        
        if not resources:
            empty_text = self.temp_main_resources_for_text.get(
                "empty_text",
                Text(base_x, base_y + 1, "Пусто...", Color.BRIGHT_BLACK, Color.RESET)
            )
            resources.append(empty_text)
        
        self.resources_panel.set_children(resources)
        
        for resource in resources:
            del resource
        
        for resource_id, _ in respawned:
            self.emit_event("resource_respawned", {"location_id": loc_id, "resource_id": resource_id})
            
        for text in self.temp_main_resources_for_text.values():
            del text
        
        self.temp_main_resources_for_text.clear()

    def set_connections_control(self):  # Панель навигации - перемещения
        from src.Game import Game
        
        self.temp_items_activities.clear()
        
        location_data = Game.game_state.computable["current_location_data"]()
        conns = location_data["connections"]
        player_level = Game.player.current_level
        
        def create_move_callback(connection_id):
            return lambda: self.game_move_to_location(connection_id)
        
        for connection_id in conns:
            connection_data = conns[connection_id]
            level_req = connection_data.get('level')
            
            if level_req and level_req > player_level:
                continue
                
            callback = create_move_callback(connection_data['id'])
            self.temp_items_activities.append((
                (f"Идти в: {connection_data['name']}", Color.WHITE), 
                None, 
                callback
            ))

    def set_resources_control(self):  # Панель навигации - ресурсы
        from src.Game import Game
        
        location_data = Game.game_state.computable["current_location_data"]()
        res_dict = location_data["resources"]
        loc_id = location_data['id']
        player_level = Game.player.current_level
        
        loc_res_meta = Game.game_state.loc_res_meta.get(loc_id, {})
        
        start_len = len(self.temp_items_activities)
        resource_activities = []
        
        def create_collect_callback(resource_id):
            return lambda: self.game_collect_resource(resource_id)
        
        for resource_id in res_dict:
            resource_config = res_dict[resource_id]
            res_data = Game.get_item_by_id(resource_id)
            
            amount = loc_res_meta.get(resource_id, {}).get('amount', resource_config['amount'])
            
            level_req = res_data.get('level_need')
            has_required_level = not level_req or level_req <= player_level
            
            if has_required_level and amount > 0:
                callback = create_collect_callback(resource_id)
                resource_activities.append((
                    (f"Собрать: {res_data['name']} [x{amount}]", Color.WHITE), 
                    None, 
                    callback
                ))
                
            del res_data
        
        if resource_activities and start_len < len(self.temp_items_activities) + len(resource_activities):
            resource_activities.insert(0, (
                SeparatorItem("-", 0, Color.BRIGHT_BLACK), None, None
            ))
        
        self.temp_items_activities = self.temp_items_activities + resource_activities
        self.control_activities.set_items(self.temp_items_activities)
        
        for resource in resource_activities:
            del resource
    
    def set_npcs_control(self):
        from src.Game import Game
        
        location_data = Game.game_state.computable["current_location_data"]()
        npcs_dict = location_data["npcs"]
        
        start_len = len(self.temp_items_activities)
        npcs_activities = []
        
        def create_npc_callback(npc_id):
            return lambda: print(npc_id)
        
        for npc_id in npcs_dict:
            npc_data = Game.get_npc_by_id(npc_id)
            
            callback = create_npc_callback(npc_id)
            npcs_activities.append((
                (f"Говорить с: {npc_data['name']}", Color.WHITE), 
                None, 
                callback
            ))
            
        if npcs_activities and start_len < len(self.temp_items_activities) + len(npcs_activities):
            npcs_activities.insert(0, (
                SeparatorItem("-", 0, Color.BRIGHT_BLACK), None, None
            ))
        
        self.temp_items_activities = self.temp_items_activities + npcs_activities
        self.control_activities.set_items(self.temp_items_activities)
        
        for npc in npcs_activities:
            del npc
        
    def set_player_panel(self): # Панель навигации - панель игрока
        from src.Game import Game
        
        self.player_panel.set_y(self.action_panel.y + self.action_panel.height)
        self.player_panel.set_height(self.control_panel.height - self.action_panel.height - 6)
        
        relax_time_y = self.player_panel.y + 1
        
        self.relax_time.set_y(relax_time_y)
        if Game.game_state.state['current_relax_time'] > 0:
            self.relax_time.set_fg_color(Color.BRIGHT_RED)
            self.relax_time.set_text(f"| ПЕРЕМЕЩЕНИЕ - {float(Game.game_state.state['current_relax_time']):.2f} сек. |")
        else:
            self.relax_time.set_fg_color(Color.BRIGHT_GREEN)
            self.relax_time.set_text("| ГОТОВ К ПЕРЕМЕЩЕНИЮ |")
        
        name_y = relax_time_y + 2
        race_y = name_y + 1
        level_y = race_y + 2
        exp_y = level_y + 1
        health_y = exp_y + 2
        energy_y = health_y + 1
        astrum_y = energy_y + 1
        
        self.player_name_addition.set_y(name_y)
        self.player_name_label.set_y(name_y)
        self.player_name.set_y(name_y)
        self.player_name.set_text(Game.player.name)
        
        self.player_race_addition.set_y(race_y)
        self.player_race_label.set_y(race_y)
        self.player_race.set_y(race_y)
        self.player_race.set_text(self._locale_manager[f"races.{Game.player.race}.name"])
        
        self.player_level_addition.set_y(level_y)
        self.player_level_label.set_y(level_y)
        self.player_level.set_y(level_y)
        self.player_level.set_text(f"{Game.player.current_level}")
        
        self.player_current_exp_addition.set_y(exp_y)
        self.player_current_exp_label.set_y(exp_y)
        self.player_current_exp.set_y(exp_y)
        self.player_current_exp.set_text(f"{Game.player.current_exp} / {Game.player.exp_to_next_level}")
        
        self.player_health_addition.set_y(health_y)
        self.player_health_label.set_y(health_y)
        self.player_health.set_y(health_y)
        self.player_health.set_text(f"{Game.player.health} / {Game.player.max_health}")
        
        self.player_energy_addition.set_y(energy_y)
        self.player_energy_label.set_y(energy_y)
        self.player_energy.set_y(energy_y)
        self.player_energy.set_text(f"{Game.player.energy} / {Game.player.max_energy}")
        
        self.player_astrum_addition.set_y(astrum_y)
        self.player_astrum_label.set_y(astrum_y)
        self.player_astrum.set_y(astrum_y)
        self.player_astrum.set_text(f"{Game.player.astrum} / {Game.player.max_astrum}")
        
        Game.time_count_with_fps('current_relax_time')
        
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
        self.player_multi_panel = MultiPanel(
            x=self.tab1.x + 2,
            y=self.tab1.y + 3,
            width=self.tab1.width - 3,
            height=self.tab1.height - 7,
            key_to_activate=Keys.S)
        
        self.characteristics_container = Panel(0, 0, 0, 0, "", " ")
        self.ability_container = Panel(0, 0, 0, 0, "", " ")
        
        self.player_multi_panel.add_panels([
            ("chars", "Характеристики", self.characteristics_container),
            ("abilities", "Способности", self.ability_container)
        ], (Alignment.CENTER, Color.BLACK, Color.BLACK))
        
        self.characteristics_panel = Panel(x=self.tab1.x + 1,
                          y=self.tab1.y + 4,
                          width=1,
                          height=self.tab1.height - 8,
                          title=" Основные характеристики ",
                          filler=" ",
                          title_alignment=Alignment.LEFT,
                          border_color=Color.BRIGHT_BLACK,
                          border_color_selected=Color.BRIGHT_BLACK,
                          title_color=Color.YELLOW)
        
        self._chars = [
            {
                'id': 'speed',
                'label': "Скорость: ",
                'desc': "- Увеличение этого параметра\nуменьшает время перезарядки перемещения"
            },
            {
                'id': 'constitution',
                'label': "Телосложение: ",
                'desc': "- Увеличение этого параметра\nувеличивает максимальное здоровье"
            },
            {
                'id': 'endurance',
                'label': "Выносливость: ",
                'desc': "- Увеличение этого параметра\nувеличивает максимальное энергии"
            },
            {
                'id': 'intelligence',
                'label': "Интеллект: ",
                'desc': "- Увеличение этого параметра\nувеличивает максимальный запас аструма\n(астрального вещества,\nнеобходимого для сотворения заклинаний)"
            }
        ]
        
        y = self.characteristics_panel.y + 2
        for i, char in enumerate(self._chars):
            setattr(self, f"{char['id']}_characteristic_addition", Text(self.characteristics_panel.x + 2, y, "[*]", Color.BRIGHT_MAGENTA, Color.RESET))
            setattr(self, f"{char['id']}_characteristic", Text(getattr(self, f"{char['id']}_characteristic_addition").x + getattr(self, f"{char['id']}_characteristic_addition").width + 1, y, char['label'], Color.WHITE, Color.RESET))
            setattr(self, f"{char['id']}_characteristic_value", Text(getattr(self, f"{char['id']}_characteristic").x + getattr(self, f"{char['id']}_characteristic").width + 2, y, "", Color.BRIGHT_YELLOW, Color.RESET))
            setattr(self, f"{char['id']}_description", Text(self.speed_characteristic_addition.x, y + 1, char['desc'], Color.BRIGHT_BLACK, Color.RESET))
            
            self.characteristics_panel.add_child(getattr(self, f"{char['id']}_characteristic_addition"))
            self.characteristics_panel.add_child(getattr(self, f"{char['id']}_characteristic"))
            self.characteristics_panel.add_child(getattr(self, f"{char['id']}_characteristic_value"))
            self.characteristics_panel.add_child(getattr(self, f"{char['id']}_description"))
            
            y += getattr(self, f"{char['id']}_description").height + 1
        
        self.tab2.add_child(self.player_multi_panel)
        
        self.characteristics_container.add_child(self.characteristics_panel)
        
        self.ability_panel = Panel(x=self.tab1.x + 1,
                          y=self.tab1.y + 4,
                          width=1,
                          height=self.tab1.height - 8,
                          title=" Способности ",
                          filler=" ",
                          title_alignment=Alignment.LEFT,
                          border_color=Color.BRIGHT_BLACK,
                          border_color_selected=Color.BRIGHT_BLACK,
                          title_color=Color.YELLOW)
        
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
        
        self.inventory_item_description_panel = Panel(self.tab3.x + 2, self.inventory_table.y + self.inventory_table.height + 1, self.tab3.width - 4, 0, " Описание ", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_BLACK, title_color=Color.YELLOW)
        self.inventory_item_description = Text(self.inventory_item_description_panel.x + 2, self.inventory_item_description_panel.y + 1, "dsfsdfsfd " * 40, Color.BRIGHT_BLACK, Color.RESET, auto_resize=True, max_width=self.inventory_item_description_panel.width - 6)
        
        self.inventory_item_description_panel.add_child(self.inventory_item_description)
        
        self.tab3.add_child(self.inventory_table)
        self.tab3.add_child(self.inventory_item_description_panel)
        
        self.inventory_table.connect_to_tab(self.tab, "inventory")
        self.inventory_table.connect_to_panel(self.main_panel)
    
    def init(self):
        self.temp_items_activities = []
        
        self.temp_main_resources_for_text = {}
        self.temp_main_connections_for_text = {}
        
        self.with_redirect_to_dialog_window_preset("Вернуться в главное меню?", (self.get_w() // 2 - 40 // 2, self.get_h() // 2 - 25), (40, 7), Color.BRIGHT_YELLOW)
        
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
            ('location', "Локация", self.tab1, Keys.L),
            ('player', "Персонаж", self.tab2, Keys.P),
            ('skills', "Навыки", self.tab4, Keys.A),
            ('inventory', "Инвентарь", self.tab3, Keys.I),
            ('quests', "Квесты", self.tab4, Keys.Q),
            ('glossary', "Глоссарий", self.tab4, Keys.B),
            ('notifications', "Уведомления", self.tab4, Keys.U)
        ])
        
        self.player_multi_panel.connect_to_tab(self.tab, 'player')
        self.player_multi_panel.connect_to_panel(self.main_panel)
        
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
        
        self.dialog_window = DialogWindow(x=self.get_w() // 2 - 20,
                                          y=self.get_h() // 2 - 25,
                                          width=40,
                                          height=7,
                                          text="Вы уверены, что хотите выйти?",
                                          ctype="YES_NO",
                                          text_color=Color.BRIGHT_YELLOW)
        
        self.on_event("player_move", self.update_location_info)
        self.on_event("player_collect_resource", self.update_inventory_info)
        self.on_event("resource_respawned", self.update_resources_count)
        self.on_event(f"{self.inventory_table.id}_row_selected", self.update_inventory_item_description)
        
        self.tab.disable_tab(2)
        self.tab.disable_tab(4)
        self.tab.disable_tab(5)
        self.tab.disable_tab(6)
        
        self.control_activities.set_active(True)
        
        self.finalize()
        
    def finalize(self):
        from src.Game import Game
        
        Game.player.move_to_location(Game.player.current_location)
        
    def update_resources_count(self, data=None):
        from src.Game import Game
        
        if not Game.game_state.state['respawning_resources'].get(data['location_id']):
            return
        
        loc = Game.game_state.state['respawning_resources'][data['location_id']][data['resource_id']]
        Game.game_state.loc_res_meta[data['location_id']][data['resource_id']]['amount'] = loc['amount_after_respawn']
        Game.get_location_by_id(data['location_id'])['resources'][data['resource_id']]['amount'] = loc['amount_after_respawn']
        
        del Game.game_state.state['respawning_resources'][data['location_id']][data['resource_id']]
        
        if len(Game.game_state.state['respawning_resources'][data['location_id']]) == 0:
            del Game.game_state.state['respawning_resources'][data['location_id']]
        
        self.set_resources_main()
        self.set_connections_control()
        self.set_resources_control()
        self.set_npcs_control()
        
    def update_location_info(self, data):
        from src.Game import Game
        
        self.name_location_text = Game.game_state.computable["current_location_data"]()["name"].upper() + "  -"
        self.name_region_text = Game.game_state.computable["current_region_data"]()["name"]
        self.description_location_text = Game.game_state.computable["current_location_data"]()["description"]
        
        self.name_location.set_text(self.name_location_text)
        self.name_region.set_text(self.name_region_text)
        self.description_location.set_text(self.description_location_text)
        
        self.name_region.set_x(self.name_location.abs_x + self.name_location.width + 2)
        
        self.set_connections_main()
        self.set_resources_main()
        self.set_connections_control()
        self.set_resources_control()
        self.set_npcs_control()
        self.set_player_panel()
        
    def update_inventory_info(self, data):
        from src.Game import Game
        
        if len(Game.player.inventory) == 0: return
        
        inv = Game.player.inventory
        
        _temp_rows = []
        _temp_colors = []
        _temp_actions = []
        _temp_keys = []
        
        for item in inv:
            
            _res_data = Game.get_item_by_id(item)
            
            type = _res_data["type"].value
            rarity = _res_data["rarity"].value
            amount = inv[item]["amount"]
            price = _res_data["price"]
            weight = _res_data["weight"]
            
            _temp_keys.append(item)
        
            _temp_rows.append([
                _res_data["name"],
                type[1],
                rarity[0],
                str(amount),
                f"{price * amount:.2f} мон.",
                f"{weight * amount:.2f} кг.",
            ])
            
            _temp_colors.append([
            (Color.BRIGHT_YELLOW, Color.RESET),
            (Color.WHITE, Color.RESET),
            (type[2], Color.RESET),
            (rarity[2], Color.RESET),
            (Color.WHITE, Color.RESET),
            (Color.WHITE, Color.RESET),
            (Color.WHITE, Color.RESET),
        ])
        
        self.inventory_table.set_rows(_temp_keys, _temp_rows, _temp_colors, _temp_actions)
        
        self.update_inventory_item_description(None)
        
        self.update_location_info(data)
        
    def update_inventory_item_description(self, data):
        from src.Game import Game
        
        if not data:
            self.inventory_item_description_panel.set_visible(False)
            self.inventory_item_description.set_visible(False)
            return
        
        self.inventory_item_description_panel.set_visible(True)
        self.inventory_item_description.set_visible(True)
        
        self.inventory_item_description_panel.set_y(self.inventory_table.y + self.inventory_table.height + 1)
        self.inventory_item_description.set_y(self.inventory_item_description_panel.y + 1)
        
        item = Game.get_item_by_id(data[-1])
        
        self.inventory_item_description.set_text(item['description'])
        
    def update_player_characteristics_info(self):
        from src.Game import Game
        
        self.speed_characteristic_value.set_text(f"{Game.player.speed}")
        self.constitution_characteristic_value.set_text(f"{Game.player.total_constitution}")
        self.endurance_characteristic_value.set_text(f"{Game.player.total_endurance}")
        self.intelligence_characteristic_value.set_text(f"{Game.player.total_intelligence}")
        
    def update(self):
        from src.Game import Game
        
        self.set_player_panel()
        self.update_player_characteristics_info()
        
        if len(Game.game_state.state['respawning_resources']) > 0:
            self.set_resources_main()
        
        if self.first_mounted < 2:
            self.first_mounted += 1
            self.update_location_info(None)
            self.update_inventory_info(None)
            self.control_activities.set_selection(0)