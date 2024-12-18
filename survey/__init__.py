from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label):
    return models.IntegerField(
        choices=[1,2,3,4,5,6,7],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    name = models.StringField(label='What is your name?')
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    SocialPresence = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7],
        label='You are interacting with an intelligent being.',  
    )
    q1 = make_field('You are interacting with an intelligent being.')
    q2 = make_field('You are not alone.')
    q3 = make_field('You are in the setting with an intelligent being.')
    q4 = make_field('An intelligent being is responding to you.')


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ["name",'age', 'gender']


class SocialPresence(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4']


page_sequence = [Demographics, SocialPresence]
