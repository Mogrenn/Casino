from enum import Enum
import random
import os

clear = lambda: os.system("clear")


class Bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Suit(Enum):
    """Docstring for Round."""

    CLUBS = "CLUBS"
    HEARTS = "HEARTS"
    DIAMONDS = "DIAMONDS"
    SPADES = "SPADES"


class Rank(Enum):
    """Docstring for Round."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card():
    """Docstring for Card."""

    def __init__(self, suit, rank):
        """Docstring for Round."""
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return "{:s} of {}".format(self.rank.name, self.suit.name)

    def get_card(self):
        """Docstring for Card."""
        return [self.rank.name, self.suit.name]

    def get_value(self):
        """Retunera värdet på kortet"""
        return self.rank.value

    def get_rank(self):
        """Retunerar namnet på kortet"""
        return self.rank


class Game():

    def __init__(self, dealer, players):
        self.dealer = dealer
        self.players = players
        self.deck = self.shuffle_deck()
        self.round = ""

    def __str__(self):
        return "{}".format(self.players[0])

    def shuffle_deck(self):
        """Skapar en ny kortlek med 52 kort i och slumpar ordningen på den"""
        temp = [Card(suit, rank) for rank in Rank for suit in Suit]
        random.shuffle(temp)
        return temp

    def start_round(self):
        clear()
        self.round = Round(self.deck, self.dealer, self.players)
        self.take_bets()

        print()
        print("New round: 1")
        print("Cashout: 2")
        if int(input("Enter Command")) == 1:
            self.start_round()

    def take_bets(self):
        self.round.take_bets()

    def deal_players(self):
        pass


class Round():

    def __init__(self, deck, dealer, players):
        self.deck = deck
        self.dealer = dealer
        self.players = players
        self.pot = 0

    def take_bets(self):
        for x in range(0, len(self.players)):
            print("Player chips are ", self.players[x].get_chips())
            bet = int(input("How much you want to bet: "))
            self.players[x].set_chips(self.players[x].get_chips() - bet)
            self.pot += bet
            self.players[x].set_bet(self.players[x].get_bet()+bet)
        else:
            self.deal_round()

    def deal_round(self):

        for i in range(0, 2):
            self.dealer.add_card_to_hand(self.deck[0])
            del self.deck[0]
            for j in range(0, len(self.players)):
                self.players[j].add_card_to_hand(self.deck[0])
                del self.deck[0]

        self.print_dealer_hand_and_value()

    def print_dealer_hand_and_value(self):
        print("Dealer card is", self.dealer.get_face_up_card(), " and value ", self.dealer.get_face_up_card_value())
        self.action_round()

    def action_round(self):
        for i in range(0, len(self.players)):
            not_bust = False
            while not not_bust:
                print(self.players[i].get_hand(), "and value ", self.players[i].get_hand_value())
                print()
                print("What do you want to do :")
                print("Hit: 1")
                print("Stand: 2")
                print("Double Down: 3")
                print("Split: 4")
                command = int(input("Enter Command :"))
                if int(command) != 2:
                    self.translate_command(command, self.players[i])
                else:
                    not_bust = True

                if self.players[i].get_hand_value() > 21:
                    print(self.players[i].get_hand(), "and value ", self.players[i].get_hand_value())
                    not_bust = True

                elif command == 3:
                    not_bust = True

        self.dealers_round()

    def translate_command(self, command, player):
        if int(command) == 1:
            self.hit(player)
        elif int(command) == 3:
            self.double_down(player)

    def hit(self, player):
        player.add_card_to_hand(self.deck[0])
        del self.deck[0]

    def double_down(self, player):
        player.set_bet(player.get_bet()*2)
        self.hit(player)

    def split(self, player):
        pass

    def dealers_round(self):
        print("Dealer hand is ", self.dealer.get_hand(), "and vale is", self.dealer.get_hand_value())
        while self.dealer.get_hand_value() < 17:
            self.dealer.add_card_to_hand(self.deck[0])
            del self.deck[0]
            print("Dealer hand is ", self.dealer.get_hand(), "and vale is", self.dealer.get_hand_value())

        self.finish_round()

    def finish_round(self):
        clear()

        for i in range(0, len(self.players)):

            # if player gets a blackjack
            if self.players[i].get_hand_value() == 21 and self.dealer.get_hand_value != 21:
                print(Bcolors.GREEN + "You got Blackjack" + Bcolors.WHITE)
                self.blackjack(self.players[i])

            # if player busts
            elif self.players[i].get_hand_value() > 21:
                print(Bcolors.GREEN + "Dealer hand is ", self.dealer.get_hand())
                print(Bcolors.RED + "Your hand is ", self.players[i].get_hand(), "" + Bcolors.WHITE)
                self.lost(self.players[i])

            # if house is bust
            elif self.dealer.get_hand_value() > 21:
                print(Bcolors.RED + "Dealer hand is ", self.dealer.get_hand())
                print(Bcolors.GREEN + "Your hand is ", self.players[i].get_hand(), "" + Bcolors.WHITE)
                self.payout(self.players[i])

            # player hand is better then house and not bust
            elif self.players[i].get_hand_value() > self.dealer.get_hand_value():
                print(Bcolors.RED + "Dealer hand is ", self.dealer.get_hand())
                print(Bcolors.GREEN + "Your hand is ", self.players[i].get_hand(), "" + Bcolors.WHITE)
                self.payout(self.players[i])

            # player hand is worse then house and not bust
            elif self.players[i].get_hand_value() < self.dealer.get_hand_value():
                print(Bcolors.GREEN + "Dealer hand is ", self.dealer.get_hand())
                print(Bcolors.RED + "Your hand is ", self.players[i].get_hand(), "" + Bcolors.WHITE)
                self.lost(self.players[i])

            # player and house have the same value
            else:
                print(Bcolors.YELLOW + "Dealer hand is ", self.dealer.get_hand())
                print("Your hand is ", self.players[i].get_hand(), "" + Bcolors.WHITE)
                self.push(self.players[i])

    def payout(self, player):
        player.set_chips(player.get_chips() + player.get_bet()*2)
        player.set_bet(0)

    def blackjack(self, player):
        player.set_chips(player.get_chips() + player.get_bet()*2.5)
        player.set_bet(0)

    def push(self, player):
        player.set_chips(player.get_chips() + player.get_bet())
        player.set_bet(0)

    def lost(self, player):
        player.set_bet(0)


class Player():

    def __init__(self):
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        value = 0
        for i in range(0, len(self.hand)):
            if self.hand[i].get_value() <= 10:
                value += self.hand[i].get_value()
            elif self.hand[i].get_value() > 10:
                value += 10

        for i in range(0, len(self.hand)):
            if self.hand[i].get_rank() == Rank.ACE:
                if value + 10 > 21:
                    pass
                elif value > 21:
                    value -= 10
                else:
                    value += 10

        return value

    def get_hand(self):
        return self.hand


class Dealer(Player):

    def __init__(self, totalchips):
        super().__init__()
        self.totalChips = totalchips

    def get_totalchips(self):
        return self.totalChips

    def set_totalchips(self, amount):
        self.totalChips = amount

    def get_face_up_card_value(self):
        return self.hand[1].rank.value if self.hand[1].rank.value <= 10 else 10 if self.hand[1].rank.name != Rank.ACE else 11

    def get_face_up_card(self):
        return self.hand[1]


class Gambler(Player):

    def __init__(self, name, chips):
        super().__init__()
        self.name = name
        self.chips = chips
        self.bet = 0

    def __str__(self):
        return "{} chips left: {}".format(self.name, self.chips)

    def get_chips(self):
        return self.chips

    def set_chips(self, amount):
        self.chips = int(amount)

    def get_bet(self):
        return self.bet

    def set_bet(self, amount):
        self.bet = amount


gambler = Gambler("Brandon", 200)
dealer = Dealer(4000)
game = Game(dealer, [gambler])
game.start_round()
