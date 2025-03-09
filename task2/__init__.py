from otree.api import *
import time

doc = """
Factor: Task: ['emotionTask', 'functionTask']
"""

class C(BaseConstants):
    NAME_IN_URL = 'task2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    primingText2 = models.LongStringField()
    # pass

#PAGES
class chatInstruct_emo_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HMC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_emo_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.participant.taskType == 'emotionTask' and player.participant.partnership == 'HHC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_fun_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.participant.taskType == 'functionTask' and player.participant.partnership == 'HMC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_fun_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.participant.taskType == 'functionTask' and player.participant.partnership == 'HHC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()


page_sequence = [chatInstruct_emo_AI, chatInstruct_emo_human, chatInstruct_fun_AI, chatInstruct_fun_human]