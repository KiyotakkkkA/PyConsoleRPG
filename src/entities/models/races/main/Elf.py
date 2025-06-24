from src.entities.interfaces.game import Race

class Elf(Race):
    def __init__(self):
        super().__init__()
        self.id = "main_elf"
        self.name = "main_elf.name"
        self.description = "main_elf.description"
        
        self.base_constitution = 6
        self.base_intelligence = 12
        self.base_endurance = 12
