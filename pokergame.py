"""
Poker Game class, Highest level of the whole program, game itself, manage the display and user interaction,
take a System variable and manage lower level of game.
"""
import os
import sys
import pygame
from CONST import *
from system import System
from gamebase import GameBase, ImageSprite


## Game itself display and update image and text, take a System() var to manage lower level process
#
class PokerGame(GameBase):
    ## CTOR
    #
    def __init__(self):
        super().__init__(800, 600)

        # set window's name
        pygame.display.set_caption('Texas Hold\'em')

        # set a System variable to manage lower level process, game start when program run
        self._system = System()
        self._start = True
        self._system.game_start()

        ## Declare variables in CTOR
        # card_back
        self._card_back1 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back2 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back3 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back4 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back5 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back6 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._card_back7 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        # Person hand card
        self._person_card1 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._person_card2 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        # Com hand card
        self._com_card1 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._com_card2 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        # table card
        self._table_card1 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._table_card2 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._table_card3 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._table_card4 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        self._table_card5 = ImageSprite(0, 0, DECK_DIR + '/j.gif')
        # text need to be displayed, result text set to white first, will reload after
        self._font = pygame.font.Font('freesansbold.ttf', 20)
        self._text_fold = self._font.render('Press J to \"FOLD\"', True, BLACK)
        self._text_check = self._font.render('Press K to \"CHECK\"', True, BLACK)
        self._text_raise = self._font.render('Press L to \"RAISE\"', True, BLACK)
        self._text_next = self._font.render('Press RETURN for next game', True, WHITE)
        self._text_lose = self._font.render('You lose!', True, WHITE)
        self._text_win = self._font.render('You win!', True, WHITE)
        self._text_tie = self._font.render('Tie.', True, WHITE)
        self._text_person = self._font.render('P1 $' + str(self._system.person.bank), True, PINK)
        self._text_com = self._font.render('COM $' + str(self._system.com.bank), True, CYAN)
        self._text_min = self._font.render('Minimum Wager $' + str(self._system.min_wager), True, PURPLE)
        self._text_pot = self._font.render('POT $' + str(self._system.pot), True, GOLD)
        self._text_warn1 = self._font.render('Please input an integer!', True, WHITE)
        self._text_warn2 = self._font.render('Input should bigger than the minimum wager and less than both of your '
                                             'bank!', True, WHITE)
        self._text_audio_on = self._font.render('Audio: On', True, GRAY)
        self._text_audio_off = self._font.render('', True, GRAY)

        ## Variables who handling input process
        # check is inputting or not
        self._inputting = False
        # the string variable who record user input
        self._how_many = ''
        # display the user input on screen
        self._text_input = self._font.render(self._how_many, True, BROWN)

        # Back ground music
        self._audio = True
        self._volume = VOLUME
        pygame.mixer.music.load(BGM_DIR)
        pygame.mixer.music.set_volume(self._volume)
        pygame.mixer.music.play(-1)

        # display game start cards(ai and table cards will face down)
        self.display_game_start()

    # mouse event
    def mouse_button_down(self, x, y):
        return

    # key event
    def key_up(self, key, event):
        # Press return, only trigger when a game is end
        if key == pygame.K_RETURN and self._start is False:
            # if ai or person lose all money
            if self._system.lose_all():
                os.execl(sys.executable, sys.executable, *sys.argv)
            # shuffle card, draw card, set turn to 1
            self._system.game_start()
            # display game start cards(ai and table cards will face down)
            self.display_game_start()
            # reset the result and next game text to white
            self.reset_text()
            # update the money
            self.update_money()
            # start next game
            self._start = True

        # raise, if is inputting, then just go back here and input
        elif (key == pygame.K_l and self._start is True) or self._inputting is True:
            self.raise_proc(key, event)

        # fold
        elif key == pygame.K_j and self._start is True:
            self.fold_proc()

        # check
        elif key == pygame.K_k and self._start is True:
            self.check_proc()

        # Audio
        elif key == pygame.K_a:
            self.audio_control()

        # increase volume
        elif key == pygame.K_UP and self._audio is True and self._volume <= 0.9:
            self._volume += 0.1
            pygame.mixer.music.set_volume(self._volume)

        # decrease volume
        elif key == pygame.K_DOWN and self._audio is True and self._volume >= 0.1:
            self._volume -= 0.1
            pygame.mixer.music.set_volume(self._volume)

    def raise_proc(self, key, event):
        # start to input, so set inputting is true
        self._inputting = True
        # show the 'Raise $' on screen let user see
        self._text_input = self._font.render('Raise $' + self._how_many, True, BROWN)
        # hide the warning
        self._text_warn1 = self._font.render('Please input an integer!', True, WHITE)
        self._text_warn2 = self._font.render('Input should bigger than the minimum wager and less than both of your '
                                             'bank!',
                                             True
                                             , WHITE)
        # record user input, put them in the how_many string, only record 0 to 9, update display at same time
        if ord('0') <= ord(event.unicode) <= ord('9'):
            self._how_many += event.unicode
            self._text_input = self._font.render('Raise $' + self._how_many, True, BROWN)

        if (not ord('0') <= ord(event.unicode) <= ord('9')) and key != pygame.K_BACKSPACE and key != pygame.K_RETURN:
            # Show the warning
            self._text_warn1 = self._font.render('Please input an integer!', True, ORANGE)

        # delete function here, if how_many string len is not 0, user can delete by pressing back space
        if len(self._how_many) > 0 and key == pygame.K_BACKSPACE:
            self._how_many = self._how_many[:-1]
            self._text_input = self._font.render('Raise $' + self._how_many, True, BROWN)

        # if there are some digit input , after user press enter
        # we will check input and see go to raise process or not
        if len(self._how_many) > 0 and key == pygame.K_RETURN:
            # Input should bigger than the minimum wager and less then your bank!
            if (int(self._how_many) < MINIMUM_WAGER) or \
               (int(self._how_many) > self._system.person.bank) or \
               (int(self._how_many) > self._system.com.bank):
                # clear input, let user input again
                self._how_many = ''
                self._text_input = self._font.render('Raise $' + self._how_many, True, BROWN)
                self._text_warn2 = self._font.render(
                    'Input should bigger than the minimum wager and less than both of your bank!', True
                    , ORANGE)
            # if everything is ok
            else:
                # not inputting any more
                self._inputting = False
                # hide the input text
                self._text_input = self._font.render('', True, BROWN)
                # raise process in lower level, pass the user input to lower level
                self._system.raise_process(int(self._how_many))
                # clear the how_many string for next input
                self._how_many = ''
                # update cards, money in every turn
                self.update_turns()

    def fold_proc(self):
        # fold process in lower level
        self._system.fold_process()
        # show result and next game text
        self._text_next = self._font.render('Press RETURN for next game', True, BLACK)
        self._text_lose = self._font.render('You lose!', True, RED)
        # end the game
        self._start = False
        # update p1, com bank and pot
        self.update_money()

    def check_proc(self):
        # check process in lower level
        self._system.check_process()
        # update cards, money in every turn
        self.update_turns()

    def audio_control(self):
        if self._audio:
            pygame.mixer.music.pause()
            self._text_audio_on = self._font.render('', True, GRAY)
            self._text_audio_off = self._font.render('Audio: Off', True, GRAY)
            self._audio = False
        else:
            pygame.mixer.music.unpause()
            self._text_audio_on = self._font.render('Audio: On', True, GRAY)
            self._text_audio_off = self._font.render('', True, GRAY)
            self._audio = True

    # display 5 table card back, 2 ai card back , and 2 person hand card
    def display_game_start(self):
        # person hand card
        person_card1_file = DECK_DIR + '/' + self._system.person.cards[0] + '.gif'
        person_card2_file = DECK_DIR + '/' + self._system.person.cards[1] + '.gif'
        self._person_card1 = ImageSprite(25, 550, person_card1_file)
        self._person_card2 = ImageSprite(100, 550, person_card2_file)

        # table and com card back
        self._card_back1 = ImageSprite(150, 100, DECK_DIR + '/b.gif')
        self._card_back2 = ImageSprite(250, 100, DECK_DIR + '/b.gif')
        self._card_back3 = ImageSprite(350, 100, DECK_DIR + '/b.gif')
        self._card_back4 = ImageSprite(450, 100, DECK_DIR + '/b.gif')
        self._card_back5 = ImageSprite(550, 100, DECK_DIR + '/b.gif')
        self._card_back6 = ImageSprite(625, 550, DECK_DIR + '/b.gif')
        self._card_back7 = ImageSprite(700, 550, DECK_DIR + '/b.gif')

        # display table card back, com card back, and person hand card
        self.add(self._card_back1)
        self.add(self._card_back2)
        self.add(self._card_back3)
        self.add(self._card_back4)
        self.add(self._card_back5)
        self.add(self._card_back6)
        self.add(self._card_back7)
        self.add(self._person_card1)
        self.add(self._person_card2)

    # display first three of table card
    def display_first_three_card(self):
        # first three table card
        table_card1_file = DECK_DIR + '/' + self._system.table_cards[0] + '.gif'
        table_card2_file = DECK_DIR + '/' + self._system.table_cards[1] + '.gif'
        table_card3_file = DECK_DIR + '/' + self._system.table_cards[2] + '.gif'
        self._table_card1 = ImageSprite(150, 100, table_card1_file)
        self._table_card2 = ImageSprite(250, 100, table_card2_file)
        self._table_card3 = ImageSprite(350, 100, table_card3_file)

        # display first three table card
        self.add(self._table_card1)
        self.add(self._table_card2)
        self.add(self._table_card3)

    # display 4th of table card
    def display_fourth_card(self):
        # read and display 4th table card
        table_card4_file = DECK_DIR + '/' + self._system.table_cards[3] + '.gif'
        self._table_card4 = ImageSprite(450, 100, table_card4_file)
        self.add(self._table_card4)

    # display 5th of table card
    def display_fifth_card(self):
        # read and display 5th table card
        table_card5_file = DECK_DIR + '/' + self._system.table_cards[4] + '.gif'
        self._table_card5 = ImageSprite(550, 100, table_card5_file)
        self.add(self._table_card5)

    # display 2 ai card
    def display_com_hand_card(self):
        # Com hand card
        com_card1_file = DECK_DIR + '/' + self._system.com.cards[0] + '.gif'
        com_card2_file = DECK_DIR + '/' + self._system.com.cards[1] + '.gif'
        self._com_card1 = ImageSprite(625, 550, com_card1_file)
        self._com_card2 = ImageSprite(700, 550, com_card2_file)

        # display com hand card
        self.add(self._com_card1)
        self.add(self._com_card2)

    # display all text in run()
    def display_text(self):
        self._display.blit(self._text_fold, (300, 150))
        self._display.blit(self._text_check, (300, 175))
        self._display.blit(self._text_raise, (300, 200))
        self._display.blit(self._text_next, (250, 575))
        self._display.blit(self._text_lose, (350, 540))
        self._display.blit(self._text_win, (350, 515))
        self._display.blit(self._text_tie, (375, 490))
        self._display.blit(self._text_pot, (350, 400))
        self._display.blit(self._text_person, (50, 400))
        self._display.blit(self._text_com, (650, 400))
        self._display.blit(self._text_min, (300, 300))
        self._display.blit(self._text_input, (25, 350))
        self._display.blit(self._text_warn1, (25, 275))
        self._display.blit(self._text_warn2, (25, 250))
        self._display.blit(self._text_audio_on, (700, 0))
        self._display.blit(self._text_audio_off, (698, 0))

    # reset the result and next game text to white
    def reset_text(self):
        self._text_next = self._font.render('Press RETURN for next game', True, WHITE)
        self._text_lose = self._font.render('You lose!', True, WHITE)
        self._text_win = self._font.render('You win!', True, WHITE)
        self._text_tie = self._font.render('Tie.', True, WHITE)

    # update p1, com bank and pot
    def update_money(self):
        text = self._font.render('P1 $' + str(self._system.person.bank), True, PINK)
        self._text_person = text
        text = self._font.render('COM $' + str(self._system.com.bank), True, CYAN)
        self._text_com = text
        text = self._font.render('POT $' + str(self._system.pot), True, GOLD)
        self._text_pot = text

    # update cards, money in every turn
    def update_turns(self):
        # Turn 2
        if self._system.turn == 2:
            # display first three card
            self.display_first_three_card()

        # Turn 3
        elif self._system.turn == 3:
            # display fourth card
            self.display_fourth_card()

        # Turn 4
        elif self._system.turn == 4:
            # display fifth card
            self.display_fifth_card()

        # Turn 5
        elif self._system.turn == 5:
            # show ai hand card
            self.display_com_hand_card()
            # show next text
            self._text_next = self._font.render('Press RETURN for next game', True, BLACK)

            is_person_win = self._system.is_person_win()

            # according to result, display result text, lower level calculate in is_person_win()
            if is_person_win == TIE:
                self._text_tie = self._font.render('Tie.', True, BLUE)

            elif is_person_win == WIN:
                self._text_win = self._font.render('You win!', True, GREEN)

            elif is_person_win == LOSE:
                self._text_lose = self._font.render('You lose!', True, RED)

            # end the game at last turn
            self._start = False

        # update p1, com bank and pot
        self.update_money()

    def update(self):
        super().update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_down(event.pos[0], event.pos[1])
                elif event.type == pygame.KEYUP:
                    self.key_up(event.key, event)

            self.update()
            self._display.fill(WHITE)
            self.display_text()
            self.draw()
            pygame.display.update()
            self._clock.tick(self._framesPerSecond)
            self._ticks += 1
