from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel, Tab
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color

class GameScene(Screen):
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
    
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
    
    def init(self):
        control_panel_w, main_panel_w = self.get_w() // 5, self.get_w() * 4 // 5
        
        self.control_panel = Panel(0, 0, control_panel_w, self.get_h(), "", " ", Alignment.LEFT)
        self.main_panel = Panel(control_panel_w, 0, main_panel_w, self.get_h(), "", " ", Alignment.LEFT)
        
        self.tab = Tab(x=self.main_panel.x,
                       y=self.main_panel.y,
                       width=self.main_panel.width,
                       height=self.main_panel.height,
                       paddings=(1, 1, 1, 1),
                       inactive_tab_color=(Color.YELLOW),
                       active_tab_color=Color.BG_YELLOW)
        
        self.tab1 = Panel(self.tab.x, self.tab.y, control_panel_w, self.get_h(), "", "@", Alignment.LEFT)
        self.tab2 = Panel(self.tab.x, self.tab.y, control_panel_w, self.get_h(), "", "#", Alignment.LEFT)
        self.tab3 = Panel(self.tab.x, self.tab.y, control_panel_w, self.get_h(), "", ".", Alignment.LEFT)
        
        self.tab.add_tabs([
            ("Tab 1", self.tab1, Keys.A),
            ("Tab 2", self.tab2, Keys.B),
            ("Tab 3", self.tab3, Keys.C),
        ])
        
        self.add_child(self.control_panel)
        self.add_child(self.main_panel)
        self.add_child(self.tab)
                
    def update(self):
        pass