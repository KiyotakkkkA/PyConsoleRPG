from typing import List
from src.entities.interfaces.game import Region
from src.services.backend.managers import ContentManager
import pkgutil
import importlib
import inspect

class RegistryRegion:
    """
    Регистратор регионов
    """
    
    _content_manager = ContentManager().get_instance()
    _json_view = {}
    
    regions: List[Region] = []
    regions_dir = _content_manager.get_modules("regions")
    
    for regions_dir in regions_dir:
        for finder, name, ispkg in pkgutil.walk_packages(regions_dir.__path__, regions_dir.__name__ + "."):
            module = importlib.import_module(name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Region) and obj is not Region:
                    regions.append(obj())
        
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