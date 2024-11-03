from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class ResourceType(Enum):
    METAL = "metal"
    COPPER = "copper"
    WIRES = "wires"
    PLASTIC = "plastic"
    ELECTRONICS = "electronics"
    BATTERIES = "batteries"
    URANIUM = "uranium"
    FUEL = "fuel"
    COUPONS = "coupons"
    ENGRAVED_SHELLS = "engraved_shells"

class BattleType(Enum):
    PVP = "pvp"
    PVE = "pve"
    RAID = "raid"
    ADVENTURE = "adventure"

@dataclass
class Resources:
    metal: int = 0
    copper: int = 0
    wires: int = 0
    plastic: int = 0
    electronics: int = 0
    batteries: int = 0
    uranium: int = 0
    fuel: int = 0
    coupons: int = 0
    engraved_shells: int = 0

@dataclass
class GameState:
    level: int = 1
    power_score: int = 0
    resources: Resources = Resources()
    current_faction: str = "Engineers"
    faction_levels: Dict[str, int] = None
    available_parts: List[str] = None
    current_build: Dict[str, int] = None
    
    def __post_init__(self):
        if self.faction_levels is None:
            self.faction_levels = {"Engineers": 1}
        if self.available_parts is None:
            self.available_parts = []
        if self.current_build is None:
            self.current_build = {}

    def update_resources(self, resource_type: ResourceType, amount: int):
        """Update resource amounts"""
        current = getattr(self.resources, resource_type.value)
        setattr(self.resources, resource_type.value, current + amount)

    def can_craft(self, item_id: str, recipe: Dict[ResourceType, int]) -> bool:
        """Check if we have enough resources to craft an item"""
        for resource_type, amount in recipe.items():
            if getattr(self.resources, resource_type.value) < amount:
                return False
        return True

    def get_optimal_battle_type(self) -> BattleType:
        """Determine best battle type based on current state"""
        if self.level < 4:
            return BattleType.PVP
        elif self.fuel >= 20 and self.level >= 4:
            return BattleType.RAID
        elif self.power_score >= 4000:
            return BattleType.PVP
        return BattleType.ADVENTURE