import random
from character_data import characters

def simulate_melee_attack(attacker_name, defender_name):
    attacker = characters[attacker_name.lower()]
    defender = characters[defender_name.lower()]
    
    # Find the melee attack action
    melee_action = next(action for action in attacker.actions if "Melee Weapon Attack" in action.description)
    
    # Roll for attack
    attack_roll = random.randint(1, 20)
    total_attack = attack_roll + melee_action.attack_bonus
    
    # Determine if it's a hit
    is_hit = total_attack >= defender.armor_class
    
    # Prepare the output
    output = f"Melee Attack: {attacker.name} attacks {defender.name} with {melee_action.name}\n"
    output += f"Attack Roll: {attack_roll} (d20) + {melee_action.attack_bonus} (bonus) = {total_attack}\n"
    output += f"Defender's AC: {defender.armor_class}\n"
    output += f"Result: {'Hit' if is_hit else 'Miss'}\n"
    
    if is_hit:
        # Roll for damage
        damage_rolls, damage_total = roll_dice(melee_action.damage_dice)
        total_damage = damage_total + melee_action.damage_bonus
        
        # Update defender's HP
        defender.hit_points = max(0, defender.hit_points - total_damage)

        output += f"Damage Roll: {damage_rolls} ({melee_action.damage_dice}) + {melee_action.damage_bonus} = {total_damage}\n"
        output += f"{defender.name}'s new HP: {defender.hit_points}\n"
    
    return output

def simulate_ranged_attack(attacker_name, defender_name):
    attacker = characters[attacker_name.lower()]
    defender = characters[defender_name.lower()]
    
    # Find the ranged attack action
    ranged_action = next(action for action in attacker.actions if "Ranged Weapon Attack" in action.description)
    
    # Roll for attack
    attack_roll = random.randint(1, 20)
    total_attack = attack_roll + ranged_action.attack_bonus
    
    # Determine if it's a hit
    is_hit = total_attack >= defender.armor_class
    
    # Prepare the output
    output = f"Ranged Attack: {attacker.name} attacks {defender.name} with {ranged_action.name}\n"
    output += f"Attack Roll: {attack_roll} (d20) + {ranged_action.attack_bonus} (bonus) = {total_attack}\n"
    output += f"Defender's AC: {defender.armor_class}\n"
    output += f"Result: {'Hit' if is_hit else 'Miss'}\n"
    
    if is_hit:
        # Roll for damage
        damage_rolls, damage_total = roll_dice(ranged_action.damage_dice)
        total_damage = damage_total + ranged_action.damage_bonus
        
        # Update defender's HP
        defender.hit_points = max(0, defender.hit_points - total_damage)

        output += f"Damage Roll: {damage_rolls} ({ranged_action.damage_dice}) + {ranged_action.damage_bonus} = {total_damage}\n"
        output += f"{defender.name}'s new HP: {defender.hit_points}\n"
    
    return output

def roll_dice(dice_string):
    num_dice, sides = map(int, dice_string.split('d'))
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    return rolls, sum(rolls)

tools = [
    {
        "name": "simulate_melee_attack",
        "description": "Simulates a D&D 5e melee attack, including attack roll, damage calculation, and HP update.",
        "input_schema": {
            "type": "object",
            "properties": {
                "attacker": {
                    "type": "string",
                    "description": "The name of the attacking character."
                },
                "defender": {
                    "type": "string",
                    "description": "The name of the defending character."
                }
            },
            "required": ["attacker", "defender"]
        }
    },
    {
        "name": "simulate_ranged_attack",
        "description": "Simulates a D&D 5e ranged attack, including attack roll, damage calculation, and HP update.",
        "input_schema": {
            "type": "object",
            "properties": {
                "attacker": {
                    "type": "string",
                    "description": "The name of the attacking character."
                },
                "defender": {
                    "type": "string",
                    "description": "The name of the defending character."
                }
            },
            "required": ["attacker", "defender"]
        }
    }
]