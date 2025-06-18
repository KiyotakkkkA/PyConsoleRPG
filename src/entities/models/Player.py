from src.services.events import EventListener
from src.entities.interfaces import Serializable, Computable

class Player(EventListener, Computable, Serializable):
    def __init__(self):
        super().__init__()
        self.is_new = True
        self.initial_location = "main_ruins_of_origins"
        self.initial_region = "main_tierenhall_kingdom"
        self.initial_name = 'BASE_PLAYER'
        
        self.reactive('name', self.initial_name)
        
        self.reactive('base_location_relax_time', 5)
        self.reactive('base_speed', 1)
        
        self.reactive('inventory', {})
        
        self.reactive('base_constitution', 10) # Телосложение - влияет на здоровье
        self.reactive('base_intelligence', 10) # Интеллект - влияет на Аструм (ману)
        self.reactive('base_endurance', 10) # Выносливость - влияет на Энергию (стамину)
        
        self.reactive('additional_constitution', 0)
        self.reactive('additional_intelligence', 0)
        self.reactive('additional_endurance', 0)
        
        self.initial_level = 2
        
        self.current_location = None
        self.current_region = None
        self.current_level = None
        
        # Характеристики
        self.location_relax_time = self.base_location_relax_time
        self.computed('speed', lambda: self.base_speed, ['base_speed'])
        
        self.reactive('current_exp', 0)
        self.reactive('exp_to_next_level', 100)
        
        self.computed('total_constitution', lambda: self.additional_constitution + self.base_constitution, ['additional_constitution'])
        self.computed('total_intelligence', lambda: self.additional_intelligence + self.base_intelligence, ['additional_intelligence'])
        self.computed('total_endurance', lambda: self.additional_endurance + self.base_endurance, ['additional_endurance'])
        
        self.computed('max_health', lambda: (self.total_constitution) * 10, ['total_constitution'])
        self.computed('max_energy', lambda: (self.total_endurance) * 10, ['total_endurance'])
        self.computed('max_astrum', lambda: (self.total_intelligence) * 10, ['total_intelligence'])
        
        self.reactive('health', self.max_health)
        self.reactive('energy', self.max_energy)
        self.reactive('astrum', self.max_astrum)
        
        if self.is_new:
            self.current_location = self.initial_location
            self.current_region = self.initial_region
            self.current_level = self.initial_level
            
    def set_name(self, name: str):
        self.name = name
        self.emit_event("player_name_set", {"name": name})
            
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
        
    def collect_resource(self, resource_id: str):
        from src.Game import Game
        """
        Сбор ресурсов
        
        Args:
            resource_id: ID ресурса
        """
        loc = Game.get_location_by_id(self.current_location)
        amount = loc["resources"][resource_id]["amount"]
        loc["resources"][resource_id]["amount"] = 0
        
        Game.game_state.loc_res_meta[self.current_location] = Game.game_state.loc_res_meta.get(self.current_location, {})
        Game.game_state.loc_res_meta[self.current_location][resource_id] = {
            'amount': loc["resources"][resource_id]["amount"]
        }
        
        self._add_resource_to_inventory(resource_id, amount)
        self.emit_event("player_collect_resource", {"resource_id": resource_id, "amount": amount})
        
    def _add_resource_to_inventory(self, resource_id: str, amount: int):
        self.inventory[resource_id] = {
            "amount": self.inventory.get(resource_id, {}).get("amount", 0) + amount,
        }
        
    def _remove_resource_from_inventory(self, resource_id: str, amount: int):
        total = self.inventory.get(resource_id, {}).get("amount", 0)
        if total < amount:
            return False
        
        self.inventory[resource_id]["amount"] -= amount
        
        if self.inventory[resource_id]["amount"] == 0:
            del self.inventory[resource_id]
        
        return True
        
        