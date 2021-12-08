"""
Include two classes, Player class and System class.

Player class, lower level of System class, has class variable cards(string list), and bank(int).

System class, lower level of Pokergame class, manage the whole lower level of the game, take two Player() variables,
shuffle and deal the card to players, use Compare class to determine winner,  distribute money on table after
determining the winner.
"""
import copy
import random
from CONST import *
from compare import Compare

DEBUG = False


## Texas hold'em players
#
class Player:
    # hand card
    cards = []
    # how many money player have, start at 200
    bank = INITIAL_MONEY

    ## draw two cards
    #  @param len 2 string list
    #
    def get_card(self, card):
        self.cards = card

    ## raise the bet, take money from bank
    #  @param how many to raise
    def raise_bet(self, how_many):
        self.bank -= how_many


## Manage the whole lower level of the game
#
class System:

    min_wager = MINIMUM_WAGER   # minimum to raise, int
    pot = 0                     # total money on table, int
    deck = []                   # the deck, len 52 string list
    table_cards = []            # the cards on table, len 5 string list
    person = Player()           # person player, Player()
    com = Player()              # ai player, Player()

    # Turn1, start the game, players do action
    # Turn2, display first three table card, players do action
    # Turn3, display fourth table card, players do action
    # Turn4, display fifth table card, players do action
    # Turn5, player do actions, determine who's winner
    turn = 1                    # No. turn, int

    ## randomly shuffle deck list
    #
    def shuffle_deck(self):
        self.deck = copy.deepcopy(DECK)
        random.shuffle(self.deck)

        if DEBUG:
            print(self.deck)
            print(len(DECK))
            print(len(self.deck))
            print('Deck shuffled')

    ## pop five card from the shuffled deck then init the table cards list
    #
    def draw_card_to_table(self):
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        card3 = self.deck.pop()
        card4 = self.deck.pop()
        card5 = self.deck.pop()
        cards = [card1, card2, card3, card4, card5]
        self.table_cards = cards

        if DEBUG:
            print('Table cards', self.table_cards)

    ## pop two card from the shuffled deck then init the person card list
    #
    def draw_card_to_person(self):
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        card = [card1, card2]
        self.person.get_card(card)

        if DEBUG:
            print('Person cards', self.person.cards)

    ## pop two card from the shuffled deck then init the com card list
    #
    def draw_card_to_com(self):
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        card = [card1, card2]
        self.com.get_card(card)

        if DEBUG:
            print('Computer cards', self.com.cards)

    ## start the game, set turn to 1, shuffle the deck, draw cards
    #
    def game_start(self):
        self.turn = 1
        self.shuffle_deck()
        self.draw_card_to_table()
        self.draw_card_to_person()
        self.draw_card_to_com()
        self.person.bank -= self.min_wager
        self.com.bank -= self.min_wager
        self.pot += self.min_wager * 2

        if DEBUG:
            print('')
            print('Game start')
            print('Turn:', self.turn)
            print('Minimum wager is', self.min_wager)
            print('Pot is', self.pot)
            print('Person bank', self.person.bank)
            print('Com bank', self.com.bank)
            print('')

    ## fold process, person lose, all money on table give to ai
    #
    def fold_process(self):
        self.com.bank += self.pot
        self.pot = 0

        if DEBUG:
            print('Turn:', self.turn)
            print('Person fold')
            print('')

    ## Go to next turn
    #
    def check_process(self):
        if DEBUG:
            print('Turn:', self.turn)
            print('Person check')
            print('Com check')
            print('')

        self.turn += 1

    ## Person enter a value to raise , Com will match the raise, all money go to pot, then go next turn
    #
    def raise_process(self, how_many):
        if DEBUG:
            print('Turn:', self.turn)

        self.person.raise_bet(how_many)
        self.com.raise_bet(how_many)
        self.pot += how_many * 2

        if DEBUG:
            print('Com match')
            print('Person raise')
            print('Pot is $', self.pot)
            print('Person bank is $', self.person.bank)
            print('Com bank is $', self.com.bank)
            print('')

        self.turn += 1

    ## Check if one of two players lose all money
    def lose_all(self):
        if self.person.bank == 0 or self.com.bank == 0:
            return True
        else:
            return False

    ## Determine winner function
    #
    def is_person_win(self):
        # put table cards and player's card together
        person_seven_cards = self.table_cards + self.person.cards
        com_seven_cards = self.table_cards + self.com.cards

        # use Compare class
        c = Compare(person_seven_cards, com_seven_cards)

        result = c.result()

        # if result is TIE, players take back their bet on table
        if result == TIE:
            self.person.bank += self.pot // 2
            self.com.bank += self.pot // 2
            self.pot = 0
            return TIE

        # if person WIN, person get all money on table
        elif result == WIN:
            self.person.bank += self.pot
            self.pot = 0
            return WIN

        # if person LOSE, com get all money on table
        elif result == LOSE:
            self.com.bank += self.pot
            self.pot = 0
            return LOSE
