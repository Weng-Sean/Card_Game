

class Players:
    def __init__(self, name):
        self.cards = []
        self.coin = 0
        self.name = name
        self.value = 0
        self.stand = False
        self.response = None
        self.thinking = 80
        self.attribute_pool = False
        self.finish_attribute = False
        self.round_coin = 0
        self.computer_amount = 0
        self.quit = False
        self.profile_img = "Eva_profile.JPG"

    def is_busted(self):
        global card_val
        self.value = 0
        is_A = False
        for card in self.cards:
            card_val = 0
            if card[1] == "J":
                card_val = 10
            elif card[1] == "Q":
                card_val = 10
            elif card[1] == "K":
                card_val = 10
            elif card[1] == "A":
                card_val = 11
                is_A = True

            else:
                card_val = card[1]

            self.value += card_val
        if self.value > 21 and is_A:
            self.value -= 10

        return self.value > 21

    def analysis_result(self):
        self.is_busted()
        if self.value < 15:
            return True
        else:
            return False

    def computer_attribute(self, game, base=0):
        if not self.finish_attribute:
            self.is_busted()
            self.computer_amount = 100 * 1.4 ** self.value
            true_amount = self.computer_amount // 10 * 10
            if self.value >= 18 or self.computer_amount > base / 4:
                if base > self.computer_amount:
                    self.computer_amount = base
                    true_amount = self.computer_amount // 10 * 10
                else:
                    game.base = true_amount
            else:
                self.quit = True
                return [0,0,0,0,0]


            self.coin -= true_amount
            game.pool += true_amount

            thousands = self.computer_amount // 1000
            self.computer_amount -= thousands * 1000
            five_hundreds = self.computer_amount // 500
            self.computer_amount -= five_hundreds * 500
            hundreds = self.computer_amount // 100
            self.computer_amount -= hundreds * 100
            twenties = self.computer_amount // 20
            self.computer_amount -= twenties * 20
            tens = self.computer_amount // 10
            self.computer_amount -= tens * 10


            return [thousands, five_hundreds, hundreds, twenties, tens]


