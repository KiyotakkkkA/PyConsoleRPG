from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel, Tab
from src.services.frontend.ui.general import Text, Menu
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color

class GameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.LEFT, self.to_control_panel)
        self.bind_key(Keys.RIGHT, self.to_main_panel)
        
    def game_move_to_location(self, location_id: str):
        """
        Перемещение игрока в указанную локацию
        
        Args:
            location_id: ID локации
        """
        from src.Game import Game
        Game.player.move_to_location(location_id)
        
        self.control_connections.set_selection(0)
    
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def to_control_panel(self):
        """Переключение активной корневой панели"""
        self.main_panel.selected = False
        self.action_panel.selected = True
        self.control_connections.is_active = True
        self.control_connections.set_selection(0)
        
    def to_main_panel(self):
        """Переключение активной корневой панели"""
        self.main_panel.selected = True
        self.action_panel.selected = False
        self.control_connections.is_active = False
        self.control_connections.flush_selection()
        
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
        
        self.control_connections = Menu(x=self.action_panel.x + 1,
                                       y=self.action_panel.y,
                                       inactive_menu_color=Color.BRIGHT_BLACK,
                                       active_menu_color=Color.BRIGHT_CYAN,
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
        
        self.player_level_label = Text(self.player_panel.x + 2, self.player_panel.y, "[*] Уровень:", Color.WHITE, Color.RESET)
        self.player_level = Text(self.player_level_label.x + self.player_level_label.width + 1, self.player_panel.y, "", Color.YELLOW, Color.RESET)
        
        self.control_panel.add_child(self.action_panel)
        self.action_panel.add_child(self.control_connections)
        self.control_panel.add_child(self.player_panel)
        
        self.player_panel.add_child(self.player_level)
        self.player_panel.add_child(self.player_level_label)
        
    def set_main_panel(self): # Основная панель
        main_panel_w = self.get_w() * 4 // 5
        self.main_panel = Panel(self.control_panel.get_width(), 0, main_panel_w, self.get_h(), "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        self.main_panel.selected = True
        
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
        
    def set_connections_control(self):
        from src.Game import Game
        
        connections = []
        conns = Game.game_state["current_location_data"]()["connections"]
        player_level = Game.player.current_level
        
        for connection in conns:            
            reqs = {
                'level': {
                    'req': lambda req=conns[connection]['level']: req,
                    'complete': lambda req=conns[connection]['level']: not req or req <= player_level,
                    'error': lambda req=conns[connection]['level']: f"Необходим уровень [{req}]"
                }
            }
            if not reqs['level']['complete'](): continue
            connections.append(((f"Идти в: {conns[connection]['name']}", Color.WHITE), None, lambda conn=conns[connection]['id']: self.game_move_to_location(conn)))
        
        self.control_connections.set_items(connections)
        
    def set_player_panel(self): # Панель навигации - панель игрока
        from src.Game import Game
        
        self.player_panel.set_y(self.action_panel.y + self.action_panel.height)
        self.player_panel.set_height(self.control_panel.height - self.action_panel.height - 6)
        
        self.player_level.set_text(f"{Game.player.current_level}")
        self.player_level.set_y(self.player_panel.y + 1)
        self.player_level_label.set_y(self.player_panel.y + 1)
        
    def set_tab_location(self): # Вкладка локации
        name_location_y = self.tab1.y + 3
        self.name_location = Text(self.tab1.x + 1, name_location_y, '', Color.WHITE, Color.RESET)
        
        name_region_y = name_location_y
        self.name_region = Text(self.name_location.x + self.name_location.width + 1, name_region_y, '', Color.BRIGHT_GREEN, Color.RESET)
        
        description_location_y = name_region_y + 2
        self.description_location = Text(self.tab1.x + 1, description_location_y, '', Color.BRIGHT_BLACK, Color.RESET)
        
        self.main_connections = Panel(x=self.tab1.x + 1,
                                y=description_location_y + 2,
                                width=self.tab1.width - 2,
                                height=10,
                                title="Все переходы:",
                                filler=" ",
                                title_alignment=Alignment.LEFT,
                                border_color=Color.BLACK,
                                border_color_selected=Color.BLACK,
                                title_color=Color.YELLOW)
        
        self.tab1.add_child(self.name_location)
        self.tab1.add_child(self.name_region)
        self.tab1.add_child(self.description_location)
        self.tab1.add_child(self.main_connections)
        
    
    def init(self):
        self.set_control_panel()
        self.set_main_panel()
        self.set_help_panel()
        
        self.tab = Tab(x=self.main_panel.x,
                       y=self.main_panel.y,
                       width=self.main_panel.width,
                       height=self.main_panel.height - self.help_panel_height + 2,
                       paddings=(1, 1, 1, 1),
                       control_keys=(None, Keys.TAB),
                       inactive_tab_color=(Color.YELLOW),
                       active_tab_color=Color.BG_YELLOW,
                       border_color=Color.BRIGHT_BLACK)  
        
        self.tab1 = Panel(self.tab.x, self.tab.y, self.control_panel.get_width(), self.get_h(), "", "", Alignment.LEFT)
        self.set_tab_location()
        
        self.tab2 = Panel(self.tab.x, self.tab.y, self.control_panel.get_width(), self.get_h(), "", "#", Alignment.LEFT)
        self.tab3 = Panel(self.tab.x, self.tab.y, self.control_panel.get_width(), self.get_h(), "", ".", Alignment.LEFT)
        
        self.tab.add_tabs([
            ("Локация", self.tab1, Keys.L),
            ("Персонаж", self.tab2, Keys.P),
            ("Навыки", self.tab2, Keys.A),
            ("Инвентарь", self.tab2, Keys.I),
            ("Квесты", self.tab2, Keys.Q),
            ("Глоссарий", self.tab2, Keys.B),
            ('Уведомления', self.tab2, Keys.U)
        ])
        
        self.add_child(self.control_panel)
        self.add_child(self.main_panel)
        self.add_child(self.tab)
        self.add_child(self.help_panel)
        
        self.first_mounted = 0
        
        self.name_location_text = ""
        self.name_region_text = ""
        self.description_location_text = ""
        
        self.on_event("player_move", self.update_location_info)
        
        self.finalize()
        
    def finalize(self):
        from src.Game import Game
        
        Game.player.move_to_location(Game.player.current_location)
        
    def update_location_info(self, data):
        from src.Game import Game
        
        self.name_location_text = Game.game_state["current_location_data"]()["name"].upper() + "  -"
        self.name_region_text = Game.game_state["current_region_data"]()["name"]
        self.description_location_text = Game.game_state["current_location_data"]()["description"]
        
        self.set_connections_main()
        self.set_connections_control()
                
    def update(self):
        self.name_location.set_text(self.name_location_text)
        self.name_region.set_text(self.name_region_text)
        self.description_location.set_text(self.description_location_text)

        self.set_player_panel()
        
        self.name_region.set_x(self.name_location.abs_x + self.name_location.width + 2)
        
        if self.first_mounted < 2:
            self.first_mounted += 1
            self.update_location_info(None)