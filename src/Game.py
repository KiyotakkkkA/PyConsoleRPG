from src.services.backend.registers import RegistryLocation, RegistryRegion, RegistryItems
from src.entities.models import Player
from src.app.scenes import MainScene, GameScene, SettingsScene
from src.services.frontend.core import ScreenManager
from src.config import Config
import time

class Game:
    DEBUG = True
    
    screen_manager = ScreenManager()
    
    # Регистрация сущностей
    _entity_registry = {
        "items": RegistryItems,
        "locations": RegistryLocation,
        "regions": RegistryRegion,
    }
    
    # Регистрация экранов
    _screens = {
        "main": MainScene,
        "game": GameScene,
        "settings": SettingsScene
    }
    
    _current_screen = None
    
    # Игрок
    player = Player()
    
    game_state = {
        "current_location_data": lambda: Game.locations.get(Game.player.current_location),
        "current_region_data": lambda: Game.regions.get(Game.player.current_region),
        "location_relax_time": lambda: Game.player.get_location_relax_time(),
        "current_relax_time": 0,
        "start_time": 0.0,
        "frame_count": 0,
        "last_update_time": 0.0
    }
    
    @classmethod
    def time_count_with_fps(cls):
        cls.game_state["frame_count"] += 1
        current_time = time.time()
        elapsed_time = current_time - cls.game_state["last_update_time"]
        
        cls.game_state["last_update_time"] = current_time
        cls.game_state["current_relax_time"] -= elapsed_time
        if cls.game_state["current_relax_time"] < 0:
            cls.game_state["current_relax_time"] = 0
    
    @classmethod
    def get_location_by_id(cls, location_id: str):
        """
        Получение локации по ID
        
        Args:
            location_id: ID локации
        """
        return RegistryLocation.get_by_id(location_id)
    
    @classmethod
    def get_item_by_id(cls, item_id: str):
        """
        Получение предмета по ID
        
        Args:
            item_id: ID предмета
        """
        return RegistryItems.get_by_id(item_id)

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
    
    @classmethod
    def init(cls):
        cls._register_entities()
        cls._register_screens()
        
        cls.screen_manager.navigate_to_screen("main")