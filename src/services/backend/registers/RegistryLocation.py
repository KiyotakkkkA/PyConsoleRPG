from typing import List
from src.entities.models.locations import *
from src.entities.interfaces.game import Location

class RegistryLocation:
    locations: List[Location] = [
        RuinsOfOrigins(),
        CurveWay(),
        SleepingGlade(),
        AncientOakCrossing()
    ]
    
    _json_view = {}
        
    @staticmethod
    def load_to_json():
        for location in RegistryLocation.locations:
            RegistryLocation._json_view[location.id] = {
                "id": location.id,
                "name": location.name,
                "description": location.description,
                "region": location.region,
                "connections": location.connections
            }
            
        RegistryLocation.process_connections()
            
    @staticmethod
    def get_json_view():
        return RegistryLocation._json_view
    
    @staticmethod
    def get_by_id(id: str):
        return RegistryLocation._json_view.get(id, None)
    
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