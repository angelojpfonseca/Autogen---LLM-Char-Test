# main.py
from dotenv import load_dotenv
from agents import DM, NPC
from tools import attack_roll, defend

load_dotenv()

def run_combat(dm, npc1, npc2, rounds):
    for round in range(1, rounds + 1):
        dm.narrate(f"Round {round} begins!")
        
        # NPC1 attacks NPC2
        attack_result = attack_roll(npc1.name, npc2.name, npc1.attack_bonus, npc1.damage_dice)
        npc1_action = npc1.act("attack", **attack_result)
        dm.narrate(npc1_action['description'])
        
        defense_result = defend(npc2.name, npc2.ac, npc2.hp, attack_result['total_attack'], attack_result['damage'])
        npc2_action = npc2.act("defend", **defense_result)
        dm.narrate(npc2_action['description'])
        
        npc2.hp = defense_result['new_hp']
        
        if npc2.hp <= 0:
            dm.narrate(f"{npc2.name} has been defeated!")
            return
        
        # NPC2 attacks NPC1
        attack_result = attack_roll(npc2.name, npc1.name, npc2.attack_bonus, npc2.damage_dice)
        npc2_action = npc2.act("attack", **attack_result)
        dm.narrate(npc2_action['description'])
        
        defense_result = defend(npc1.name, npc1.ac, npc1.hp, attack_result['total_attack'], attack_result['damage'])
        npc1_action = npc1.act("defend", **defense_result)
        dm.narrate(npc1_action['description'])
        
        npc1.hp = defense_result['new_hp']
        
        if npc1.hp <= 0:
            dm.narrate(f"{npc1.name} has been defeated!")
            return
        
        dm.narrate(f"End of round {round}. {npc1.name} HP: {npc1.hp}, {npc2.name} HP: {npc2.hp}")

if __name__ == "__main__":
    dm = DM()
    warrior = NPC("Warrior", 15, 30, 5, "2d6+3")
    rogue = NPC("Rogue", 13, 25, 4, "1d8+3")
    
    dm.narrate("Welcome, brave warriors! Today, we have two formidable opponents facing each other in combat. On one side, we have the stalwart Warrior, clad in heavy armor with a mighty greatsword in hand. On the other, we have the nimble Rogue, dressed in light leather armor and wielding a sharp rapier.")
    dm.narrate("Let the battle commence!")
    
    run_combat(dm, warrior, rogue, 5)
    
    dm.narrate("The combat has ended. Thank you for your valiant efforts, warriors!")