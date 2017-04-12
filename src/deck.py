from random import randint

class Deck(object):
    def __init__(self):
        self.cards = [
                        "2c", "2d", "2h", "2s",
                        "3c", "3d", "3h", "3s",
                        "4c", "4d", "4h", "4s",
                        "5c", "5d", "5h", "5s",
                        "6c", "6d", "6h", "6s",
                        "7c", "7d", "7h", "7s",
                        "8c", "8d", "8h", "8s",
                        "9c", "9d", "9h", "9s",
                        "10c", "10d", "10h", "10s",
                        "jc", "jd", "jh", "js",
                        "qc", "qd", "qh", "qs",
                        "kc", "kd", "kh", "ks",
                        "ac", "ad", "ah", "as",
                     ]

        self.values = {
                        "2c": 2, "2d": 2, "2h": 2, "2s": 2,
                        "3c", "3d", "3h", "3s",
                        "4c", "4d", "4h", "4s",
                        "5c", "5d", "5h", "5s",
                        "6c", "6d", "6h", "6s",
                        "7c", "7d", "7h", "7s",
                        "8c", "8d", "8h", "8s",
                        "9c", "9d", "9h", "9s",
                        "10c", "10d", "10h", "10s",
                        "jc", "jd", "jh", "js",
                        "qc", "qd", "qh", "qs",
                        "kc", "kd", "kh", "ks",
                        "ac", "ad", "ah", "as",
                     }

    def draw(self):
        return self.cards.pop(randint(0, len(self.cards) - 1))

    def empty(self):
        if len(self.cards) == 0:
            return True
        return False
