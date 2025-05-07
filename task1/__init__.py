from otree.api import *
import time

doc = """
Factor: Task: ['emotionTask', 'functionTask']
"""

class C(BaseConstants):
    NAME_IN_URL = 'task1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    primingText = models.LongStringField(default='')
    # pass

def primingText_error_message(player, value):  #  The most flexible method for validating a field.
    if len(value) < 20:
        return 'Please enter at least 20 words.'


#PAGES
class taskPriming(Page):
    form_model = 'player'
    form_fields = ['primingText']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.partnership == 'HHC':
            print('upcoming_apps is', upcoming_apps)
            return "chatHHC"  # Or return a hardcoded string (as long as that string is in upcoming_apps)
        elif player.participant.partnership == 'HMC':
            print('upcoming_apps is', upcoming_apps)
            return "chatHMC"


page_sequence = [
    taskPriming,
    chatInstruct,
    ]