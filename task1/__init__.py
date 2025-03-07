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

# factorial experiment: balanced design
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
    primingText = models.LongStringField(default='At least 20 words...')
    # pass


#PAGES
class emotionTask(Page):
    form_model = 'player'
    form_fields = ['primingText']

    @staticmethod
    def is_displayed(player: Player):
        return player.taskType == 'emotionTask'
    # pass

class functionTask(Page):
    form_model = 'player'
    form_fields = ['primingText']

    @staticmethod
    def is_displayed(player: Player):
        return player.taskType == 'functionTask'
    # pass


class chatInstruct_emo_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'emotionTask' and player.partnership == 'HMC'
    # pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'emotionTask' and player.partnership == 'HMC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps)


class chatInstruct_emo_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'emotionTask' and player.partnership == 'HHC'
    # pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()
    
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'emotionTask' and player.partnership == 'HHC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps)


class chatInstruct_fun_AI(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'functionTask' and player.partnership == 'HMC'
    # pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'functionTask' and player.partnership == 'HMC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps)

class chatInstruct_fun_human(Page):
    @staticmethod
    def is_displayed(player: Player):  # Only display this page if the player will converse with a chatbot
        return player.taskType == 'functionTask' and player.partnership == 'HHC'
    # pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()
    
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.taskType == 'functionTask' and player.partnership == 'HHC':
            print('upcoming_apps is', upcoming_apps)
            return upcoming_apps[0]  # Or return a hardcoded string (as long as that string is in upcoming_apps)


page_sequence = [emotionTask, functionTask, chatInstruct_emo_AI, chatInstruct_emo_human, chatInstruct_fun_AI, chatInstruct_fun_human]