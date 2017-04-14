from deck import Deck

class DealerBrain(object):
    def __init__(self):
        self.deck = Deck()

    def calculate_value(self, hand):
        value = 0
        ace_count = 0
        status = None

        for card in hand:
            if card == "ac" or card == "ad" or card == "ah" or card == "as":
                ace_count += 1
            else:
                value += self.deck.values[card]

        while(ace_count > 0):
            if value + (ace_count * 11) > 21:
                value += 1
                ace_count -= 1
            else:
                value += ace_count * 11

        if value == 21 and len(hand) == 2:
            status = "blackjack"
            response = "You got blackjack!"
        elif value <= 21 and len(hand) == 5:
            status = "five-card"
            response = "You've five-carded'!"
        elif value == 21:
            status = "21"
            response = "You got 21!"
        elif value > 21:
            status = "busted"
            response = "You've busted!"

        return value, status, response
