from typing import List
import src.entities.models.regions as reg_package
from src.entities.interfaces.game import Region
import pkgutil
import importlib
import inspect

class RegistryRegion:
    """
    Регистратор регионов
    """
    
    regions: List[Region] = []
    
    for finder, name, ispkg in pkgutil.walk_packages(reg_package.__path__, reg_package.__name__ + "."):
        module = importlib.import_module(name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Region) and obj is not Region:
                regions.append(obj())
    
    _json_view = {}
        
    @staticmethod
    def load_to_json():
        for region in RegistryRegion.regions:
            RegistryRegion._json_view[region.id] = {
                "name": region.name,
                "description": region.description
            }
            
    @staticmethod
    def get_json_view():
        return RegistryRegion._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryRegion._json_view.get(id, None)