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

def creating_session(subsession):  
    import itertools

    treatments = itertools.cycle(
        itertools.product(['emotionTask', 'functionTask'], ['HMC', 'HHC'], ['chatbot', 'human'])
    )
    for p in subsession.get_players():
        treatment = next(treatments)
        # print('treatment is', treatment)
        p.taskType = treatment[0]
        p.partnership = treatment[1]
        p.partnerLabel = treatment[2]

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    taskType = models.StringField(
        choices=['emotionTask', 'functionTask'],
    )
    partnership = models.StringField(
        choices=['HMC', 'HHC'],
    )
    partnerLabel = models.StringField(
        choices=['chatbot', 'human'],
    )
    primingText2 = models.LongStringField()
    # pass

#PAGES
class chatInstruct_emo_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'emotionTask' and player.partnership == 'HMC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_emo_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'emotionTask' and player.partnership == 'HHC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_fun_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'functionTask' and player.partnership == 'HMC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

class chatInstruct_fun_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'functionTask' and player.partnership == 'HHC'
    # pass
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()


page_sequence = [chatInstruct_emo_AI, chatInstruct_emo_human, chatInstruct_fun_AI, chatInstruct_fun_human]