from deck import Deck

class DealerBrain(object):
    def __init__(self):
        self.deck = Deck()

    def calculate_value(self, hand):
        value = 0
        ace_count = 0
        status = None
        response = None

        for card in hand:
            if card == "ac" or card == "ad" or card == "ah" or card == "as":
                ace_count += 1
            else:
                value += self.deck.values[card]

        while(ace_count > 0):
            if value + 11 <= 21:
                value += 11
                ace_count -= 1
            else:
                value += ace_count * 1
                ace_count = 0

        if value == 21 and len(hand) == 2:
            status = "blackjack"
            response = "You got blackjack!"
        elif value <= 21 and len(hand) == 5:
            status = "five-card"
            response = "You've five-carded!"
        elif value == 21:
            status = "21"
            response = "You got 21!"
        elif value > 21:
            status = "busted"
            response = "You've busted!"

        return value, status, response

    def calculate_decision(self, players, hard):
        fives = 0
        fours = 0
        twos = 0
        num_players = 0
        deck = Deck()

        for player in players:
            if player.get('name') != "Dealer":
                for card in player.get('hand'):
                    if card != player.get('hand')[1]:
                        deck.remove(card)
                if player.get('status') != None and player.get('bet') != None:
                    num_players += 1
                    if len(player.get('hand')) > 4:
                        fives += 1
                    if len(player.get('hand')) == 4:
                        fours += 1
                    if len(player.get('hand')) == 2:
                        twos += 1

        for player in players:
            if player.get('name') == "Dealer":
                for card in player.get('hand'):
                    deck.remove(card)
                odds = deck.odds_of_busting(21 - player.get('hand_value'))

                # Normal AI
                if hard == False:
                    if odds <= 65:
                        return 1
                    else:
                        return 0

                # Hard AI
                else:
                    # Percent of players that prob got 17+
                    stayed_at_2 = int(float(twos/num_players) * 100)
                    # Percent of players that prob busted
                    stayed_at_4 = int(float(fours/num_players) * 100)
                    stayed_at_5 = int(float(fives/num_players) * 100)
                    if stayed_at_2 == 100 and player.get('hand_value') < 19:
                        return 1
                    if stayed_at_2 >= 50 and player.get('hand_value') < 18:
                        if odds <= 65:
                            return 1
                        elif stayed_at_2 < 70:
                            if odds <= 65:
                                return 1
                    if stayed_at_4 > 50:
                        if fives > 0 and odds < 70 and num_players < 5:
                            return 1
                        else:
                            return 0
