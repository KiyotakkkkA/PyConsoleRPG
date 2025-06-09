from src.entities.interfaces.game import Location


class CurveWay(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_curve_way"
        self.region = "main_great_elmira_forest"
        
        self.name = "Извилистая тропа"
        self.description = "Поросший мхом и кустарниками путь, ведущий сквозь Великий Лес"
        self.connections = {
            "main_ruins_of_origins": {
                "level": None
            },
            "main_ancient_oak_crossing": {
                "level": None
            },
            "main_sleeping_glade": {
                "level": 3
            }
        }