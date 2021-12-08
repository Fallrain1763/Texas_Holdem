"""
Lower level of Compare class, has functions which could check hand type, compare two five cards list, and find the
largest five cards in seven cards.
"""
import collections
from CONST import *


## check which hand type is for this five cards
#  @param len 5 string, 5 cards
#  @return 0-9 int, rep High_card to Royal flush(in Const.py)
#
def check_hand(five_cards):
    # get cards' num and color
    nums = []
    colors = []

    # color is the last char in string
    # num is the rest of
    for card in five_cards:
        nums.append(int(card[:-1]))
        colors.append(card[-1:])

    # key is card num, value is the card num freq count
    cards_dic = dict()
    for num in nums:
        if num not in cards_dic.keys():
            cards_dic[num] = 1
        else:
            cards_dic[num] += 1

    # get the difference between highest freq count and low freq count
    diff_freq = max(cards_dic.values()) - min(cards_dic.values())

    # remove the dups in color and num list,get how many types
    colors_len = len(set(colors))
    nums_len = len(set(nums))

    # all card same color, and is 10 to acer
    if colors_len == 1 and sorted(nums) == [1, 10, 11, 12, 13]:
        return ROYAL_FLUSH
    # all card same color, all five card different, largest card is 4 more than smallest
    elif colors_len == 1 and nums_len == 5 and max(nums) - min(nums) == 4:
        return STRAIGHT_FLUSH
    # Four same - one == 3
    elif diff_freq == 3:
        return FOUR_OF_A_KIND
    # three same - two same = 1, 2 different num
    elif diff_freq == 1 and nums_len == 2:
        return FULL_HOUSE
    # all card sam color
    elif colors_len == 1:
        return FLUSH
    # all five card different, largest card is 4 more than smallest, ace is special here
    elif (nums_len == 5 and max(nums) - min(nums) == 4) or (sorted(nums) == [1, 10, 11, 12, 13]):
        return STRAIGHT
    # Three same - one = 2
    elif diff_freq == 2:
        return THREE_OF_A_KIND
    # Two same - one = 1, 3 different num
    elif diff_freq == 1 and nums_len == 3:
        return TWO_PAIRS
    # Two same - one = 1
    elif diff_freq == 1:
        return PAIR
    # elif diff_freq == 0
    else:
        return HIGH_CARD


## compare two group of five cards
#  @param len5 card string list
#  @param len5 card string list
#  @return TIE, LOSE or WIN, int
#
def compare_hand(cards1, cards2):
    """
     1. compare hand kind first, cards1> cards2, return WIN; < , return lose, = return TIE
     2. else compare the card list, use ten functions: compare_high_card() to compare_royal_flush
     3. these ten functions, cards1 > cards2, return WIN
    """
    cards1_type = check_hand(cards1)
    cards2_type = check_hand(cards2)

    if cards1_type > cards2_type:
        return WIN
    elif cards1_type < cards2_type:
        return LOSE
    else:
        if cards1_type == ROYAL_FLUSH or cards2_type == STRAIGHT_FLUSH or cards2_type == STRAIGHT:
            return compare_straight(cards1, cards2)
        else:
            return compare_non_straight(cards1, cards2)


## find the largest five cards in 21 combinations
#  @param seven cards list, len 7 string list
#  @return len 2 tuple, [0] is a len5 card list, [1] is int, rep hand kind,ex: (cardlist, HIGHCARD)
#
def largest_hand_in_seven(seven_cards):
    """
     1. list 21 different possible five cards in seven_card
     2. use compare_hand() and loop find the biggest value fivecard, and return it
    """

    # list all 21 possible
    twenty_one_possible = [[seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[4]],
                           [seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[5]],
                           [seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[6]],
                           [seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[4], seven_cards[5]],
                           [seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[4], seven_cards[6]],
                           [seven_cards[0], seven_cards[1], seven_cards[2], seven_cards[5], seven_cards[6]],
                           [seven_cards[0], seven_cards[1], seven_cards[3], seven_cards[4], seven_cards[5]],
                           [seven_cards[0], seven_cards[1], seven_cards[3], seven_cards[4], seven_cards[6]],
                           [seven_cards[0], seven_cards[1], seven_cards[3], seven_cards[5], seven_cards[6]],
                           [seven_cards[0], seven_cards[1], seven_cards[4], seven_cards[5], seven_cards[6]],
                           [seven_cards[0], seven_cards[2], seven_cards[3], seven_cards[4], seven_cards[5]],
                           [seven_cards[0], seven_cards[2], seven_cards[3], seven_cards[4], seven_cards[6]],
                           [seven_cards[0], seven_cards[2], seven_cards[3], seven_cards[5], seven_cards[6]],
                           [seven_cards[0], seven_cards[2], seven_cards[4], seven_cards[5], seven_cards[6]],
                           [seven_cards[0], seven_cards[3], seven_cards[4], seven_cards[5], seven_cards[6]],
                           [seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[4], seven_cards[5]],
                           [seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[4], seven_cards[6]],
                           [seven_cards[1], seven_cards[2], seven_cards[3], seven_cards[5], seven_cards[6]],
                           [seven_cards[1], seven_cards[2], seven_cards[4], seven_cards[5], seven_cards[6]],
                           [seven_cards[1], seven_cards[3], seven_cards[4], seven_cards[5], seven_cards[6]],
                           [seven_cards[2], seven_cards[3], seven_cards[4], seven_cards[5], seven_cards[6]]]

    # Max element in list algorithm
    largest_hand = twenty_one_possible[0]
    for cards in twenty_one_possible:
        if compare_hand(largest_hand, cards) == LOSE:
            largest_hand = cards

    return largest_hand


## Sort a list by elements' freq(more to less), if same freq, sort then by value
#  @param an int list
#  @return a sorted by freq int list
#
def sort_freq(lst):
    counts = collections.Counter(lst)
    sorted_list = sorted(lst, key=lambda x: (counts[x], x), reverse=True)
    return sorted_list


## Finding and replacing a specific element in a list
#  @param an int list
#  @param the element need to be replace, int
#  @param the element used for replacing, int
#  @return the replaced int list
#
def replace_all(lst, a, b):
    new_list = [b if element == a else element for element in lst]
    return new_list


## get nums from strings then sort the by freq
#  @param len5 string list
#  @param sorted int list
#
def get_nums(cards):
    nums = []
    for card in cards:
        nums.append(int(card[:-1]))

    # Sort a list by elements' freq(more to less), if same freq, sort then by value
    nums = sort_freq(nums)

    return nums


## compare two group of straight five cards(Royal flush, straight flush, straight)
#  @param len5 card string list
#  @param len5 card string list
#  @return TIE, LOSE or WIN, int
#
def compare_straight(cards1, cards2):
    # get cards' nums
    nums1 = get_nums(cards1)
    nums2 = get_nums(cards2)

    # same nums in straight means Tie
    if nums1 == nums2:
        return TIE
    # if not same and num1 is ace to 10, then Win
    elif nums1 == [13, 12, 11, 10, 1]:
        return WIN
    # if not same and num2 is ace to 10, then Lose
    elif nums2 == [13, 12, 11, 10, 1]:
        return LOSE
    # other than the ace to 10, the largest card decide how large is the straight
    elif max(nums1) > max(nums2):
        return WIN
    # elif max(nums1) < max(nums2):
    else:
        return LOSE


## compare two group of non_straight five cards(other than Royal flush, straight flush, straight)
#  @param len5 card string list
#  @param len5 card string list
#  @return TIE, LOSE or WIN, int
#
def compare_non_straight(cards1, cards2):
    # get cards' nums
    nums1 = get_nums(cards1)
    nums2 = get_nums(cards2)

    # replace all 1 to 100, because acer is
    nums1 = replace_all(nums1, 1, 100)
    nums2 = replace_all(nums2, 1, 100)

    if nums1 == nums2:
        return TIE

    # compare most freq values first, pair compare pair, three compare three
    # if same, compare next largest value, which the list is already sorted like that
    else:
        for i in range(5):
            if nums1[i] > nums2[i]:
                return WIN
            elif nums1[i] < nums2[i]:
                return LOSE

    return TIE
