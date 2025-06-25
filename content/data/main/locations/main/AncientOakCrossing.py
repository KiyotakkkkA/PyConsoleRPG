from src.entities.interfaces.game import Location

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