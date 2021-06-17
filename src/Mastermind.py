import random
from models.Color import Color
from models.Game import Game
from models.Pin import Pin


class Mastermind:

    def __init__(self, Game):
        self.Game = Game

    def make_code(self):
        secret_code = []
        for x in range(self.Game.number_of_colors):
            color = self.get_random_color()

            if not self.Game.duplicate_color:
                while color in secret_code:
                    color = self.get_random_color()

            secret_code.append(color)

        Game.code = secret_code
        return secret_code

    def get_random_color(self):
        return Color(random.randint(0, self.Game.number_of_colors - 1))

    def get_all_results(self):
        pins = Pin.query.filter_by(game_id=self.Game.id).all()

        sorted_pins = self.sort_pins(pins)

        all_results = []

        for key in sorted_pins.keys():
            all_results.append(self.guess_the_code(sorted_pins[key]))

        return all_results

    def sort_pins(self, pins):
        sorted_pins = {}
        for pin in pins:
            key_list = sorted_pins.keys()
            if pin.y in key_list:
                pin_array = sorted_pins[pin.y]
                pin_array.append(pin)
            else:
                sorted_pins[pin.y] = [pin]

        return sorted_pins

    def guess_the_code(self, guessed_code):
        result = {
            "in_but_not_correct": 0,
            "correct": 0,
        }

        # ToDo: fix bug with duplicate colors
        for guessed_colors in range(len(guessed_code)):
            if self.Game.code[guessed_colors] == guessed_code[guessed_colors]:
                result["correct"] += 1
            else:
                for color in range(len(self.Game.code)):
                    if self.Game.code[color] == guessed_code[guessed_colors]:
                        if guessed_colors == color:
                            result["correct"] += 1
                        else:
                            result["in_but_not_correct"] += 1
                        break
        return result

    def did_player_win(self, result):
        if Game.number_of_positions == result["correct"]:
            return True

        return False
