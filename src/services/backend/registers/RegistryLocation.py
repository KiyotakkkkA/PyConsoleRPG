from typing import List
from src.entities.interfaces.game import Location
from src.services.backend.managers import ContentManager
import pkgutil
import importlib
import inspect

class RegistryLocation:
    """
    Регистратор локаций
    """
    _content_manager = ContentManager().get_instance()
    _json_view = {}
    
    locations: List[Location] = []
    locations_dir = _content_manager.get_modules("locations")
    
    for locations_dir in locations_dir:
        for finder, name, ispkg in pkgutil.walk_packages(locations_dir.__path__, locations_dir.__name__ + "."):
            module = importlib.import_module(name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Location) and obj is not Location:
                    locations.append(obj())
        
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
                _data[x] = {
                    "id": x,
                    "amount": RegistryLocation._json_view[location]["resources"][x]["amount"],
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