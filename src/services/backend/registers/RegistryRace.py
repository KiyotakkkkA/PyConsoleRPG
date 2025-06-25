from typing import List
from src.entities.interfaces.game import Race
from src.services.backend.managers import ContentManager
from src.services.backend.managers import LocaleManager
import pkgutil
import importlib
import inspect

class RegistryRace:
    """
    Регистратор рас
    """
    
    _content_manager = ContentManager().get_instance()
    _json_view = {}
    
    races: List[Race] = []
    locale_manager = LocaleManager()
    races_dir = _content_manager.get_modules("races")
    
    for race_dir in races_dir:
        for finder, name, ispkg in pkgutil.walk_packages(race_dir.__path__, race_dir.__name__ + "."):
            module = importlib.import_module(name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Race) and obj is not Race:
                    races.append(obj())
    
    @staticmethod
    def load_to_json():
        for race in RegistryRace.races:
            RegistryRace._json_view[race.id] = {
                "id": race.id,
                "name": RegistryRace.locale_manager[f"races.{race.name}"],
                "description": RegistryRace.locale_manager[f"races.{race.description}"],
                
                'race_chars': {
                    'constitution': race.base_constitution,
                    'intelligence': race.base_intelligence,
                    'endurance': race.base_endurance
                }
            }
            
    @staticmethod
    def get_json_view():
        return RegistryRace._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryRace._json_view.get(id, None)