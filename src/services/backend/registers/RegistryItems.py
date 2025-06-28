from src.entities.interfaces.game.Item import Item, ItemTypes
from src.services.backend.registers.Registry import Registry

class RegistryItems(Registry):
    """
    Регистратор предметов
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        super().__init__()
        
        self.setup_entities(Item, "items")
        
    def load_to_json(self):
        for item in self.items:
            self._json_view[item.id] = {
                "name": item.name,
                "description": item.description,
                "type": item.type,
                "rarity": item.rarity,
                "weight": item.weight,
                "price": item.price,
                "level_need": item.level_need
            }
            
            if item.type == ItemTypes.MATERIAL:
                self._json_view[item.id]["respawn_time"] = item.respawn_time