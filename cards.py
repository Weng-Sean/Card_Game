import random
import pickle

class Cards:
    def __init__(self, players):
        self.cards_val = [ 'A', 'K', 'Q', 'J', 10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.cards_suits = ["Heart", "Club", "Diamond", "Spade"]
        self.cards = []
        for suit in self.cards_suits:
            for val in self.cards_val:
                self.cards.append([suit, val])
        self.available_card = [copy[:] for copy in self.cards]
        self.players = players

    def random_card(self):
        card = random.choice(self.available_card)
        self.available_card.remove(card)
        return card


my_coin = {
    "Sean": 100000,
    "Eva": 100000,
    "Computer": 100000,
}
with open("coin_history.txt", "wb") as f:
    f.write(pickle.dumps(my_coin))


