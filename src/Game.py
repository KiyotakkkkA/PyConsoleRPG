from src.services.backend.registers import RegistryLocation, RegistryRegion, RegistryItems
from src.entities.models import Player
from src.entities.interfaces import Serializable
from src.app.scenes import MainScene, GameScene, SettingsScene, NewGameScreen, LoadGameScreen
from src.services.frontend.core import ScreenManager
import time
import json
import os

class GameState(Serializable):
    """
    Класс для хранения состояния игры
    """
    
    def __init__(self):
        super().__init__()
        
        self.__exclude__.add("computable")
        
        self.computable = {
            "current_location_data": lambda: Game.locations.get(Game.player.current_location),
            "current_region_data": lambda: Game.regions.get(Game.player.current_region),
            "location_relax_time": lambda: Game.player.get_location_relax_time(),
        }
        
        self.state = {
            "current_relax_time": 0,
            "start_time": 0.0,
            "frame_count": 0,
            "last_update_time": 0.0
        }
        
        # Метаданные локаций (где сколько ресурсов и т.д.)
        self.loc_res_meta = {
            
        }


class Game:
    
    __allowed_ext__ = [".json"]
    
    DEBUG = True
    
    SAVES_DIR = 'saves'
    GAME_WAS_LOADED_SUCCESSFULLY = False
    CURRENT_LOADING_PLAYER = None
    
    # Игрок
    player = Player()
    
    # Состояние игры
    game_state = GameState()
    
    # Регистрация сущностей
    entity_registry = {
        "items": RegistryItems,
        "locations": RegistryLocation,
        "regions": RegistryRegion,
    }
    
    # Регистрация экранов
    screens = {
        "main": MainScene,
        "game": GameScene,
        "settings": SettingsScene,
        "new_game": NewGameScreen,
        "load_game": LoadGameScreen
    }
    
    # Экраны
    screen_manager = ScreenManager()
    
    # Текущий экран
    current_screen = None
    
    @classmethod
    def add_json_meta_file(cls, file_path: str, data: dict):
        if os.path.splitext(file_path)[1] not in cls.__allowed_ext__:
            raise ValueError(f"Недопустимый формат файла: {os.path.splitext(file_path)[1]}")
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    @classmethod
    def new_game(cls, new_player_data: dict):
        cls.player = Player()
        cls.game_state = GameState()
        
        cls.player.set_name(new_player_data['name'])
        
        cls.GAME_WAS_LOADED_SUCCESSFULLY = True
        cls.save()
        cls.screen_manager.navigate_to_screen("game")
    
    @staticmethod
    def save():
        if not Game.GAME_WAS_LOADED_SUCCESSFULLY: return
        if not os.path.exists(f"{Game.SAVES_DIR}/{Game.player.name}"):
            os.makedirs(f"{Game.SAVES_DIR}/{Game.player.name}")
        Game.player.dump_to_file(f"{Game.SAVES_DIR}/{Game.player.name}/playerdata.json")
        Game.game_state.dump_to_file(f"{Game.SAVES_DIR}/{Game.player.name}/gamestate.json")
        
        Game.add_json_meta_file(f"{Game.SAVES_DIR}/{Game.player.name}/meta.json", {
            "player_name": Game.player.name,
            'player_level': Game.player.current_level,
            'last_save_time': time.time(),
        })
        
    @staticmethod
    def _load_set_resources_amount():
        for loc in Game.game_state.loc_res_meta:
            for res in Game.game_state.loc_res_meta[loc]:
                Game.locations[loc]["resources"][res]["amount"] = Game.game_state.loc_res_meta[loc][res]["amount"]
    
    @staticmethod
    def load():
        PLAYER_DATA_LOAD = False
        GAME_STATE_LOAD = False
        if os.path.exists(f"{Game.SAVES_DIR}/{Game.CURRENT_LOADING_PLAYER}/playerdata.json"):
            Player.apply(Game.player, f"{Game.SAVES_DIR}/{Game.CURRENT_LOADING_PLAYER}/playerdata.json")
            PLAYER_DATA_LOAD = True
        if os.path.exists(f"{Game.SAVES_DIR}/{Game.CURRENT_LOADING_PLAYER}/gamestate.json"):
            GameState.apply(Game.game_state, f"{Game.SAVES_DIR}/{Game.CURRENT_LOADING_PLAYER}/gamestate.json")
            Game._load_set_resources_amount()
            GAME_STATE_LOAD = True
        
        Game.GAME_WAS_LOADED_SUCCESSFULLY = PLAYER_DATA_LOAD and GAME_STATE_LOAD and Game.CURRENT_LOADING_PLAYER is not None
        return Game.GAME_WAS_LOADED_SUCCESSFULLY
    
    @classmethod
    def time_count_with_fps(cls):
        cls.game_state.state["frame_count"] += 1
        current_time = time.time()
        elapsed_time = current_time - cls.game_state.state["last_update_time"]
        
        cls.game_state.state["last_update_time"] = current_time
        cls.game_state.state["current_relax_time"] -= elapsed_time
        if cls.game_state.state["current_relax_time"] < 0:
            cls.game_state.state["current_relax_time"] = 0
    
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
        for name, registry in cls.entity_registry.items():
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
        cls.screen_manager.add_screens(cls.screens)
        if cls.DEBUG:
            print("[INFO] Экраны зарегистрированы.")
    
    @classmethod
    def init(cls):
        cls._register_entities()
        cls._register_screens()
        
        cls.screen_manager.navigate_to_screen("main")