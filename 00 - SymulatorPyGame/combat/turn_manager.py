class TurnManager:
    def __init__(self, characters):
        self.characters = characters
        self.turn_order = []
        self.current_turn = 0
        self.round = 1

    def roll_initiative(self):
        for character in self.characters:
            character.roll_initiative()
        self.turn_order = sorted(self.characters, key=lambda x: x.initiative, reverse=True)

    def next_turn(self):
        self.current_turn += 1
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
            self.round += 1
            for character in self.characters:
                character.reset_turn()
        return self.turn_order[self.current_turn]

    def get_current_character(self):
        return self.turn_order[self.current_turn]