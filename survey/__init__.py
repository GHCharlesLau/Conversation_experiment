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

    # Sense of Agency
    senA_1 = make_field('The conversational partner in the first round is capable of thought.')
    senA_2 = make_field('The conversational partner in the first round is capable of planning.')
    senA_3 = make_field('The conversational partner in the first round has the ability to solve problems.')
    senA_4 = make_field('The conversational partner in the first round has its own personality.')
    senA_5 = make_field('The conversational partner in the first round is capable of communication.')
    senA_6 = make_field('The conversational partner in the first round can experience emotions.')
    senA_7 = make_field('The conversational partner in the first round  is capable of memory.')
    senA_8 = make_field('The conversational partner in the first round is capable of acting morally.')

    # Feeling Heard
    fh_1 = make_field('The conversational partner in the first round is interested in what I have to say.')
    fh_2 = make_field('The conversational partner in the first round encourages me to speak openly.')
    fh_3 = make_field('The conversational partner in the first round understands my thoughts.')
    fh_4 = make_field('The conversational partner in the first round cares about me.')

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
    form_fields = ['senA_1', 'senA_2', 'senA_3', 'senA_4', 'senA_5', 'senA_6', 'senA_7', 'senA_8',
                #    'fh_1', 'fh_2', 'fh_3', 'fh_4',
                   ]


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']

    @staticmethod
    def before_next_page(player: Player):
        player.participant.finished = True


page_sequence = [survey_prompt, survey_variables, Demographics]
