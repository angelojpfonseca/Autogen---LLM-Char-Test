from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Ability:
    score: int
    modifier: int

@dataclass
class Action:
    name: str
    description: str
    attack_bonus: Optional[int] = None
    damage_dice: Optional[str] = None
    damage_bonus: Optional[int] = None

@dataclass
class CharacterSheet:
    name: str
    type: str
    size: str
    alignment: str
    armor_class: int
    hit_points: int
    hit_dice: str
    speed: str
    abilities: Dict[str, Ability]
    skills: Dict[str, int]
    senses: Dict[str, str]
    languages: List[str]
    challenge_rating: str
    xp: int
    traits: Dict[str, str]
    actions: List[Action]

    def __post_init__(self):
        self.passive_perception = 10 + self.abilities['WIS'].modifier + self.skills.get('Perception', 0)

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "size": self.size,
            "alignment": self.alignment,
            "armor_class": self.armor_class,
            "hit_points": self.hit_points,
            "hit_dice": self.hit_dice,
            "speed": self.speed,
            "abilities": {k: {"score": v.score, "modifier": v.modifier} for k, v in self.abilities.items()},
            "skills": self.skills,
            "senses": self.senses,
            "languages": self.languages,
            "challenge_rating": self.challenge_rating,
            "xp": self.xp,
            "traits": self.traits,
            "actions": [
                {
                    "name": action.name,
                    "description": action.description,
                    "attack_bonus": action.attack_bonus,
                    "damage_dice": action.damage_dice,
                    "damage_bonus": action.damage_bonus
                } for action in self.actions
            ],
            "passive_perception": self.passive_perception
        }

    @classmethod
    def from_dict(cls, data):
        data['abilities'] = {k: Ability(**v) for k, v in data['abilities'].items()}
        data['actions'] = [Action(**action) for action in data['actions']]
        return cls(**data)