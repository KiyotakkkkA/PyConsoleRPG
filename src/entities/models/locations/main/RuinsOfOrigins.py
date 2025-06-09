from src.entities.interfaces.game import Location

class RuinsOfOrigins(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_ruins_of_origins"
        self.region = "main_tierenhall_kingdom"
        
        self.name = "Руины Истоков"
        self.description = "Забытое разрушенное святилище, некогда служившее местом для старинных ритуалов"
        self.connections = {
            "main_curve_way": {
                "level": None
            }
        }
        
        self.resources = {
            "material_the_thorn": {
                "amount": 1
            },
            "material_silver_lichen": {
                "amount": 3
            }
        }