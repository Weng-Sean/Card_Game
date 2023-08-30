from cards import Cards
import pickle
from players import Players
import random

class Game:
    def __init__(self, players):
        self.players = []
        for player in players:
            self.players.append(Players(player))
        self.Card = Cards(self.players)
        self.initial_cards()
        self.initial_coin_data()
        self.pool = 0
        self.pool_token = []
        self.base = 0
        self.click = False
        self.turn = random.choice(self.players)
        self.winner = []
        self.final = False



    def initial_cards(self):
        for player in self.players:
            player.cards.append(self.Card.random_card())
            #print(player.name, player.cards)

    def initial_coin_data(self):
        with open("coin_history.txt", "rb") as f:
            data = f.read()
            coin_data = pickle.loads(data)
        for player in self.players:
            player.coin = coin_data[player.name]

    def add_cards(self, player=None):
        if not player:
            if not self.players[0].is_busted():
                self.players[0].cards.append(self.Card.random_card())
        else:
            player.cards.append(self.Card.random_card())

    def deduct_coins(self, amount, player=None):
        if not player:
            self.players[0].coin -= amount

    def next_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        elif self.turn == self.players[1]:
            self.turn = self.players[2]
        else:
            self.turn = self.players[0]

    def money_result(self):
        if not self.final:
            if self.winner:
                winner_num = len(self.winner)
                for player in self.winner:
                    player.coin += self.pool / winner_num
                self.final = True
                return True
        return False
