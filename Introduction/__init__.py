from otree.api import *
import time
import datetime as dt


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
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

    # Add a label for the session
    session = subsession.session
    now = dt.datetime.now()
    format_date = now.strftime("%Y-%m-%d %H:%M:%S")
    session.label = format_date


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    agreement = models.BooleanField(
        label='Do you agree to participate in this study?',
        widget=widgets.RadioSelectHorizontal,
    )
    avatar = models.StringField(
        label='Please choose your avatar:',
        # choices=["👩‍🦰", "👨‍🦰", "👩‍🦱", "👨‍🦱"],
        # choices=["<img src='{{ static 'avatar/Woman1.jpg' }}'/>", 
        #          "<img src='{{ static 'avatar/Man1.jpg' }}'/>",
        #          "<img src='{{ static 'avatar/Woman2.jpg' }}'/>",
        #          "<img src='{{ static 'avatar/Man2.jpg' }}'/>",
        #          ],
        # widget=widgets.RadioSelectHorizontal
    )
    prolificID = models.StringField(
        label='Please enter your prolific ID:',
    )
    nickname = models.StringField(
        label='Please enter your nickname:',
    )
    taskType = models.StringField(
        choices=['emotionTask', 'functionTask'],
    )
    partnership = models.StringField(
        choices=['HMC', 'HHC'],
    )
    partnerLabel = models.StringField(
        choices=['chatbot', 'human'],
    )

def prolificID_error_message(player, value):
    if len(value) != 24:
        return 'Please enter a valid Prolific ID (24 characters).'


# FUNCTIONS
# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['agreement']

    @staticmethod
    def is_displayed(player: Player):
        timestamp = dt.datetime.now(dt.timezone.utc)
        player.participant.start_utc = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return True
    @staticmethod
    def app_after_this_page(player, upcoming_apps):  # Skip to the final page if the participant does not agree to participate (have to delete the button in the template)
        if player.agreement == False:
            return upcoming_apps[-1]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.agreement == False:
            player.participant.finished = False


def make_image_data(image_names):
    return [dict(name=name, path='avatar/{}'.format(name), index=i) for i, name in enumerate(image_names)]


class WelcomePage(Page):
    form_model = 'player'
    form_fields = ['prolificID', 'avatar', 'nickname']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()
        player.participant.prolificID = str(player.prolificID)
        player.participant.avatar = player.avatar
        player.participant.nickname = player.nickname
        print(f"The player's (idInGroup: {player.id_in_group}) nickname is {player.participant.nickname}")
        # Transfer players's propertities to the participant object for later use
        player.participant.taskType = player.taskType
        player.participant.partnership = player.partnership
        player.participant.partnerLabel = player.partnerLabel

    @staticmethod
    def vars_for_template(player: Player):
        image_names = [
            'fox.png',
            'lion.png',
            'rabbit.png',
            'tiger.png',
        ]
        return dict(image_data=make_image_data(image_names))


page_sequence = [ConsentPage, WelcomePage]