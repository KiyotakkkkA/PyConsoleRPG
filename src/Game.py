from src.services.backend.registers import RegistryLocation, RegistryRegion
from src.entities.models import Player
from src.app.scenes import MainScene, GameScene, SettingsScene
from src.services.frontend.core import ScreenManager


class Game:
    DEBUG = True
    
    screen_manager = ScreenManager()
    
    # Регистрация сущностей
    _entity_registry = {
        "locations": RegistryLocation,
        "regions": RegistryRegion
    }
    
    # Регистрация экранов
    _screens = {
        "main": MainScene(),
        "game": GameScene(),
        "settings": SettingsScene()
    }
    
    # Игрок
    player = Player()

    @classmethod
    def _register_entities(cls):
        """
        Регистрация сущностей
        """
        if cls.DEBUG:
            print("[INFO] Регистрация сущностей...")
        for name, registry in cls._entity_registry.items():
            registry.load_to_json()
            setattr(cls, name, registry.get_json_view())
        if cls.DEBUG:
            print("[INFO] Сущности зарегистрированы.")
            
    @classmethod
    def _register_screens(cls):
        """
        Регистрация экранов
        """
        if cls.DEBUG:
            print("[INFO] Регистрация экранов...")
        cls.screen_manager.add_screens(cls._screens)
        if cls.DEBUG:
            print("[INFO] Экраны зарегистрированы.")
    
    # Игровое состояние
    game_state = {
        "current_location_name": lambda: Game.player.current_location,
        "current_location_data": lambda: Game.locations.get(Game.player.current_location),
        "current_region_name": lambda: Game.player.current_region,
        "current_region_data": lambda: Game.regions.get(Game.player.current_region)
    }
    
    @classmethod
    def init(cls):
        cls._register_entities()
        cls._register_screens()
        cls.screen_manager.set_current_screen("main")