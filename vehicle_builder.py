from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
import numpy as np

class VehiclePart(Enum):
    FRAME = "frame"
    CABIN = "cabin"
    WEAPON = "weapon"
    WHEEL = "wheel"
    MODULE = "module"
    ARMOR = "armor"
    DECOR = "decor"

@dataclass
class PartProperties:
    durability: float
    weight: float
    power_score: int
    explosion_damage: Optional[float] = None
    is_explosive: bool = False

class VehicleBuilder:
    def __init__(self, max_parts: int, max_weight: float):
        self.max_parts = max_parts
        self.max_weight = max_weight
        self.current_parts = []
        self.total_weight = 0.0
        self.power_score = 0
        self.working_side = "front"
        
    def validate_part_placement(self, part: VehiclePart, position: Dict[str, float]) -> bool:
        """Validate if part can be placed at given position"""
        # Check weight limit
        if self.total_weight + part.weight > self.max_weight:
            return False
            
        # Check parts limit
        if len(self.current_parts) >= self.max_parts:
            return False
            
        # Check for explosive parts proximity
        if part.is_explosive:
            return self._check_explosive_safety(position)
            
        return True
        
    def _check_explosive_safety(self, position: Dict[str, float]) -> bool:
        """Check if position is safe for explosive components"""
        MIN_SAFE_DISTANCE = 2.0
        
        for existing_part in self.current_parts:
            if existing_part.is_explosive:
                distance = self._calculate_distance(position, existing_part.position)
                if distance < MIN_SAFE_DISTANCE:
                    return False
        return True
        
    def optimize_armor_placement(self) -> List[Dict[str, float]]:
        """Calculate optimal armor placement positions"""
        armor_positions = []
        
        # Prioritize working side
        if self.working_side == "front":
            armor_positions.extend(self._get_front_armor_positions())
        elif self.working_side == "back":
            armor_positions.extend(self._get_back_armor_positions())
        
        # Protect explosive components
        armor_positions.extend(self._get_module_protection_positions())
        
        return armor_positions
        
    def _get_front_armor_positions(self) -> List[Dict[str, float]]:
        """Calculate front armor positions"""
        positions = []
        # Add armor positions to protect cabin and critical components
        # Center protection
        positions.append({"x": 0, "y": 2, "z": 1})  # Front center
        positions.append({"x": -1, "y": 2, "z": 1})  # Front left
        positions.append({"x": 1, "y": 2, "z": 1})   # Front right
        return positions
        
    def _get_module_protection_positions(self) -> List[Dict[str, float]]:
        """Calculate positions to protect modules"""
        positions = []
        for part in self.current_parts:
            if part.is_explosive:
                # Add armor positions around explosive component
                pos = part.position
                positions.extend([
                    {"x": pos["x"], "y": pos["y"] + 1, "z": pos["z"]},  # Front
                    {"x": pos["x"], "y": pos["y"] - 1, "z": pos["z"]},  # Back
                    {"x": pos["x"] + 1, "y": pos["y"], "z": pos["z"]},  # Right
                    {"x": pos["x"] - 1, "y": pos["y"], "z": pos["z"]}   # Left
                ])
        return positions
        
    def calculate_power_score(self) -> int:
        """Calculate vehicle's power score"""
        total_ps = 0
        for part in self.current_parts:
            total_ps += part.power_score
        return total_ps
        
    def optimize_weapon_placement(self, weapon_type: str) -> List[Dict[str, float]]:
        """Calculate optimal weapon placement based on weapon type"""
        if weapon_type == "autocannon":
            return self._get_autocannon_positions()
        elif weapon_type == "rocket":
            return self._get_rocket_positions()
        return []
        
    def _get_autocannon_positions(self) -> List[Dict[str, float]]:
        """Get optimal autocannon placement positions"""
        # Place autocannons with good firing angles
        return [
            {"x": 0, "y": 1, "z": 1.5},   # Center mount
            {"x": -1.5, "y": 0, "z": 1.5}, # Left side
            {"x": 1.5, "y": 0, "z": 1.5}   # Right side
        ]