from src.services.events import EventListener

class Player(EventListener):
    def __init__(self):
        super().__init__()
        self._is_new = True
        self.initial_location = "main_ruins_of_origins"
        self.initial_region = "main_tierenhall_kingdom"
        self.initial_level = 1
        
        self.current_location = None
        self.current_region = None
        self.current_level = None
        
        # Характеристики
        self.current_level = None
        
        if self._is_new:
            self.current_location = self.initial_location
            self.current_region = self.initial_region
            self.current_level = self.initial_level
    
    def move_to_location(self, location_id: str):
        from src.Game import Game
        """
        Перемещение игрока в указанную локацию
        
        Args:
            location_id: ID локации
        """
        self.current_location = location_id
        self.current_region = Game.get_location_by_id(location_id)["region"]
        
        self.emit_event("player_move", {"location_id": location_id})