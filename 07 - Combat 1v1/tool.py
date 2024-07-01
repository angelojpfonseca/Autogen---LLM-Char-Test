import random

def roll_attack(attacker, attack_bonus, target_ac, weapon_damage, target):
    # Roll a d20
    attack_roll = random.randint(1, 20)
    
    # Add attack bonus
    total_attack = attack_roll + attack_bonus
    
    # Check if attack is successful
    if total_attack > target_ac:
        # Roll for damage
        damage = random.randint(1, weapon_damage)
        return f"{attacker} rolled {attack_roll} for a total of {total_attack}. It hits the {target} and causes {damage} damage."
    else:
        return f"{attacker} rolled {attack_roll} for a total of {total_attack}. It misses the {target}."

# Tool definition
attack_tool = {
    "name": "roll_attack",
    "description": "Rolls an attack action, determining if the attack hits and calculating damage if successful.",
    "input_schema": {
        "type": "object",
        "properties": {
            "attacker": {
                "type": "string",
                "description": "The name of the character making the attack."
            },
            "attack_bonus": {
                "type": "integer",
                "description": "The attack bonus of the attacker."
            },
            "target_ac": {
                "type": "integer",
                "description": "The Armor Class (AC) of the target."
            },
            "weapon_damage": {
                "type": "integer",
                "description": "The maximum damage of the weapon (e.g., 6 for a d6, 12 for a d12)."
            },
            "target": {
                "type": "string",
                "description": "The name of the target being attacked."
            }
        },
        "required": ["attacker", "attack_bonus", "target_ac", "weapon_damage", "target"]
    }
}

def take_damage(target, damage, current_hp):
    new_hp = max(current_hp - damage, 0)
    
    if new_hp == 0:
        return f"{target} has been defeated!"
    else:
        return f"{target} took {damage} damage. New HP: {new_hp}"

# Tool definition
damage_tool = {
    "name": "take_damage",
    "description": "Simulates a character taking damage in an RPG. Reduces the character's HP and determines if they've been defeated.",
    "input_schema": {
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "The name of the character taking damage."
            },
            "damage": {
                "type": "integer",
                "minimum": 0,
                "description": "The amount of damage being dealt."
            },
            "current_hp": {
                "type": "integer",
                "minimum": 0,
                "description": "The current HP of the target before taking damage."
            }
        },
        "required": ["target", "damage", "current_hp"]
    }
}


