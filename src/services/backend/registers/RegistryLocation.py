from typing import List
from src.entities.models.locations import *
from src.entities.interfaces.game import Location

class RegistryLocation:
    locations: List[Location] = [
        RuinsOfOrigins(),
        CurveWay()
    ]
    
    _json_view = {}
        
    @staticmethod
    def load_to_json():
        for location in RegistryLocation.locations:
            RegistryLocation._json_view[location.id] = {
                "name": location.name,
                "description": location.description
            }
            
    @staticmethod
    def get_json_view():
        return RegistryLocation._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryLocation._json_view.get(id, None)