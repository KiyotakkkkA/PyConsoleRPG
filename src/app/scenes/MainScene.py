from src.services.frontend.core import Screen
from src.services.frontend.ui.containers import Panel
from src.services.storage.State import State
from src.services.frontend.core.Format import Alignment
from src.services.events import Keys
from src.services.output import Color

class MainScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
    def init(self):
        self.selected_panel_index = None
        self.panels = ["panel11", "panel12", "panel13", "panel14"]
        
        self.panel1 = Panel(5, 3, 30, 7, "Основная панель", border_color=Color.GREEN, title_color=Color.YELLOW)

        self.panel11 = Panel(5, 4, 40, 10, "Подпанель 1 - State: {}".format(State.counter1), ".", Alignment.LEFT, title_color=Color.YELLOW)
        self.panel12 = Panel(50, 4, 40, 10, "Подпанель 2 - State: {}".format(State.counter1), ".", Alignment.LEFT, title_color=Color.YELLOW)
        self.panel13 = Panel(5, 15, 40, 10, "Подпанель 3 - State: {}".format(self.panel11.parent), "", Alignment.LEFT, title_color=Color.YELLOW)
        self.panel14 = Panel(50, 15, 40, 10,
                             "Подпанель 4 - State: {}".format(State.counter1),
                             ".", Alignment.LEFT, title_color=Color.YELLOW,
                             filler_color=Color.CYAN)
        
        self.panel1.add_children([self.panel11, self.panel12, self.panel13, self.panel14],
                                 self.panels)
        
        self.add_child(self.panel1)
        
        self.bind_key(Keys.UP, self.clear_counter)
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        self.bind_key(Keys.LEFT, self.select_children_panels_back)
        self.bind_key(Keys.RIGHT, self.select_children_panels_forward)
        
    @staticmethod
    def clear_counter():
        State.counter1 = 0

    def select_children_panels_back(self):
        if not self.panel1.selected:
            return
        
        if self.selected_panel_index == None:
            self.selected_panel_index = -1
        
        self.panel1.get_child_by_name(self.panels[self.selected_panel_index]).selected = False
        if self.selected_panel_index == -1:
            self.selected_panel_index = len(self.panels) - 1
        else:
            self.selected_panel_index = (self.selected_panel_index - 1) % len(self.panels)
        self.panel1.get_child_by_name(self.panels[self.selected_panel_index]).selected = True
        
        
        
    def select_children_panels_forward(self):
        if not self.panel1.selected:
            return
        
        if self.selected_panel_index == None:
            self.selected_panel_index = -1
        
        self.panel1.get_child_by_name(self.panels[self.selected_panel_index]).selected = False
        self.selected_panel_index = (abs(self.selected_panel_index + 1)) % len(self.panels)
        self.panel1.get_child_by_name(self.panels[self.selected_panel_index]).selected = True
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def update(self):
        State.counter1 += 1
        
        self.panel11.title = "Подпанель 1 - State: {}".format(State.counter1)
        self.panel12.title = "Подпанель 2 - State: {}".format(State.counter1)
        self.panel13.title = "Подпанель 3 - State: {}".format(State.counter1)
        self.panel14.title = "Подпанель 4 - State: {}".format(State.counter1)
        
        