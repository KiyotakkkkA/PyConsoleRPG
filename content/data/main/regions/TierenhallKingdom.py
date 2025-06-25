from src.entities.interfaces.game import Region

class TierenhallKingdom(Region):
    def __init__(self):
        super().__init__()
        self.id = "main_tierenhall_kingdom"
        self.name = "Королевство Тиренхолл"
        self.description = "Огромное королевство, расположившееся на западе континента. Обладает особой культурой и развитой экономикой."