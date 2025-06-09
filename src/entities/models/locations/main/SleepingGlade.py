from src.entities.interfaces.game import Location

class SleepingGlade(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_sleeping_glade"
        self.region = "main_great_elmira_forest"
        
        self.name = "Поляна сновидений"
        self.description = "Странная поляна, усеянная цветами, наполняющими воздух сладковатым ароматом спокойствия и дремоты"
        self.connections = {
            "main_curve_way": {
                "level": 3
            },
            "main_ancient_oak_crossing": {
                "level": 3
            }
        }