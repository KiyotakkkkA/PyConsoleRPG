from src.services.events import EventListener
from src.entities.interfaces import Serialiazble

class Player(EventListener, Serialiazble):
    def __init__(self):
        super().__init__()
        self._is_new = True
        self.initial_location = "main_ruins_of_origins"
        self.initial_region = "main_tierenhall_kingdom"
        
        self.base_location_relax_time = 5
        self.base_speed = 1
        self.initial_level = 1
        
        self.current_location = None
        self.current_region = None
        self.current_level = None
        
        # Характеристики
        self.current_level = None
        self.location_relax_time = self.base_location_relax_time
        self.speed = self.base_speed
        
        if self._is_new:
            self.current_location = self.initial_location
            self.current_region = self.initial_region
            self.current_level = self.initial_level
            
    def get_location_relax_time(self):
        return (1 / self.speed) * self.location_relax_time
    
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