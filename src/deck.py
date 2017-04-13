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
                        "3c": 3, "3d": 3, "3h": 3, "3s": 3,
                        "4c": 4, "4d": 4, "4h": 4, "4s": 4,
                        "5c": 5, "5d": 5, "5h": 5, "5s": 5,
                        "6c": 6, "6d": 6, "6h": 6, "6s": 6,
                        "7c": 7, "7d": 7, "7h": 7, "7s": 7,
                        "8c": 8, "8d": 8, "8h": 8, "8s": 8,
                        "9c": 9, "9d": 9, "9h": 9, "9s": 9,
                        "10c": 10, "10d": 10, "10h": 10, "10s": 10,
                        "jc": 10, "jd": 10, "jh": 10, "js": 10,
                        "qc": 10, "qd": 10, "qh": 10, "qs": 10,
                        "kc": 10, "kd": 10, "kh": 10, "ks": 10
                     }

    def draw(self):
        return self.cards.pop(randint(0, len(self.cards) - 1))

    def empty(self):
        if len(self.cards) == 0:
            return True
        return False
