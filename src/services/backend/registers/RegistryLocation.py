from typing import List
import src.entities.models.locations as loc_package
from src.entities.interfaces.game import Location
import pkgutil
import importlib
import inspect
from .RegistryItems import RegistryItems

class RegistryLocation:
    """
    Регистратор локаций
    """
    locations: List[Location] = []

    for finder, name, ispkg in pkgutil.walk_packages(loc_package.__path__, loc_package.__name__ + "."):
        module = importlib.import_module(name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Location) and obj is not Location:
                locations.append(obj())

    _json_view = {}
        
    @staticmethod
    def load_to_json():
        for location in RegistryLocation.locations:
            RegistryLocation._json_view[location.id] = {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "region": location.region,
                "connections": location.connections,
                "resources": location.resources 
            }
            
        RegistryLocation.process_connections()
        RegistryLocation.process_resources()
            
    @staticmethod
    def get_json_view():
        return RegistryLocation._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryLocation._json_view.get(id, None)
    
    
    @staticmethod
    def process_resources():
        for location in RegistryLocation._json_view:
            _data = {}
            for x in RegistryLocation._json_view[location]["resources"]:
                item = RegistryItems.get_by_id(x)
                _data[x] = {
                    "id": x,
                    "name": item['name'],
                    "type": item['type'],
                    "rarity": item['rarity'],
                    "weight": item['weight'],
                    "amount": RegistryLocation._json_view[location]["resources"][x]["amount"],
                    "level_need": item['level_need']
                }
            
            RegistryLocation._json_view[location]["resources"] = _data
    
    @staticmethod
    def process_connections():
        for location in RegistryLocation._json_view:
            _data = {}
            for x in RegistryLocation._json_view[location]["connections"]:
                loc = RegistryLocation.get_by_id(x)
                _data[x] = {
                    "id": x,
                    "name": loc['name'],
                    "level": loc['connections'][location]['level']
                }
            
            RegistryLocation._json_view[location]["connections"] = _data