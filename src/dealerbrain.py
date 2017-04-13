from deck import Deck

class DealerBrain(object):
    def __init__(self):
        self.deck = Deck()

    def calculate_value(self, hand):
        value = 0

        for card in hand:
            if card == "ac" or card == "ad" or card == "ah" or card == "as":
                if value + 11 > 21:
                    value += 1
                else:
                    value += 11
            else:
                value += self.deck.values[card]

        return value
