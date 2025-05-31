from typing import List
from src.entities.models.regions import *
from src.entities.interfaces.game import Region

class RegistryRegion:
    regions: List[Region] = [
        TierenhallKingdom(),
        GreatElmiraForest(),
        SwardenfallEmpire()
    ]
    
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