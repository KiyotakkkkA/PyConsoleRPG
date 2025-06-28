from src.entities.interfaces.game import Race
from src.services.backend.registers.Registry import Registry

class RegistryRace(Registry):
    """
    Регистратор рас
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        super().__init__()
        
        self.setup_entities(Race, "races")
    
    def load_to_json(self):
        for race in self.races:
            self._json_view[race.id] = {
                "id": race.id,
                "name": self._locale_manager[f"races.{race.name}"],
                "description": self._locale_manager[f"races.{race.description}"],
                
                'race_chars': {
                    'constitution': race.base_constitution,
                    'intelligence': race.base_intelligence,
                    'endurance': race.base_endurance
                }
        }