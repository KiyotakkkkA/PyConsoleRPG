from src.entities.interfaces.game import Region    

class GreatElmiraForest(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_great_elmira_forest"
        self.name = "Великий Эльмирский лес"
        self.description = "Великий лес, расположенный в середине континента. Является естественной границей между Королевством Тиренхолл и Империей Сварденфолл."