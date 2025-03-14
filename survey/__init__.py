from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_field(label):  # Reduce the amount of repeated code by defining a function that returns a field
    return models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label=label,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    # Social Presence
    SP_1 = make_field('You are interacting with an intelligent being.')
    SP_2 = make_field('You are not alone.')
    SP_3 = make_field('You are in the setting with an intelligent being.')
    SP_4 = make_field('An intelligent being is responding to you.')

    # Demographics
    name = models.StringField(label='What is your name?')
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
# PAGES
class survey_prompt(Page):
    pass


class survey_variables(Page):
    form_model = 'player'
    form_fields = ['SP_1', 'SP_2', 'SP_3', 'SP_4']


class Demographics(Page):
    form_model = 'player'
    form_fields = ["name", 'age', 'gender']


page_sequence = [survey_prompt, survey_variables, Demographics]
