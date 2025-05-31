from src.entities.interfaces.game import Location

class RuinsOfOrigins(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_ruins_of_origins"
        self.region = "main_tierenhall_kingdom"
        
        self.name = "Руины Истоков"
        self.description = "Забытое разрушенное святилище, некогда служившее местом для проведения диковинных ритуалов"


class CurveWay(Location):
    def __init__(self):
        super().__init__()
        self.id = "main_curve_way"
        self.region = "main_great_elmira_forest"
        
        self.name = "Извилистая тропа"
        self.description = "Поросший мхом и кустарниками путь, ведущий сквозь Великий Лес"