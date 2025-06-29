from src.entities.interfaces.game.NPC import NPC
from src.services.backend.registers.Registry import Registry

class RegistryNPC(Registry):
    """
    Регистратор NPC
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        super().__init__()
        
        self.setup_entities(NPC, "npcs")
        
    def load_to_json(self):
        for npc in self.npcs:
            self._json_view[npc.id] = {
                "name": self._locale_manager[f"npcs.{npc.name}"],
            }