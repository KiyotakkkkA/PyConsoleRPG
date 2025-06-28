from src.entities.interfaces.game import Region
from src.services.backend.registers.Registry import Registry

class RegistryRegion(Registry):
    """
    Регистратор регионов
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        super().__init__()
        
        self.setup_entities(Region, "regions")
        
    def load_to_json(self):
        for region in self.regions:
            self._json_view[region.id] = {
                "name": region.name,
                "description": region.description
        }