from combat.simulator import CombatSimulator
from entities.character import Character

def main():
    # Create a combat simulator with a 20x10 map
    simulator = CombatSimulator(map_width=20, map_height=10)

    # Add characters
    simulator.add_character(Character("Orc Warrior", 15, 30, 1, 5, "1d12", 3, 30))
    simulator.add_character(Character("Elven Archer", 14, 25, 3, 4, "1d8", 2, 35))
    simulator.add_character(Character("Human Cleric", 16, 28, 0, 3, "1d6", 1, 25))
    simulator.add_character(Character("Dwarf Fighter", 17, 35, -1, 6, "2d6", 4, 25))

    # Run the simulation
    simulator.simulate_combat()

if __name__ == "__main__":
    main()