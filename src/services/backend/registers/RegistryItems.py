from typing import List
import src.entities.models.items as items_package
from src.entities.interfaces.game.Item import Item
import pkgutil
import importlib
import inspect

class RegistryItems:
    """
    Регистратор предметов
    """
    
    items: List[Item] = []
    
    for finder, name, ispkg in pkgutil.walk_packages(items_package.__path__, items_package.__name__ + "."):
        module = importlib.import_module(name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Item) and obj is not Item:
                items.append(obj())
    
    _json_view = {}
        
    @staticmethod
    def load_to_json():
        for item in RegistryItems.items:
            RegistryItems._json_view[item.id] = {
                "name": item.name,
                "description": item.description,
                "type": item.type,
                "rarity": item.rarity,
                "weight": item.weight,
                "price": item.price,
                "level_need": item.level_need
            }
            
    @staticmethod
    def get_json_view():
        return RegistryItems._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryItems._json_view.get(id, None)