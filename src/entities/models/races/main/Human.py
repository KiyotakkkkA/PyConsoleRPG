from src.entities.interfaces.game import Race

class Human(Race):
    def __init__(self):
        super().__init__()
        self.id = "main_human"
        self.name = "main_human.name"
        self.description = "main_human.description"
        
        self.base_constitution = 10
        self.base_intelligence = 10
        self.base_endurance = 10