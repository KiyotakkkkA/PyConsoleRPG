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

class AncientOakCrossing(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_ancient_oak_crossing"
        self.region = "main_great_elmira_forest"
        
        self.name = "Перепутье Древнего Дуба"
        self.description = "Огромный вековой дуб стоит на перекрёстке лесных троп, его кора покрыта таинственными рунами."
        self.connections = {
            "main_sleeping_glade": {
                "level": 3
            },
            "main_curve_way": {
                "level": None
            }
        }