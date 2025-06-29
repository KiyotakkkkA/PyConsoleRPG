from src.entities.interfaces.game import Location
from src.services.backend.registers.Registry import Registry

class RegistryLocation(Registry):
    """
    Регистратор локаций
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    
    def __init__(self):
        super().__init__()
        
        self.setup_entities(Location, "locations")
      
    def load_to_json(self):
        for location in self.locations:
            self._json_view[location.id] = {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "region": location.region,
                "connections": location.connections,
                "resources": location.resources,
                "npcs": location.npcs
            }
            
        self.process_connections()
        self.process_resources()
    
    def process_resources(self):
        for location in self._json_view:    
            _data = {}
            for x in self._json_view[location]["resources"]:
                _data[x] = {
                    "id": x,
                    "amount": self._json_view[location]["resources"][x]["amount"],
                }
            
            self._json_view[location]["resources"] = _data
    
    def process_connections(self):
        for location in self._json_view:
            _data = {}
            for x in self._json_view[location]["connections"]:
                loc = self.get_by_id(x)
                _data[x] = {
                    "id": x,
                    "name": loc['name'],
                    "level": loc['connections'][location]['level']
                }
            
            self._json_view[location]["connections"] = _data