from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel, Tab
from src.services.frontend.ui.general import Text
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color
from src.services.storage.State import State

class GameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.LEFT, self.toggle_active_root_panel)
        self.bind_key(Keys.RIGHT, self.toggle_active_root_panel)
    
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def toggle_active_root_panel(self):
        """Переключение активной корневой панели"""
        self.main_panel.selected = not self.main_panel.selected
        self.control_panel.selected = not self.control_panel.selected
        
    def set_control_panel(self): # Панель навигации
        control_panel_w = self.get_w() // 5
        self.control_panel = Panel(0, 0, control_panel_w, self.get_h(), " НАВИГАЦИЯ ", " ", Alignment.CENTER, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        
    def set_main_panel(self): # Основная панель
        main_panel_w = self.get_w() * 4 // 5
        self.main_panel = Panel(self.control_panel.get_width(), 0, main_panel_w, self.get_h(), "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK, border_color_selected=Color.BRIGHT_YELLOW)
        self.main_panel.selected = True
        
    def set_help_panel(self): # Панель помощи
        self.help_panel_height = 3
        self.help_panel_w = self.main_panel.width
        self.help_panel = Panel(self.control_panel.get_width(), self.get_h() - self.help_panel_height, self.help_panel_w, self.help_panel_height, "", " ", Alignment.LEFT, border_color=Color.BRIGHT_BLACK)
        
        text = Text(self.help_panel.x + 1, self.help_panel.y, "↑↓: Навигация, Tab: Переключение вкладок, Enter: Подтвердить, Esc: Назад, F1: Монитор производительности, ←→: Переключение активных панелей", Color.BRIGHT_BLACK, Color.RESET)
        self.help_panel.add_child(text)
        
    def set_tab_location(self): # Вкладка локации
        self.name_location = Text(self.tab1.x + 1, self.tab1.y + 3, '', Color.WHITE, Color.RESET)
        self.name_region = Text(self.name_location.x + self.name_location.width + 1, self.name_location.y, '', Color.BRIGHT_GREEN, Color.RESET)
        self.description_location = Text(self.tab1.x + 1, self.tab1.y + 5, '', Color.BRIGHT_BLACK, Color.RESET)
        
        self.tab1.add_child(self.name_location)
        self.tab1.add_child(self.name_region)
        self.tab1.add_child(self.description_location)
        
    
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
                
    def update(self):
        from src.Game import Game
        self.name_location.set_text(Game.game_state["current_location_data"]()["name"].upper() + "  -")
        self.name_region.set_text(Game.game_state["current_region_data"]()["name"])
        self.description_location.set_text(Game.game_state["current_location_data"]()["description"])
        
        self.name_region.set_x(self.name_location.abs_x + self.name_location.width + 2)