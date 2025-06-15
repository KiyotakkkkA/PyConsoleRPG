from src.services.frontend.core import Screen
from src.services.frontend.ui.input import Input, Selector
from src.services.events import Keys
from src.services.output import Color

class SettingsScene(Screen):    
    def __init__(self):
        super().__init__()
        self.performance_vision = True
        
        self.bind_key(Keys.F1, self.toggle_performance_monitor)
        
    def toggle_performance_monitor(self):
        """Включение/выключение монитора производительности"""
        self.performance_vision = not self.performance_vision
        self.enable_performance_monitor(self.performance_vision)
        
    def init(self):
        
        opts = [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5",
        ]
        
        self.selector_none_current_none = Selector(10, 10, 20, 
                                 label_title="Selector: ",
                                 label_color=Color.RESET,
                                 label_selected_color=Color.BG_BRIGHT_YELLOW,
                                 label_active_color=Color.BG_BRIGHT_GREEN,
                                 selection_type="none-current-none",
                                 options=opts)
        
        self.selector_minus_current_plus = Selector(75, 10, 20, 
                                 label_title="Selector: ",
                                 label_color=Color.RESET,
                                 label_selected_color=Color.BG_BRIGHT_YELLOW,
                                 label_active_color=Color.BG_BRIGHT_GREEN,
                                 selection_type="minus-current-plus")
        
        self.selector_prev_current_next = Selector(150, 10, 20, 
                                 label_title="Selector: ",
                                 label_color=Color.RESET,
                                 label_selected_color=Color.BG_BRIGHT_YELLOW,
                                 label_active_color=Color.BG_BRIGHT_GREEN,
                                 selection_type="prev-current-next",
                                 options=opts)
        
        self.input = Input(10, 15, 20, 
                           label_title="Input: ",
                           label_color=Color.RESET,
                           label_selected_color=Color.BG_BRIGHT_YELLOW,
                           label_active_color=Color.BG_BRIGHT_GREEN,
                           input_color=Color.RESET,
                           input_selected_color=Color.RESET,
                           input_active_color=Color.RESET,
                           enter_type="text",
                           solo_key_brackets="br_angle")
        self.input.set_selected(False)
        
        self.add_child(self.selector_none_current_none)
        self.add_child(self.selector_minus_current_plus)
        self.add_child(self.selector_prev_current_next)
        self.add_child(self.input)
        
        self.selector_none_current_none.set_selected(False)
        self.selector_minus_current_plus.set_selected(False)
        self.selector_prev_current_next.set_selected(True)
        
        self.selector_none_current_none.set_active(False)
        self.selector_minus_current_plus.set_active(False)
        self.selector_prev_current_next.set_active(False)
        
    def update(self):
        pass