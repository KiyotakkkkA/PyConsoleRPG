from src.entities.interfaces.game import NPC

class MysticStatue(NPC):
    def __init__(self):
        super().__init__()
        
        self.id = "main_mystic_statue"
        self.name = "main_mystic_statue.name"