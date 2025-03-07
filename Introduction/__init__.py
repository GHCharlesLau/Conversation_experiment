from otree.api import *
import time


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    agreement = models.BooleanField(
        label='Do you agree to participate in this study?',
        widget=widgets.RadioSelectHorizontal,
    )
    avatar = models.StringField(
        label='Please choose your avatar',
        choices=["🐱", "🦁", "🐯", "🦊"],
        widget=widgets.RadioSelectHorizontal
    )
    nickname = models.StringField(
        label='Please enter your nickname',
    )


# FUNCTIONS
# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['agreement']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):  # Skip to the final page if the participant does not agree to participate (have to delete the button in the template)
        if player.agreement == False:
            return upcoming_apps[-1]


class WelcomePage(Page):
    form_model = 'player'
    form_fields = ['avatar', 'nickname']
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):  # record the timestamp when the participant arrives at the wait page
        player.participant.wait_page_arrival = time.time()
        player.participant.avatar = player.avatar
        player.participant.nickname = player.nickname
        print(f"The player's (idInGroup: {player.id_in_group}) nickname is {player.participant.nickname}")


page_sequence = [ConsentPage, WelcomePage]