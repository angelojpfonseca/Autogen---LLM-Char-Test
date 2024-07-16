characters = {
    "orc": {
        "name": "Orc",
        "type": "humanoid (orc)",
        "size": "Medium",
        "alignment": "chaotic evil",
        "armor_class": 13,
        "hit_points": 15,
        "hit_dice": "2d8+6",
        "speed": "30 ft.",
        "abilities": {
            "STR": {"score": 16, "modifier": 3},
            "DEX": {"score": 12, "modifier": 1},
            "CON": {"score": 16, "modifier": 3},
            "INT": {"score": 7, "modifier": -2},
            "WIS": {"score": 11, "modifier": 0},
            "CHA": {"score": 10, "modifier": 0}
        },
        "skills": {"Intimidation": 2},
        "senses": {"Darkvision": "60 ft."},
        "languages": ["Common", "Orc"],
        "challenge_rating": "1/2",
        "xp": 100,
        "traits": {
            "Aggressive": "As a bonus action, the orc can move up to its speed toward a hostile creature that it can see."
        },
        "actions": [
            {
                "name": "Greataxe",
                "description": "Melee Weapon Attack: +5 to hit, reach 5 ft., one target.",
                "attack_bonus": 5,
                "damage_dice": "1d12",
                "damage_bonus": 3
            }
        ]
    },
    "goblin": {
        "name": "Goblin",
        "type": "humanoid (goblinoid)",
        "size": "Small",
        "alignment": "neutral evil",
        "armor_class": 15,
        "hit_points": 7,
        "hit_dice": "2d6",
        "speed": "30 ft.",
        "abilities": {
            "STR": {"score": 8, "modifier": -1},
            "DEX": {"score": 14, "modifier": 2},
            "CON": {"score": 10, "modifier": 0},
            "INT": {"score": 10, "modifier": 0},
            "WIS": {"score": 8, "modifier": -1},
            "CHA": {"score": 8, "modifier": -1}
        },
        "skills": {"Stealth": 6},
        "senses": {"Darkvision": "60 ft."},
        "languages": ["Common", "Goblin"],
        "challenge_rating": "1/4",
        "xp": 50,
        "traits": {
            "Nimble Escape": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."
        },
        "actions": [
            {
                "name": "Scimitar",
                "description": "Melee Weapon Attack: +4 to hit, reach 5 ft., one target.",
                "attack_bonus": 4,
                "damage_dice": "1d6",
                "damage_bonus": 2
            },
            {
                "name": "Shortbow",
                "description": "Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target.",
                "attack_bonus": 4,
                "damage_dice": "1d6",
                "damage_bonus": 2
            }
        ]
    }
}