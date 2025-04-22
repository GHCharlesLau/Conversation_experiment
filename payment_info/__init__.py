from otree.api import *
import random



doc = """
This application provides a webpage instructing participants how to get paid.
Examples are given for the lab and Amazon Mechanical Turk (AMT).
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_info'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    finishCode = models.StringField(initial='HCM246HCH')
    pass


# FUNCTIONS
# PAGES
class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['finishCode']

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.finished == True
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                    finishCode=player.finishCode,
                    )

class EndNoConsent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.finished == False

page_sequence = [PaymentInfo, EndNoConsent]
