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
    
    def move_to_location(self, location_id: str):
        from src.Game import Game
        """
        Перемещение игрока в указанную локацию
        
        Args:
            location_id: ID локации
        """
        self.current_location = location_id
        self.current_region = Game.get_location_by_id(location_id)["region"]