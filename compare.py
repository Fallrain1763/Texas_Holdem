"""
Compare class, lower level of System class, take two length 7 string list to construct , the result() method inside will
use the functions in compare_functions to return an int which represents the result.
"""
from compare_functions import *

DEBUG = False


## compare two 7 card list base on Texas hold'em rules
#
class Compare:
    ## CTOR
    #  @param person's 7 cards, len 7 string list
    #  @param com's 7 cards, len 7 string list
    #
    def __init__(self, person, com):
        self._person = person
        self._com = com

    ## compare the person and com's card
    #  @return TIE, WIN, or LOSE, const int
    #
    def result(self):
        person_great_value_hand = largest_hand_in_seven(self._person)
        com_great_value_hand = largest_hand_in_seven(self._com)

        if DEBUG:
            print(person_great_value_hand)
            print(com_great_value_hand)
            print('')

        return compare_hand(person_great_value_hand, com_great_value_hand)
