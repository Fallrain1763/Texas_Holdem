"""
Manage all const values, include color codes, deck list, file paths, hand types, and compare results.
"""

# Deck string ;ist
DECK = ['1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c',
        '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d',
        '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h',
        '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s']

# Deck file path
DECK_DIR = 'DECK'

# BGM file path
BGM_DIR = 'AUDIO/17 - The White Lady.mp3'

# Players' start up money
INITIAL_MONEY = 200

# Minimum value to raise
MINIMUM_WAGER = 10

# Volume
VOLUME = 0.5

# Results
TIE = 0
WIN = 1
LOSE = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 86, 95)
PURPLE = (235, 15, 255)
GOLD = (255, 215, 0)
CYAN = (31, 248, 255)
BROWN = (114, 77, 44)
ORANGE = (242, 133, 0)
GRAY = (169, 169, 169)

# Hands
HIGH_CARD = 0
PAIR = 1
TWO_PAIRS = 2
THREE_OF_A_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OF_A_KIND = 7
STRAIGHT_FLUSH = 8
ROYAL_FLUSH = 9
