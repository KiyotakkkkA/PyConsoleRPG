class Player:
    def __init__(self):
        self._is_new = True
        self.initial_location = "main_ruins_of_origins"
        self.initial_region = "main_tierenhall_kingdom"
        
        self.current_location = None
        self.current_region = None
        
        if self._is_new:
            self.current_location = self.initial_location
            self.current_region = self.initial_region